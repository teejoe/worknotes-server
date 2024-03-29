# encoding=utf8
from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta, MO
from dateutil import tz
import db

def update_todo(todo):
    return db.update_todo(todo)

def delete_todo(todo_id):
    return db.delete_todo(todo_id)

def add_todo(username, todo):
    return db.add_todo(username, todo)

def get_todolist(username):
    newlist = db.get_todolist(username, status="new")
    progresslist = db.get_todolist(username, status="inprogress")
    donelist = db.get_todolist(username, status="done")
    abortlist = db.get_todolist(username, status="abort")
    newlist.extend(progresslist)
    newlist.extend(donelist)
    newlist.extend(abortlist)
    for todo in newlist:
        todo['updatetime'] = todo['updatetime'].replace(
             tzinfo=tz.gettz('UTC')
             ).astimezone(tz.tzlocal()).strftime("%Y-%m-%d %H:%M:%S")
    return newlist
    #return db.get_todolist(username)

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
        note['time'] = note['updatetime'].replace(
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
        if not note['detail']:
            note['detail'] = ''
        note['time'] = note['time'].replace(
            tzinfo=tz.gettz('UTC')
        ).astimezone(tz.tzlocal()).strftime("%Y-%m-%d %H:%M:%S")
    return notes


def search_work_notes(username, keyword):
    notes = db.search_worknotes(username, keyword)
    for note in notes:
        if not note['detail']:
            note['detail'] = ''
        note['time'] = note['time'].replace(
            tzinfo=tz.gettz('UTC')
        ).astimezone(tz.tzlocal()).strftime("%Y-%m-%d %H:%M:%S")
    return notes


def get_weekly_report(username):
    start_time, end_time = get_last_week()
    notes = db.get_worknotes(username, start_time, end_time)
    notes = sorted(notes, key=lambda k: k['category'])
    report = "%s ~ %s\n\n" % (start_time, end_time)
    if len(notes) == 0:
        return report

    category = notes[0]['category']
    report += "%s\n================\n" % category
    for n in notes:
        if category != n['category']:
            category = n['category']
            report += "\n%s\n================\n" % category
        report += "+ %s\n" % n['content']
        items = [] if not n['detail'] else n['detail'].split('\n')
        for item in items:
            if item: report += "  - %s\n" % item
        #report += "\n"

    return report


def get_monthly_report(username):
    start_time, end_time = get_last_month()
    return get_work_report(username, start_time, end_time, True)


def get_yearly_report(username):
    start_time, end_time = get_last_year()
    return get_work_report(username, start_time, end_time)


def get_this_week_report(username):
    start_time, end_time = get_this_week()
    return get_work_report(username, start_time, end_time, True)


def get_work_report(username, start_time, end_time, showdetail=False):
    notes = db.get_worknotes(username, start_time, end_time)
    notes = sorted(notes, key=lambda k: k['category'])
    report = u"%s ~ %s\n\n" % (start_time, end_time)
    if len(notes) == 0:
        return report

    category = notes[0]['category']
    report += u"%s\n================\n" % category
    total_cost = 0
    for n in notes:
        total_cost += n['cost']
        if category != n['category']:
            category = n['category']
            report += u"\n%s\n================\n" % category
        report += u"+ %s (%g天)\n" % (n['content'], n['cost'])
        if showdetail:
            items = [] if not n['detail'] else n['detail'].split('\n')
            for item in items:
                if item: report += "  - %s\n" % item
            #report += "\n"
    report += u"\n总计: %g 天" % total_cost
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
