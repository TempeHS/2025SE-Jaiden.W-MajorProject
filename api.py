import logging
from datetime import timedelta, datetime
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from userLogic import login_user, signup_user
import databaseManagement as dbHandler

api = Flask(__name__)
cors = CORS(api)
api.config["CORS_HEADERS"] = "Content-Type"
auth_key = "uPTPeF9BDNiqAkNj"
limiter = Limiter(
    get_remote_address,
    app=api,
    default_limits=["200 per day", "50 per hour"],
    storage_uri="memory://",
)

# Initialize logging
app_log = logging.getLogger(__name__)
logging.basicConfig(
    filename="api_security_log.log",
    encoding="utf-8",
    level=logging.DEBUG,
    format="%(asctime)s %(levelname)s %(message)s",
)

def check_api_key():
    if request.headers.get("Authorisation") != auth_key:
        return jsonify({"message": "Invalid or missing API key"}), 401

@api.route("/api/login", methods=["POST"])
def api_login():
    auth_response = check_api_key()
    if auth_response:
        return auth_response
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    response, status_code = login_user(username, password)
    # if login is sucessful, add user's role to response
    if status_code == 200:
        user = dbHandler.retrieveUserByUsername(username)
        if user:
            response["role"] = user.get("role")
    return jsonify(response), status_code

@api.route("/api/signup", methods=["POST"])
@limiter.limit("1/second", override_defaults=False)
def api_signup():
    """Handles user signup by creating a new user with the provided details."""
    auth_response = check_api_key()
    if auth_response:
        return auth_response
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    email = data.get("email")
    full_name = data.get("full_name")
    role = data.get("role")
    try:
        response, status_code = signup_user(username, password, email, full_name, role)
        return jsonify(response), status_code
    except Exception:
        api.logger.error("Error during signup", exc_info=True)
        return jsonify({"message": "Internal server error"}), 500

@api.route("/api/search_teams", methods=["GET"])
def api_get_teams():
    auth_response = check_api_key()
    if auth_response:
        return auth_response
    query = request.args.get("q", "")
    if query:
        teams = dbHandler.search_teams_by_name(query)
    else:
        teams = dbHandler.get_all_teams()
    return jsonify({"teams": teams}), 200


@api.route("/api/create_team", methods=["POST"])
@limiter.limit("1/second", override_defaults=False)
def api_create_team():
    auth_response = check_api_key()
    if auth_response:
        return auth_response
    data = request.get_json()
    team_name = data.get("name")
    team_description = data.get("description")
    team_profile_picture = data.get("profile_pic")
    try:
        dbHandler.create_team(team_name, team_description, team_profile_picture)
        return jsonify({"message": "Team created successfully"}), 201
    except Exception as e:
        if "already exists" in str(e):
            return jsonify({"message": "A team with this name already exists."}), 400
        api.logger.error("Error creating team: %s", str(e))
        return jsonify({"message": "Internal server error"}), 500

@api.route("/api/create_team_event", methods=["POST"])
@limiter.limit("1/second", override_defaults=False)
def api_create_team_event():
    auth_response = check_api_key()
    if auth_response:
        return auth_response
    data = request.get_json()
    team_id = data.get("team_id")
    title = data.get("title")
    description = data.get("description")
    event_date = data.get("event_date")
    location = data.get("location")
    recurrence = data.get("recurrence")
    recurrence_end = data.get("recurrence_end")
    if not all([team_id, title, event_date, location]):
        return jsonify({"message": "Missing required fields"}), 400
    try:
        dbHandler.create_team_event(team_id, title, description, event_date, location)
        # Handle recurrence
        if recurrence and recurrence != "none" and recurrence_end:
            start_date = datetime.strptime(event_date, "%Y-%m-%dT%H:%M")
            end_date = datetime.strptime(recurrence_end, "%Y-%m-%d")
            next_date = start_date
            while True:
                # Calculate next occurrence
                if recurrence == "daily":
                    next_date += timedelta(days=1)
                elif recurrence == "weekly":
                    next_date += timedelta(weeks=1)
                else:
                    break
                if next_date.date() > end_date.date():
                    break
                dbHandler.create_team_event(
                    team_id, title, description, next_date.strftime("%Y-%m-%dT%H:%M"), location
                )
        return jsonify({"message": "Team event created successfully"}), 201
    except Exception as e:
        api.logger.error("Error creating team event: %s", str(e))
        return jsonify({"message": "Internal server error"}), 500

if __name__ == "__main__":
    api.run(debug=True, host="0.0.0.0", port=3000)
# End-of-file (EOF)
