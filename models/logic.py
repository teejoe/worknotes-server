# encoding=utf8
from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta, MO
import db

def add_user_note(username, note):
    return db.add_note(username, note)


def get_all_notes(username):
    return db.get_notes(username)


def get_weekly_report(username):
    start_time, end_time = get_last_week()
    notes = db.get_notes(username, start_time, end_time)
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
    notes = db.get_notes(username, start_time, end_time)
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
        report += u"+ %s (%g天)<br>" % (n['content'], total_cost)
        total_cost += n['cost']
    report += u"<br>总计: %g 天<br>" % total_cost

    return report


def get_last_week():
    today = date.today()
    last_monday = today + relativedelta(weekday=MO(-2))
    last_monday = datetime.combine(last_monday, datetime.min.time())
    last_sunday = last_monday + timedelta(days=7)
    return last_monday, last_sunday

def get_last_month():
    end_time = date.today() + timedelta(days=1)
    start_time = end_time + relativedelta(months=-1)
    start_time = datetime.combine(start_time, datetime.min.time())
    end_time = datetime.combine(end_time, datetime.min.time())
    return start_time, end_time

