# -*- encoding: utf8 -*-

from flask import Flask, render_template, request
from models.Guestbook import Guestbook, Greeting, guestbook_key
import logging
import time

app = Flask(__name__)
app.config.from_object(__name__)
app.debug = True
DEBUG = True


@app.route('/', methods=['GET', 'POST'])
def home():
    message = ''
    if request.method == 'POST':
        new_guestbook = Guestbook()
        new_guestbook.name = request.form['guestbook_title']

        guestbooks_query = Guestbook.query(Guestbook.name == new_guestbook.name)

        if len(guestbooks_query.fetch()) > 0:
            message = 'Error: Guest already exists'
        else:
            new_guestbook.put()
            print(new_guestbook)

    time.sleep(1)

    guestbooks_query = Guestbook.query()
    guestbooks = guestbooks_query.fetch()
    logging.info(guestbooks)

    return render_template('guestbook.html', guestbooks=guestbooks, message=message)


@app.route('/guestbook/<gbid>', methods=['GET', 'POST'])
def greetings(gbid):
    if request.method == 'POST':
        greeting = Greeting(parent=guestbook_key(gbid))
        greeting.content = request.form['content']
        greeting.put()
    guestbook = guestbook_key(gbid)
    greetings_query = Greeting.query(ancestor=guestbook).order(-Greeting.date)
    greetings = greetings_query.fetch(10)

    return render_template('greetings.html', guestbook=gbid, greetings=greetings)
