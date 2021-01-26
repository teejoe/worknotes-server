# encoding=utf8
from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta, MO
from dateutil import tz
import db

def update_note(note):
    return db.update_note(note)

def delete_note(username, note_id):
    return db.delete_note(username, note_id)

def add_note(username, note):
    return db.add_note(username, note)

def get_note(note_id):
    return db.get_note(note_id)

def get_all_notes(username):
    end_time = datetime.now()
    start_time = end_time - timedelta(days=365)
    notes = db.get_notes(username, start_time, end_time)
    for note in notes:
        note['title'] = note['content'].partition('\n')[0]
        note['desc'] = '\n'.join(note['content'][:200].split('\n')[0:6])
        note['time'] = note['time'].replace(
            tzinfo=tz.gettz('UTC')
        ).astimezone(tz.tzlocal()).strftime("%Y-%m-%d %H:%M:%S")
    return notes


def search_notes(username, keyword):
    notes = db.search_notes(username, keyword)
    for note in notes:
        note['title'] = note['content'].partition('\n')[0]
        note['desc'] = '\n'.join(note['content'][:200].split('\n')[0:6])
        note['time'] = note['time'].replace(
            tzinfo=tz.gettz('UTC')
        ).astimezone(tz.tzlocal()).strftime("%Y-%m-%d %H:%M:%S")
    return notes


def update_worknote(note):
    return db.update_worknote(note)


def delete_worknote(username, note_id):
    return db.delete_worknote(username, note_id)


def add_user_worknote(username, note):
    return db.add_worknote(username, note)


def get_all_worknotes(username):
    end_time = datetime.now()
    start_time = end_time - timedelta(days=60)
    notes = db.get_worknotes(username, start_time, end_time)
    for note in notes:
        note['time'] = note['time'].replace(
            tzinfo=tz.gettz('UTC')
        ).astimezone(tz.tzlocal()).strftime("%Y-%m-%d %H:%M:%S")
    return notes


def search_work_notes(username, keyword):
    notes = db.search_worknotes(username, keyword)
    for note in notes:
        note['time'] = note['time'].replace(
            tzinfo=tz.gettz('UTC')
        ).astimezone(tz.tzlocal()).strftime("%Y-%m-%d %H:%M:%S")
    return notes


def get_weekly_report(username):
    start_time, end_time = get_last_week()
    notes = db.get_worknotes(username, start_time, end_time)
    notes = sorted(notes, key=lambda k: k['category'])
    report = "%s ~ %s<br><br>" % (start_time, end_time)
    if len(notes) == 0:
        return report

    category = notes[0]['category']
    report += "%s<br>================<br>" % category
    for n in notes:
        if category != n['category']:
            category = n['category']
            report += "<br>%s<br>================<br>" % category
        report += "+ %s<br>" % n['content']

    return report


def get_monthly_report(username):
    start_time, end_time = get_last_month()
    return get_work_report(username, start_time, end_time)


def get_yearly_report(username):
    start_time, end_time = get_last_year()
    return get_work_report(username, start_time, end_time)


def get_this_week_report(username):
    start_time, end_time = get_this_week()
    return get_work_report(username, start_time, end_time)


def get_work_report(username, start_time, end_time):
    notes = db.get_worknotes(username, start_time, end_time)
    notes = sorted(notes, key=lambda k: k['category'])
    report = u"%s ~ %s<br><br>" % (start_time, end_time)
    if len(notes) == 0:
        return report

    category = notes[0]['category']
    report += u"%s<br>================<br>" % category
    total_cost = 0
    for n in notes:
        if category != n['category']:
            category = n['category']
            report += u"<br>%s<br>================<br>" % category
        report += u"+ %s (%g天)<br>" % (n['content'], n['cost'])
        total_cost += n['cost']
    report += u"<br>总计: %g 天<br>" % total_cost
    return report


def get_last_week():
    today = date.today()
    last_monday = today + relativedelta(weekday=MO(-2))
    last_monday = datetime.combine(last_monday, datetime.min.time())
    last_sunday = last_monday + timedelta(days=7)
    return last_monday, last_sunday


def get_this_week():
    today = date.today()
    monday = today + relativedelta(weekday=MO(-1))
    monday = datetime.combine(monday, datetime.min.time())
    return monday, datetime.now()


def get_last_month():
    end_time = date.today() + timedelta(days=1)
    start_time = end_time + relativedelta(months=-1)
    #start_time = datetime.strptime('01/08/20 00:00:00', '%m/%d/%y %H:%M:%S')
    start_time = datetime.combine(start_time, datetime.min.time())
    end_time = datetime.combine(end_time, datetime.min.time())
    return start_time, end_time


def get_last_year():
    end_time = date.today()
    start_time = end_time + relativedelta(years=-1)
    start_time = datetime.combine(start_time, datetime.min.time())
    end_time = datetime.combine(end_time, datetime.min.time())
    return start_time, end_time
