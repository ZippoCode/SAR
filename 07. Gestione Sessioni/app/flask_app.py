# -*- encoding: UTF-8 -*-

import logging

from flask import Flask, url_for, render_template, request, make_response, session
from flask_wtf.csrf import CSRFProtect
import os

app = Flask(__name__)
app.config.from_object(__name__)
app.debug = True
DEBUG = True

# Protezione
csrf = CSRFProtect(app)
app.secret_key = os.urandom(32)


@app.route('/')
def main():
    handlers = [
        ('Set cookie', url_for('set_cookie')),
        ('Delete cookie', url_for('delete_cookie')),
        ('Insert in session', url_for('create_session')),
        ('Clear session', url_for('clear_session')),

    ]
    return render_template('home.html', handlers=handlers)


@app.route('/set-cookie')
def set_cookie():
    if not request.cookies:
        s = 'No cookies available'
    else:
        s = 'Actual cookies are {}'.format(str(request.cookies))
    r = make_response(s)
    if request.args:
        for k, v in request.args.items():
            r.set_cookie(k, v)
    logging.info("Cookies:" + str(request.cookies))
    return r


@app.route('/delete-cookie')
def delete_cookie():
    r = make_response("Cookie deleted!")
    for cookie in request.cookies:
        logging.info("Cookie deleted: " + cookie)
        r.set_cookie(cookie, '', expires=0)
    return r


@app.route('/create-session')
def create_session():
    if not request.cookies:
        s = 'No cookies available'
    else:
        s = 'Actual cookies are {}'.format(str(request.cookies))
    r = make_response(s)
    if request.args:
        for k, v in request.args.items():
            session[k] = v
    logging.info("Session created:" + str(request.cookies))
    print(app.secret_key)
    return r


@app.route('/clear-session')
def clear_session():
    session.clear()
    return ""
