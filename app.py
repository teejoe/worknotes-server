# encoding=utf8

from flask import Flask, request, render_template, make_response
from flask import session, redirect, url_for
from etc.config import *
from models import logic


app = Flask(__name__)
app.secret_key = SECRET_KEY

@app.route('/')
def home():
    if 'username' in session:
        return redirect(url_for('index'))

    return render_template('login.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    uname = request.form['username']
    pwd = request.form['password']
    for user in AUTH_USERS:
        if user['username'] == uname and user['password'] == pwd:
            session['username'] = uname
            return redirect(url_for('index'))

    return render_template('login.html', msg="invalid user")


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('home'))


@app.route('/index')
def index():
    if 'username' not in session:
        return redirect(url_for('home'))

    return render_template('index.html', categories=CATEGORIES)


@app.route('/addnote', methods=['GET', 'POST'])
def addnote():
    if 'username' not in session:
        return 'error'

    note = {}
    note['category'] = request.form['category']
    note['content'] = request.form['content']
    note['cost'] = float(request.form['cost'])
    logic.add_user_note(session['username'], note)
    return redirect(url_for('index'))


@app.route('/notelist', methods=['GET', 'POST'])
def notelist():
    if 'username' not in session:
        return redirect(url_for('home'))

    notes = logic.get_all_notes(session['username'])
    return render_template('notelist.html',
            notes=notes,
            categories=CATEGORIES)


@app.route('/notebook', methods=['GET', 'POST'])
def notebook():
    if 'username' not in session:
        return redirect(url_for('home'))

    notes = logic.get_all_notes(session['username'])
    return render_template('notebook.html',
            notes=notes,
            categories=CATEGORIES)


@app.route('/modifynote', methods=['POST'])
def modifynote():
    if 'username' not in session:
        return redirect(url_for('home'))
    note = {
        'id': request.form['note_id'],
        'category': request.form['category'],
        'content': request.form['content'],
        'cost': request.form['cost'],
    }
    if logic.update_note(note):
        return '{"code": 0}'
    else:
        return '{"code": -1}'


@app.route('/deletenote', methods=['GET', 'POST'])
def deletenote():
    if 'username' not in session or not request.args.get('note_id'):
        return '{"code": -1, "info": "param error"}'

    if logic.delete_note(session['username'], request.args['note_id']):
        return '{"code": 0}'
    else:
        return '{"code": -1}'


@app.route('/weeklyreport', methods=['GET', 'POST'])
def weeklyreport():
    if 'username' not in session:
        return redirect(url_for('home'))

    return logic.get_weekly_report(session['username'])


@app.route('/monthlyreport', methods=['GET', 'POST'])
def monthlyreport():
    if 'username' not in session:
        return redirect(url_for('home'))

    return logic.get_monthly_report(session['username'])


@app.route('/yearlyreport', methods=['GET', 'POST'])
def yearlyreport():
    if 'username' not in session:
        return redirect(url_for('home'))

    return logic.get_yearly_report(session['username'])


@app.route('/thisweekreport', methods=['GET', 'POST'])
def thisweekreport():
    if 'username' not in session:
        return redirect(url_for('home'))

    return logic.get_this_week_report(session['username'])


if __name__ == "__main__":
    app.run()
