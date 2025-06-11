import threading
from flask import session
from contextlib import nullcontext

# Global dictionary to store locks
session_locks = {}

# Function to get or create a lock for a session
def get_session_lock(session_id):
    if session_id not in session_locks:
        session_locks[session_id] = threading.Lock()
    return session_locks[session_id]

# Cleanup function to remove the lock when the session is deleted
def cleanup_session_lock(response):
    session_id = session.get('_id', None)
    if session_id and session_id in session_locks:
        del session_locks[session_id]
    return response


def acquire_session_lock():
    session_id = session.get('_id', None)
    if session_id is None:
        return nullcontext()  # Acts as a no-op context manager
    lock = get_session_lock(session_id)
    return lock