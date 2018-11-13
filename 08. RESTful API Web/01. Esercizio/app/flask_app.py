# -*- Encoding: UTF-8 -*-

import appengine_config
import logging
from flask import Flask, url_for, render_template
from flask_wtf import CSRFProtect
from flask_restful import Api

app = Flask(__name__)
app.config.from_object(__name__)
csrf = CSRFProtect(app)
api = Api(app, decorators=[csrf.exempt])

# Setting the secret key
if appengine_config.GAE_DEV:
    logging.warning("Using a dummy secret key")
    app.secret_key = "my-secret-key"
    app.debug = True
else:
    from app import app_config

    app.secret_key = app_config.secret_key


@app.route('/')
def main():
    handlers = [
        ('Get Color', url_for('apicolorlist')),
    ]
    return render_template('list.html', handlers=handlers)

@app.errorhandler(404)
def page_not_found(error):
    return "Sorry. But this page does not exit", 404
