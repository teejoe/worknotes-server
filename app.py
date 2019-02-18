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

    return render_template('index.html')

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

if __name__ == "__main__":
    app.run()
