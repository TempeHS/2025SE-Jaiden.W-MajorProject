import logging
from flask import flash, session, redirect, render_template, request, url_for
import requests
import databaseManagement as dbHandler
from sanitize import sanitize_data, sanitize_input
from forms import DeleteEventForm, AttendanceForm

app_log = logging.getLogger(__name__)
app_header = {"Authorisation": "uPTPeF9BDNiqAkNj"}

def user_in_team(team_id):
    """returns user if logged in and in the given team, else None"""
    if 'username' not in session:
        return None
    user = dbHandler.retrieveUserByUsername(session['username'])
    if not user:
        return None
    try:
        # Always compare as integers
        if int(user.get('team_id')) != int(team_id):
            print(f"User {session['username']} is not in team {team_id}.")
            return None
    except (ValueError, TypeError):
        print("Type error comparing team IDs")
        return None
    return user

def get_logged_in_user():
    if 'username' not in session:
        return None
    return dbHandler.retrieveUserByUsername(session['username'])

def require_role(role):
    user = get_logged_in_user()
    if not user or user.get('role') != role:
        return None
    return user

def handle_my_team():
    user = get_logged_in_user()
    if not user:
        return redirect(url_for('login'))
    if not user or not user.get('team_id'):
        flash("You have not joined a team yet.", "info")
        return render_template('index.html', team=None)
    team = dbHandler.get_team_by_id(user['team_id'])
    return render_template('index.html', team=team)

def handle_search_team(JoinTeamForm):
    query = request.args.get('q', '')
    query = sanitize_input(query)
    params = {}
    if query:
        params['q'] = query
    try:
        response = requests.get("http://127.0.0.1:3000/api/search_teams", params=params, headers=app_header, timeout=5)
        response.raise_for_status()
        teams = response.json().get("teams", [])
    except Exception as _e:
        flash("Could not fetch teams from the server.", "danger")
        teams = []
    user = get_logged_in_user()
    if user: 
        user_team_id = user.get('team_id')
    return render_template('searchTeam.html', teams=teams, query=query, form=JoinTeamForm, user_team_id=user_team_id)

def handle_join_team(team_id):
    user = get_logged_in_user()
    if not user:
        return redirect(url_for('login'))
    dbHandler.update_user_team(user['username'], team_id)
    flash("You have joined the team!", "success")
    return redirect(url_for('search_team'))

def handle_create_team(teamForm):
    user = get_logged_in_user()
    if not user:
        return redirect(url_for('login'))
    if not user or user.get('role') != 'Coach':
        return redirect(url_for('index'))
    if teamForm.validate_on_submit():
        sanitized_data = sanitize_data({
            "name": teamForm.team_name.data,
            "description": teamForm.team_description.data
        })
        try:
            response = requests.post("http://127.0.0.1:3000/api/create_team", json=sanitized_data, headers=app_header, timeout=5)
            if response.status_code == 201:
                app_log.info("Team '%s' created successfully", teamForm.team_name.data)
                flash('Team created successfully!', 'success')
                return redirect(url_for('search_team'))
            elif response.status_code == 400:
                # Team name already exists
                error_msg = response.json().get("message", "An error occurred during team creation.")
                flash(error_msg, 'danger')
                app_log.warning("Failed team creation attempt: %s - %s", teamForm.team_name.data, error_msg)
            else:
                flash('An error occurred during team creation. Please try again.', 'danger')
                app_log.warning("Failed team creation attempt: %s", teamForm.team_name.data)
            if response.status_code not in (201, 400):
                response.raise_for_status()
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
    user = user_in_team(team_id)
    if not user:
        return redirect(url_for('index'))
    team = dbHandler.get_team_by_id(team_id)
    if not team:
        flash("Team not found.", "danger")
        return redirect(url_for('index'))
    return render_template('teamDetail.html', team=team, team_id=team_id, team_nav=True)

