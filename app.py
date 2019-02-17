# coding=utf8

from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World! maotianjiao'

@app.route('/about')
def about():
    return 'The about page'

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/hello/')
@app.route('/hello/<name>')
def hello(name=None):
    return render_template('hello.html', name=name)
