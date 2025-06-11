from flask_socketio import join_room, leave_room, send
from flask import request, session
import databaseManagement as dbHandler
from sanitize import sanitize_input
from flask_wtf.csrf import validate_csrf, ValidationError
from teamHandlers import user_in_team
from datetime import datetime
from zoneinfo import ZoneInfo

def register_socketio_events(socketio, app_log):
    print("Registering SocketIO events...")
    @socketio.on('join')
    def on_join(data):
        # team messaging
        team_id = data['team_id']
        user = user_in_team(team_id)
        #authentication handling
        if not user:
            print("User not in team or not logged in.")
            return False
        username = user['username']
        room = data['room']
        join_room(room)
        if room.startswith("team_"):
            previous_messages = dbHandler.get_team_messages(team_id)
            for msg in previous_messages:
                send(msg, to=request.sid)
        app_log.info(f"{username} has joined the room {room}")
    
    @socketio.on('leave')
    def on_leave(data):
        team_id = data['team_id']
        user = user_in_team(team_id)
        if not user:
            return False
        username = user['username']
        room = data['room']
        leave_room(room)
        #send({"name": username, "message": f"{username} has left the room."}, to=room)
        app_log.info(f"{username} has left the room {room}")

    @socketio.on('send_message')
    def handle_message(data):
        #csrf validation
        try:
            validate_csrf(data.get('csrf_token'))
        except ValidationError:
            return False
        # authentication handling
        team_id = data['team_id']
        user = user_in_team(team_id)
        if not user:
            return False
        # get user info
        username = user['username']
        room = data['room']
        time = datetime.now(ZoneInfo("Australia/Sydney")).strftime("%Y-%m-%d %H:%M")
        message_text = sanitize_input(data['message'])
        # save to DB for team chat
        if room.startswith("team_"):
            dbHandler.save_team_messages(team_id, username, message_text, time)
        content = {"name": username, "message": message_text, "timestamp": time}
        send(content, to=room)
    
    @socketio.on('join_dm')
    def on_join_dm(data):
        user1 = data['user1']
        user2 = data['user2']
        #sort usernames to ensure room name is consistent
        room = f"dm_{'_'.join(sorted([user1, user2]))}"
        join_room(room)
        previous_messages = dbHandler.get_private_messages(user1, user2)
        for msg in previous_messages:
            socketio.emit("private_message", msg, to=request.sid)
    
    @socketio.on('send_private_message')
    def handle_private_message(data):
        try:
            validate_csrf(data.get('csrf_token'))
        except ValidationError:
            return False
        sender = session.get('username')
        if not sender:
            return False  # Not authenticated
        recipient = data['recipient']
        time = datetime.now(ZoneInfo("Australia/Sydney")).strftime("%Y-%m-%d %H:%M")
        message = sanitize_input(data['message'])
        room = f"dm_{'_'.join(sorted([sender, recipient]))}"
        dbHandler.save_private_message(sender, recipient, message, time)
        socketio.emit("private_message", {"name": sender, "message": message, "timestamp": time}, to=room)