def handle_team_events(team_id):
    team = dbHandler.get_team_by_id(team_id)
    upcoming_events = dbHandler.get_upcoming_team_events(team_id)
    past_events = dbHandler.get_past_team_events(team_id)

    # delete + attendance forms for each event
    delete_forms = {event['id']: DeleteEventForm() for event in upcoming_events + past_events}
    attendance_forms = {event['id']: AttendanceForm() for event in upcoming_events}

    # attendance counts + username for each event
    attendance_counts = {}
    attendance_usernames = {}
    user_attendance = {}
    for event in upcoming_events + past_events:
        attendance_counts[event['id']] = dbHandler.get_event_attendance_counts(event['id'])
        attendance_usernames[event['id']] = dbHandler.categorize_attendance(event['id'], team['id'])

    if 'username' in session:
        user = dbHandler.retrieveUserByUsername(session['username'])
        if user:
            for event in upcoming_events + past_events:
                status = dbHandler.get_event_attendance(event['id'], user['id'])
                user_attendance[event['id']] = status
    
    return render_template('teamEvents.html', team=team, upcoming_events=upcoming_events, past_events=past_events, 
    team_nav=True, delete_forms=delete_forms, attendance_forms=attendance_forms, attendance_counts=attendance_counts, 
    user_attendance=user_attendance, attendance_usernames=attendance_usernames)

def handle_create_team_event(team_id, form):
    user = require_role('Coach')
    if not user:
        return redirect(url_for('team_detail', team_id=team_id))
    team = dbHandler.get_team_by_id(team_id)
    if not team:
        flash("Team not found.", "danger")
        return redirect(url_for('index'))
    if form.validate_on_submit():
        event_data = {
            "team_id": team_id,
            "title": form.title.data,
            "description": form.description.data,
            "event_date": form.event_date.data.strftime('%Y-%m-%dT%H:%M'),
            "location": form.location.data,
            "recurrence": form.recurrence.data,
            "recurrence_end": form.recurrence_end.data.strftime('%Y-%m-%d') if form.recurrence_end.data != "none" else None
        }
        try:
            response = requests.post("http://127.0.0.1:3000/api/create_team_event",json=event_data,headers=app_header, timeout=5)
            response.raise_for_status()
            if response.status_code == 201:
                flash("Event created successfully!", "success")
                return redirect(url_for('team_events', team_id=team_id))
            else:
                flash("Failed to create event. Please try again.", "danger")
                app_log.warning("Failed to create team event: %s", response.text)
        except requests.exceptions.RequestException as e:
            flash("An error occurred while creating the event.", "danger")
            app_log.error("Error during team event creation: %s", str(e))
    return render_template('createTeamEvent.html', form=form, team=team, team_nav=True)

def handle_delete_team_event (team_id, event_id):
    user = require_role('Coach')
    if not user:
        return redirect(url_for('team_detail', team_id=team_id))
    dbHandler.delete_team_event(event_id)
    flash("Event deleted successfully!", "success")
    return redirect(url_for('team_events', team_id=team_id))

def handle_event_attendance (team_id, event_id):
    user = require_role('Player')
    if not user:
        return redirect(url_for('team_events', team_id=team_id))
    form = AttendanceForm()
    if form.validate_on_submit():
        dbHandler.set_event_attendance(event_id, user['id'], form.status.data)
        flash("Your attendance has been recorded.", "success")
        return redirect(url_for('team_events', team_id=team_id))
    #pre-fill form if already responded
    current_status = dbHandler.get_event_attendance(event_id, user['id'])
    if current_status:
        form.status.data = current_status
    return redirect(url_for('team_events', team_id=team_id))

def handle_team_messages(team_id):
    user = user_in_team(team_id)
    if not user:
        return redirect(url_for('index'))
    team = dbHandler.get_team_by_id(team_id)
    team_name = team.get('name')
    # chat sidebar
    all_users = dbHandler.get_all_usernames_in_team(team_id)
    current_user = session['username']
    dm_users = [user for user in all_users if user != current_user]
    return render_template('teamMessages.html', team=team, team_nav=True, team_id=team_id, 
    team_name=team_name, dm_users=dm_users)