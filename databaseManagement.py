import sqlite3 as sql

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