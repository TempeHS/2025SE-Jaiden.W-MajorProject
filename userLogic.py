import databaseManagement as dbHandler
from werkzeug.security import generate_password_hash, check_password_hash
from twoFactor import generate_totp_secret
import logging

app_log = logging.getLogger(__name__)

def login_user(username, password):
    user = dbHandler.retrieveUserByUsername(username)
    if user and check_password_hash(user['password'], password):
        return {"message": "Login successful"}, 200
    else:
        return {"message": "Invalid username or password"}, 401

def signup_user(username, password, email, full_name, role):
    hashed_password = generate_password_hash(password)
    totp_secret = generate_totp_secret()
    try:
        dbHandler.insertUser(username, hashed_password, totp_secret, email, full_name, role)
        return {"message": "User created successfully"}, 201
    except Exception:
        logging.error("Error during signup")
        return {"message": "Internal server error"}, 500