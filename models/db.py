# encoding=utf8

import torndb
import MySQLdb
from utils.smartsql import QS, F, T, Condition
from etc.config import DB_CONFIG

_db = torndb.Connection(
        DB_CONFIG['host'],
        DB_CONFIG['db_name'],
        DB_CONFIG['user'],
        DB_CONFIG['password'])

def delete_note(username, note_id):
    sql, params = QS(T.notebook).where(F.id == note_id).delete()
    if not execute(sql, *params):
        return False
    return True


def update_note(note):
    sql, params = QS(T.notebook).where(
        F.id == note['id']
    ).update({
        'category': note['category'],
        'content': note['content'],
    })
    if not execute(sql, *params):
        return False
    return True


def add_note(username, note):
    sql, params = QS(T.notebook).insert({
        'username': username,
        'category': note['category'],
        'content': note['content'],
    })

    if not execute(sql, *params):
        return False

    return True

def get_note(note_id):
    cond = Condition('1 = 1')
    cond &= (F.id == note_id)
    sql, params = QS(T.notebook).where(cond).select_one()
    notes = query(sql, *params) 
    if len(notes) == 0:
        return None
    else:
        return notes[0]
    

def get_notes(username = None, start_time = None, end_time = None, category = None):
    cond = Condition('1 = 1')
    if username != None:
        cond &= (F.username == username)
    if start_time != None:
        cond &= (F.time >= start_time)
    if end_time != None:
        cond &= (F.time <= end_time)
    if category != None:
        cond &= (F.category == category)

    sql, params = QS(T.notebook).where(
        cond
    ).order_by(F.time, desc=True).select()
    return query(sql, *params)


def search_notes(username = None, keyword = None):
    cond = Condition('1 = 1')
    if username:
        cond &= (F.username == username)
    if keyword:
        keyword = '%' + keyword + '%'
        cond &= ((F.content % keyword) | (F.category % keyword))

    sql, params = QS(T.notebook).where(cond).order_by(F.time, desc=True).select()
    return query(sql, *params)

def search_worknotes(username = None, keyword = None):
    cond = Condition('1 = 1')
    if username:
        cond &= (F.username == username)
    if keyword:
        keyword = '%' + keyword + '%'
        cond &= ((F.content % keyword) | (F.category % keyword))

    sql, params = QS(T.worknotes).where(cond).order_by(F.time, desc=True).select()
    return query(sql, *params)


def delete_worknote(username, note_id):
    sql, params = QS(T.worknotes).where(F.id == note_id).delete()
    if not execute(sql, *params):
        return False
    return True


def update_worknote(note):
    sql, params = QS(T.worknotes).where(
        F.id == note['id']
    ).update({
        'category': note['category'],
        'content': note['content'],
        'cost': note['cost']
    })
    if not execute(sql, *params):
        return False
    return True


def add_worknote(username, note):
    sql, params = QS(T.worknotes).insert({
        'username': username,
        'category': note['category'],
        'content': note['content'],
        'cost': note['cost']
    })

    if not execute(sql, *params):
        return False

    return True

def get_worknotes(username = None, start_time = None, end_time = None, category = None):
    cond = Condition('1 = 1')
    if username != None:
        cond &= (F.username == username)
    if start_time != None:
        cond &= (F.time >= start_time)
    if end_time != None:
        cond &= (F.time <= end_time)
    if category != None:
        cond &= (F.category == category)

    sql, params = QS(T.worknotes).where(
        cond
    ).order_by(F.time, desc=True).select()
    return query(sql, *params)

def _reconnect():
    _db = torndb.Connection(
        DB_CONFIG['host'],
        DB_CONFIG['db_name'],
        DB_CONFIG['user'],
        DB_CONFIG['password'])

    return _db

def query(sql, *params):
    rows = None
    try:
        rows = _db.query(sql, *params)
    except:
        _reconnect()
        rows = _db.query(sql, *params)

    return rows

def execute(sql, *params):
    try:
        _db.execute(sql, *params)
    except (MySQLdb.OperationalError):
        _reconnect()
        _db.execute(sql, *params)
    except:
        return False
    return True
