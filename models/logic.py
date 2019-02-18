import db

def add_user_note(username, note):
    return db.add_note(username, note)

