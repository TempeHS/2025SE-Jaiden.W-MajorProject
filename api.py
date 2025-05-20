from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import logging
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
    return jsonify(response), status_code

@api.route("/api/signup", methods=["POST"])
@limiter.limit("1/second", override_defaults=False)
def api_signup():
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


if __name__ == "__main__":
    api.run(debug=True, host="0.0.0.0", port=3000)