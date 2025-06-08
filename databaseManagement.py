# This file contains functions to manage the database operations for the volleyball team application.

import sqlite3 as sql
from datetime import datetime

db_path = "./databaseFiles/database.db"

def insertUser(username, hashed_password, totp_secret, email, full_name, role):
    con = sql.connect(db_path)
    cur = con.cursor()
    # Check if the username already exists
    cur.execute("SELECT COUNT(*) FROM secure_users_9f WHERE username = ?", (username,))
    if cur.fetchone()[0] > 0:
        con.close()
        raise Exception("Username already exists")
    cur.execute(
        "INSERT INTO secure_users_9f (username, password, totp_secret, role, email, full_name) VALUES (?, ?, ?, ?, ?, ?)",  
        (username, hashed_password, totp_secret, role, email, full_name),   
    )
    con.commit()
    con.close()

def retrieveUserByUsername(username):
    conn = sql.connect(db_path)
    cur = conn.cursor()
    cur.execute(
        "SELECT * FROM secure_users_9f WHERE username = ?",
        (username,)
    )
    user = cur.fetchone()
    conn.close()
    if user:
        return {
            'id': user[0],
            'username': user[1],
            'password': user[2],
            'email': user[3],
            'full_name': user[4],
            'role': user[5],
            'team_id': user[6],
            'totp_secret': user[7],
            'twofa_enabled': user[8],
        }
    return None

def updateUserTotpSecret(username, totp_secret):
    conn = sql.connect(db_path)
    cur = conn.cursor()
    cur.execute(
        "UPDATE secure_users_9f SET totp_secret = ? WHERE username = ?",
        (totp_secret, username)
    )
    conn.commit()
    conn.close()

def setTwoFAEnabled(username, enabled=True):
    conn = sql.connect(db_path)
    conn.execute(
        "UPDATE secure_users_9f SET twofa_enabled = ? WHERE username = ?",
        (1 if enabled else 0, username)
    )
    conn.commit()
    conn.close()

def get_all_teams():
    conn = sql.connect(db_path)
    cur = conn.cursor()
    cur.execute("SELECT id, name, description, created_at FROM volleyball_teams")
    teams = [
        {
            "id": row[0],
            "name": row[1],
            "description": row[2],
            "created_at": row[3]
        }
        for row in cur.fetchall()
    ]
    conn.close()
    return teams

def get_team_by_id(team_id):
    conn = sql.connect(db_path)
    cur = conn.cursor()
    cur.execute("SELECT id, name, description, created_at FROM volleyball_teams WHERE id = ?", (team_id,))
    row = cur.fetchone()
    conn.close()
    if row:
        return {
            "id": row[0],
            "name": row[1],
            "description": row[2],
            "created_at": row[3]
        }
    return None

def search_teams_by_name(query):
    conn = sql.connect(db_path)
    cur = conn.cursor()
    cur.execute("SELECT id, name, description, created_at FROM volleyball_teams WHERE name LIKE ?", ('%' + query + '%',))
    teams = [
        {
            "id": row[0],
            "name": row[1],
            "description": row[2],
            "created_at": row[3]
        }
        for row in cur.fetchall()
    ]
    conn.close()
    return teams

def update_user_team(username, team_id):
    conn = sql.connect(db_path)
    cur = conn.cursor()
    cur.execute("UPDATE secure_users_9f SET team_id = ? WHERE username = ?", (team_id, username))
    conn.commit()
    conn.close()

def create_team(name, description):
    conn = sql.connect(db_path)
    cur = conn.cursor()
    cur.execute("INSERT INTO volleyball_teams (name, description) VALUES (?, ?)", (name, description))
    conn.commit()
    conn.close()

def create_team_event(team_id, title, description, event_date, location):
    conn = sql.connect(db_path)
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO team_events (team_id, title, description, event_date, location) VALUES (?, ?, ?, ?, ?)",
        (team_id, title, description, event_date, location)
    )
    conn.commit()
    conn.close()

def get_upcoming_team_events(team_id):
    conn = sql.connect(db_path)
    cur = conn.cursor()
    now = datetime.now().strftime("%Y-%m-%dT%H:%M")
    cur.execute(
        "SELECT id, title, description, event_date, location FROM team_events WHERE team_id = ? AND event_date >= ? ORDER BY event_date ASC",
        (team_id, now)
    )
    events = []
    for row in cur.fetchall():
        try:
            event_date = datetime.strptime(row[3], "%Y-%m-%dT%H:%M")
            formatted_date = event_date.strftime("%A, %d %B %Y at %I:%M %p")
        except Exception:
            formatted_date = row[3]
        events.append({
            "id": row[0],
            "title": row[1],
            "description": row[2],
            "event_date": formatted_date,
            "location": row[4]
        })
    conn.close()
    return events

