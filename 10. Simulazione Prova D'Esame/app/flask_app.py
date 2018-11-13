import appengine_config
import logging

from flask import Flask
from flask_restful import Api
from flask_wtf import CSRFProtect

app = Flask(__name__)
app.config.from_object(__name__)
csrf_protect = CSRFProtect()
api = Api(app, decorators=[csrf_protect.exempt])

if appengine_config.GAE_DEV:
    logging.warning('Using a dummy secret key')
    app.secret_key = 'MyS3cr3tKey'
    app.debug = True
    DEBUG = True

else:
    import app_secrets

    app.secret_key = app_secrets.app_secret_key
