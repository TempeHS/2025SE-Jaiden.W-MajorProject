import logging
from datetime import timedelta
from flask import Flask, render_template, request, redirect, flash, session, url_for
from flask_wtf.csrf import CSRFProtect
from flask_csp.csp import csp_header
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_cors import CORS
from flask_session import Session
from flask_socketio import SocketIO

import chatSocket
from forms import LoginForm, SignUpForm, TwoFactorForm, JoinTeamForm, TeamForm, TeamEventForm, DeleteUserForm, UpdateProfileForm
from authHandlers import handle_login, handle_two_factor, handle_sign_up
import teamHandlers as teamHandler
from sessionLocks import acquire_session_lock, cleanup_session_lock
from profileHandler import deleteData, handle_profile

app = Flask(__name__)
app.secret_key = b"T4Ht6NAcHy2yNDH3;apl"
limiter = Limiter(get_remote_address, app=app)
csrf = CSRFProtect(app)
cors = CORS(app)
socketio = SocketIO(app, cors_allowed_origins= "*")
app.config["CORS_HEADERS"] = "Content-Type"

# logging configuration
app_log = logging.getLogger(__name__)
logging.basicConfig(
    filename="security_log.log",
    encoding="utf-8",
    level=logging.DEBUG,
    format="%(asctime)s %(message)s",
)

# Flask-Session configuration
app.config["SESSION_TYPE"] = "filesystem"
app.config["SESSION_PERMANENT"] = True  # Make sessions permanent
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(minutes=720)  # Set session lifetime to 24 hrs
app.config["SESSION_USE_SIGNER"] = True
app.config["SESSION_KEY_PREFIX"] = "session:"
app.config["SESSION_FILE_DIR"] = "./.flask_session/"
app.config["SESSION_FILE_THRESHOLD"] = 100
Session(app)

# Secure cookie settings
app.config.update(
    SESSION_COOKIE_SECURE=True,  # Ensure cookies are only sent over HTTPS
    SESSION_COOKIE_HTTPONLY=True,  # Prevent JavaScript access to cookies
    SESSION_COOKIE_SAMESITE='Lax',  # Control how cookies are sent with cross-site requests
)

# Import and register chatSocket events here
chatSocket.register_socketio_events(socketio, app_log)

# Register the cleanup function to be called after each request
@app.teardown_request
def teardown_request(exception=None):
    return cleanup_session_lock(exception)

# Custom error handler for rate limit exceeded
@app.errorhandler(429)
def ratelimit_handler(_e):
    """Custom error handler for rate limit exceeded."""
    flash("Too many incorrect attempts. Please try again later.", "danger")
    app_log.warning("Rate limit exceeded for IP: %s", request.remote_addr)
    return render_template("login.html", form=LoginForm(), rate_limit_exceeded=True), 429


# Redirect index.html to domain root for consistent UX
@app.route("/index", methods=["GET"])
@app.route("/index.htm", methods=["GET"])
@app.route("/index.asp", methods=["GET"])
@app.route("/index.php", methods=["GET"])
@app.route("/index.html", methods=["GET"])
def root():
    return redirect("/", 302)

@app.route("/", methods=["POST", "GET"])
@csp_header(
    {
        # Server Side CSP is consistent with meta CSP in layout.html
        "base-uri": "'self'",
        "default-src": "'self'",
        "style-src": "'self'",
        "script-src": "'self' https://cdnjs.cloudflare.com",
        "img-src": "'self' data:",
        "media-src": "'self'",
        "font-src": "'self'",
        "object-src": "'self'",
        "child-src": "'self'",
        "connect-src": "'self'",
        "worker-src": "'self'",
        "report-uri": "/csp_report",
        "frame-ancestors": "'none'",
        "form-action": "'self'",
        "frame-src": "'none'",
    }
)
def index():
    lock = acquire_session_lock()
    with lock:
        return teamHandler.handle_my_team()

@app.route("/login.html", methods=["GET", "POST"])
@limiter.limit("5 per minute")
def login():
    loginForm = LoginForm()
    return handle_login(loginForm)

@app.route("/2fa", methods=["GET", "POST"])
def two_factor():
    twoFactorForm = TwoFactorForm()
    lock = acquire_session_lock()
    with lock:
        return handle_two_factor(twoFactorForm)

@app.route("/signUp.html", methods=["GET", "POST"])
def sign_up():
    signUpForm = SignUpForm()
    return handle_sign_up(signUpForm)

@app.route("/privacy.html", methods=["GET"])
def privacy():
    return render_template("/privacy.html")

@app.route('/searchteam', methods=['GET'])
def search_team():
    joinTeamForm = JoinTeamForm()
    lock = acquire_session_lock()
    with lock:
        return teamHandler.handle_search_team(joinTeamForm)

@app.route('/jointeam/<int:team_id>', methods=['POST'])
def join_team(team_id):
    lock = acquire_session_lock()
    with lock:
        return teamHandler.handle_join_team(team_id)

@app.route('/create_team', methods=['GET', 'POST'])
def create_team():
    teamForm = TeamForm()
    lock = acquire_session_lock()
    with lock:
        return teamHandler.handle_create_team(teamForm)

# dynamic flask route for specific teams
@app.route('/team/<int:team_id>', methods=['GET'])
def team_detail(team_id):
    lock = acquire_session_lock()
    with lock:
        return teamHandler.handle_team_detail(team_id)

@app.route('/team/<int:team_id>/events', methods=['GET', 'POST'])
def team_events(team_id):
    lock = acquire_session_lock()
    with lock:
        return teamHandler.handle_team_events(team_id)

@app.route('/team/<int:team_id>/create_event', methods=['GET', 'POST'])
def create_team_event(team_id):
    form = TeamEventForm()
    lock = acquire_session_lock()
    with lock:
        return teamHandler.handle_create_team_event(team_id, form)

@app.route('/team/<int:team_id>/delete_event/<int:event_id>', methods=['POST'])
def delete_team_event(team_id, event_id):
    lock = acquire_session_lock()
    with lock:
        return teamHandler.handle_delete_team_event(team_id, event_id)
    
@app.route('/team/<int:team_id>/event/<int:event_id>/attendance', methods=['GET', 'POST'])
def event_attendance(team_id, event_id):
    lock = acquire_session_lock()
    with lock:
        return teamHandler.handle_event_attendance(team_id, event_id)

@app.route('/team/<int:team_id>/messages', methods=['GET', 'POST'])
def team_messages(team_id):
    lock = acquire_session_lock()
    with lock:
        return teamHandler.handle_team_messages(team_id)

@app.route("/logout")
def logout():
    username = session.pop('username', None)
    if username:
        app_log.info("User '%s' logged out successfully", username)
    flash('You have been logged out.', 'success')
    return redirect("login.html")

@app.route("/profile.html", methods=["GET", "POST"])
def profile():
    lock = acquire_session_lock()
    with lock:
        return handle_profile()

@app.route("/delete_data", methods=["POST"])
def delete_data():
    lock = acquire_session_lock()
    with lock:
        return deleteData(app)

# Endpoint for logging CSP violations
@app.route("/csp_report", methods=["POST"])
@csrf.exempt
def csp_report():
    app.logger.critical(request.data.decode())
    return "done"

if __name__ == "__main__":
    socketio.run(app, debug=True, host="0.0.0.0", port=5000)