def get_past_team_events(team_id):
    conn = sql.connect(db_path)
    cur = conn.cursor()
    now = datetime.now().strftime("%Y-%m-%dT%H:%M")
    cur.execute(
        "SELECT id, title, description, event_date, location FROM team_events WHERE team_id = ? AND event_date < ? ORDER BY event_date DESC",
        (team_id, now)
    )
    events = []
    for row in cur.fetchall():
        try:
            event_date = datetime.strptime(row[3], "%Y-%m-%dT%H:%M")
            formatted_date = event_date.strftime("%A, %d %B %Y at %I:%M %p")
        except Exception:
            formatted_date = row[3]
        events.append({
            "id": row[0],
            "title": row[1],
            "description": row[2],
            "event_date": formatted_date,
            "location": row[4]
        })
    conn.close()
    return events

def delete_team_event(event_id):
    conn = sql.connect(db_path)
    cur = conn.cursor()
    cur.execute("DELETE FROM team_events WHERE id = ?", (event_id,))
    conn.commit()
    conn.close()

def set_event_attendance (event_id, user_id, status):
    conn = sql.connect(db_path)
    cur = conn.cursor()
    # inserts a new attendance record or updates the existing one by using ON CONFLICT
    cur.execute("""
        INSERT INTO event_attendance (event_id, user_id, status)
        VALUES (?, ?, ?)
        ON CONFLICT(event_id, user_id) DO UPDATE SET status=excluded.status, responded_at=CURRENT_TIMESTAMP
    """, (event_id, user_id, status))
    conn.commit()
    conn.close()

def get_event_attendance (event_id, user_id):
    conn = sql.connect(db_path)
    cur = conn.cursor()
    cur.execute("SELECT status FROM event_attendance WHERE event_id = ? AND user_id = ?", (event_id, user_id))
    row = cur.fetchone()
    conn.close()
    return row[0] if row else None

def get_event_attendance_counts(event_id):
    conn = sql.connect(db_path)
    cur = conn.cursor()
    cur.execute("""
        SELECT status, COUNT(*) FROM event_attendance
        WHERE event_id = ?
        GROUP BY status
    """, (event_id,))
    counts = {row[0]: row[1] for row in cur.fetchall()}
    conn.close()
    # Ensure both keys exist 
    return {
        'attending': counts.get('attending', 0),
        'not_attending': counts.get('not_attending', 0)
    }

def get_team_members(team_id):
    conn = sql.connect(db_path)
    cur = conn.cursor()
    cur.execute("SELECT id, username FROM secure_users_9f WHERE team_id = ? AND role != 'Coach'", (team_id,))
    members = cur.fetchall() 
    conn.close()
    return members

def get_all_usernames_in_team(team_id):
    conn = sql.connect(db_path)
    cur = conn.cursor()
    cur.execute("SELECT username FROM secure_users_9f WHERE team_id = ?", (team_id,))
    members = [row[0] for row in cur.fetchall()]
    conn.close()
    return members

def get_event_responses(event_id):
    conn = sql.connect(db_path)
    cur = conn.cursor()
    cur.execute("SELECT user_id, status FROM event_attendance WHERE event_id = ?", (event_id,))
    responses = cur.fetchall() 
    conn.close()
    return responses

def categorize_attendance(event_id, team_id):
    members = get_team_members(team_id) 
    responses = dict(get_event_responses(event_id)) 
    attending = []
    not_attending = []
    not_responded = []
    for user_id, username in members:
        status = responses.get(user_id)
        if status == 'attending':
            attending.append(username)
        elif status == 'not_attending':
            not_attending.append(username)
        else:
            not_responded.append(username)
    return {
        'attending': attending,
        'not_attending': not_attending,
        'not_responded': not_responded
    }

def save_team_messages (team_id, username, message, timestamp):
    conn = sql.connect(db_path)
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO team_messages (team_id, username, message, timestamp) VALUES (?,?,?,?)", 
        (team_id, username, message, timestamp)
                )
    conn.commit()
    conn.close()

def get_team_messages(team_id, limit=50):
    conn = sql.connect(db_path)
    cur = conn.cursor()
    cur.execute("SELECT username, message, timestamp FROM team_messages WHERE team_id = ? ORDER by timestamp DESC LIMIT ?",
                (team_id, limit)
                )
    messages = [
        {"name": row[0], "message": row[1], "timestamp": row[2]}
        for row in cur.fetchall()
    ]
    conn.close()
    return list(reversed(messages))  # Oldest first

def save_private_message(sender, recipient, message, timestamp):
    conn = sql.connect(db_path)
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO private_messages (sender, recipient, message, timestamp) VALUES (?, ?, ?, ?)", 
        (sender, recipient, message, timestamp)
    )
    conn.commit()
    conn.close()

def get_private_messages(user1, user2, limit=50):
    conn = sql.connect(db_path)
    cur = conn.cursor()
    cur.execute("""
        SELECT sender, message, timestamp FROM private_messages
        WHERE (sender = ? AND recipient = ?) OR (sender = ? AND recipient = ?)
        ORDER BY timestamp DESC LIMIT ?
    """, (user1, user2, user2, user1, limit))
    messages = [
        {"name": row[0], "message": row[1], "timestamp": row[2]}
        for row in cur.fetchall()
    ]
    conn.close()
    return list(reversed(messages))