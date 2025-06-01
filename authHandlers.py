import logging
import requests
from flask import flash, session, redirect, render_template, request, url_for
import databaseManagement as dbHandler
from twoFactor import generate_totp_secret, get_totp_uri, generate_qr_code, verify_totp
from sanitize import sanitize_data

app_log = logging.getLogger(__name__)
app_header = {"Authorisation": "uPTPeF9BDNiqAkNj"}

def handle_login(loginForm):
    rate_limit_exceeded = False 
    if loginForm.validate_on_submit():
        sanitized_data = sanitize_data({
            "username": loginForm.username.data,
            "password": loginForm.password.data
        })
        try:
            response = requests.post("http://127.0.0.1:3000/api/login", json=sanitized_data, headers=app_header, timeout=5)
            response.raise_for_status()
            if response.status_code == 200:
                user_data = response.json()
                session['username'] = loginForm.username.data
                session['role'] = user_data.get('role')
                session.permanent = True  # Mark the session as permanent
                app_log.info("User '%s' logged in, hasn't passed 2FA", loginForm.username.data)
                return redirect(url_for('two_factor'))
            else:
                flash('Invalid username or password', 'danger')
                app_log.warning("Failed login attempt for user: %s", loginForm.username.data)
        except requests.exceptions.HTTPError as e:
            flash('Invalid username or password', 'danger')
            app_log.error("Invalid login attempt for user: %s - %s", loginForm.username.data, str(e))
        except requests.exceptions.RequestException as e:
            flash('An error occurred. Please try again later.', 'danger')
            app_log.error("Error during login attempt for user: %s - %s", loginForm.username.data, str(e))
    return render_template("login.html", form=loginForm, rate_limit_exceeded=rate_limit_exceeded)

def handle_two_factor(twoFactorForm):
    if 'username' not in session:
        return redirect(url_for('login'))
    username = session['username']
    user = dbHandler.retrieveUserByUsername(username)
    if not user:
        return redirect(url_for('login'))
    secret = user.get('totp_secret')
    twofa_enabled = int(user.get('twofa_enabled', 0)) 
    
    # If user does not have a secret, generate and store one
    if not secret:
        secret = generate_totp_secret()
        dbHandler.updateUserTotpSecret(username, secret)
        twofa_enabled = 0  # Force setup if secret was missing
    show_qr = not twofa_enabled
    qr_code = None
    if show_qr:
        uri = get_totp_uri(secret, username)
        qr_code = generate_qr_code(uri)
    if request.method == "POST" and twoFactorForm.validate_on_submit():
        token = twoFactorForm.token.data
        if verify_totp(token, secret):
            if show_qr:
                dbHandler.setTwoFAEnabled(username, True)
            app_log.info("2FA successful, User '%s' logged in successfully", username)
            return redirect(url_for('index'))
        else:
            flash('Invalid 2FA token', 'danger')
            app_log.warning("Invalid 2FA token for user: %s", username)
    return render_template("2fa.html", form=twoFactorForm, qr_code=qr_code)
 
def handle_sign_up(signUpForm):
    if signUpForm.validate_on_submit():
        sanitized_data = sanitize_data({
            "username": signUpForm.username.data,
            "password": signUpForm.password.data,
            "email": signUpForm.email.data,
            "full_name": signUpForm.full_name.data,
            "role": signUpForm.role.data
        })      
        try:
            response = requests.post("http://127.0.0.1:3000/api/signup", json=sanitized_data, headers=app_header, timeout=5)
            response.raise_for_status()
            if response.status_code == 201:
                app_log.info("User '%s' signed up successfully", signUpForm.username.data)
                #flash('Sign up successful. Please log in.', 'success')
                return redirect(url_for('login'))
            else:
                flash('An error occurred during sign up. Please try again.', 'danger')
                app_log.warning("Failed signup attempt for user: %s", signUpForm.username.data)
        except requests.exceptions.RequestException as e:
            flash('An error occurred', 'danger')
            app_log.error("Error during signup attempt for user: %s - %s", signUpForm.username.data, str(e))
    else:
        for field, errors in signUpForm.errors.items():
            for error in errors: 
                flash(f"Error in {getattr(signUpForm, field).label.text}: {error}", 'danger')
                app_log.warning("Validation error in %s: %s", getattr(signUpForm, field).label.text, error)
    return render_template('signUp.html', form=signUpForm)

