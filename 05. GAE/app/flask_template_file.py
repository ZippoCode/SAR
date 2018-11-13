# -*- encoding: UTF-8 -*-

import logging
from flask import Flask, render_template, request

app = Flask(__name__)
app.config.from_object(__name__)
app.debug = True
DEBUG = True


@app.route('/greeting/<recipient>', methods=['GET', 'POST'])
def helloworld(recipient):
    app.logger.debug('Uri parameter: {}'.format(recipient))
    app.logger.debug('Uri query: {}'.format(request.args))
    app.logger.debug('Request payload: {}'.format(request.data))
    return render_template('greeting.html', recipient=recipient)
