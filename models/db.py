# encoding=utf8

import torndb
import MySQLdb
from etc.config import DB_CONFIG

_db = torndb.Connection(
        DB_CONFIG['host'],
        DB_CONFIG['db_name'],
        DB_CONFIG['user'],
        DB_CONFIG['password'])


def add_note(user, note):
    SQL = '''INSERT INTO worknotes(`username`, `category`, `content`, `cost`)
             VALUES(%s, %s, %s, %s)
          '''
    if not execute(SQL, user, note['category'], note['content'], note['cost']):
        return False

    return True

def _reconnect():
    _db = torndb.Connection(
            Database.HOST,
            Database.DB_NAME,
            Database.USER,
            Database.PASSWORD)
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
