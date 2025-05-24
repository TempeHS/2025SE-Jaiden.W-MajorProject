from flask import flash, session, redirect, render_template, request, url_for
import requests
import logging
import databaseManagement as dbHandler
from twoFactor import generate_totp_secret, get_totp_uri, generate_qr_code, verify_totp
from sanitize import sanitize_data, sanitize_input

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
            response = requests.post("http://127.0.0.1:3000/api/login", json=sanitized_data, headers=app_header)
            response.raise_for_status()
            if response.status_code == 200:
                session['username'] = loginForm.username.data
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
            return redirect(url_for('team'))
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
            response = requests.post("http://127.0.0.1:3000/api/signup", json=sanitized_data, headers=app_header)
            response.raise_for_status()
            if response.status_code == 201:
                app_log.info("User '%s' signed up successfully", signUpForm.username.data)
                #flash('Sign up successful. Please log in.', 'success')
                return redirect(url_for('login'))
            else:
                flash('An error occurred during sign up. Please try again.', 'danger')
                app_log.warning("Failed signup attempt for user: %s", signUpForm.username.data)
        except requests.exceptions.RequestException as e:
            flash(f'An error occurred', 'danger')
            app_log.error("Error during signup attempt for user: %s - %s", signUpForm.username.data, str(e))
    else:
        for field, errors in signUpForm.errors.items():
            for error in errors: 
                flash(f"Error in {getattr(signUpForm, field).label.text}: {error}", 'danger')
                app_log.warning("Validation error in %s: %s", getattr(signUpForm, field).label.text, error)
    return render_template('signUp.html', form=signUpForm)

def handle_my_team():
    if 'username' not in session:
        return redirect(url_for('login'))
    user = dbHandler.retrieveUserByUsername(session['username'])
    if not user or not user.get('team_id'):
        flash("You have not joined a team yet.", "info")
        return render_template('team.html', team=None)
    team = dbHandler.get_team_by_id(user['team_id'])
    return render_template('team.html', team=team)

def handle_search_team(JoinTeamForm):
    query = request.args.get('q', '')
    query = sanitize_input(query)
    params = {}
    if query:
        params['q'] = query
    try:
        response = requests.get("http://127.0.0.1:3000/api/search_teams", params=params, headers=app_header)
        response.raise_for_status()
        teams = response.json().get("teams", [])
    except Exception as e:
        flash("Could not fetch teams from the server.", "danger")
        teams = []
    return render_template('searchTeam.html', teams=teams, query=query, form=JoinTeamForm)

def handle_join_team(team_id):
    if 'username' not in session:
        return redirect(url_for('login'))
    user = dbHandler.retrieveUserByUsername(session['username'])
    dbHandler.update_user_team(user['username'], team_id)
    flash("You have joined the team!", "success")
    return redirect(url_for('search_team'))

def handle_create_team(teamForm):
    if 'username' not in session:
        return redirect(url_for('login'))
    user = dbHandler.retrieveUserByUsername(session['username'])
    if not user or user.get('role') != 'Coach':
        return redirect(url_for('team'))
    if teamForm.validate_on_submit():
        sanitized_data = sanitize_data({
            "name": teamForm.team_name.data,
            "description": teamForm.team_description.data
        })
        try:
            response = requests.post("http://127.0.0.1:3000/api/create_team", json=sanitized_data, headers=app_header)
            response.raise_for_status()
            if response.status_code == 201:
                app_log.info("Team '%s' created successfully", teamForm.team_name.data)
                flash('Team created successfully!', 'success')
                return redirect(url_for('search_team'))
            else:
                flash('An error occurred during team creation. Please try again.', 'danger')
                app_log.warning("Failed team creation attempt: %s", teamForm.team_name.data)
        except requests.exceptions.RequestException as e:
            flash('An error occurred. Please try again later.', 'danger')
            app_log.error("Error during team creation attempt: %s - %s", teamForm.team_name.data, str(e))
    else:
        for field, errors in teamForm.errors.items():
            for error in errors: 
                flash(f"Error in {getattr(teamForm, field).label.text}: {error}", 'danger')
                app_log.warning("Validation error in %s: %s", getattr(teamForm, field).label.text, error)
    return render_template('createTeam.html', form=teamForm)

def handle_team_detail(team_id):
    team = dbHandler.get_team_by_id(team_id)
    if not team:
        flash("Team not found.", "danger")
        return redirect(url_for('team'))
    return render_template('teamDetail.html', team=team)

def handle_team_events(team_id):
    team = dbHandler.get_team_by_id(team_id)
    return render_template('teamEvents.html', team=team)

def handle_team_messages(team_id):
    team = dbHandler.get_team_by_id(team_id)
    return render_template('teamMessages.html', team=team)