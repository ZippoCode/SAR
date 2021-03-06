# -*- encoding UTF-8 -*-
from flask import Flask

app = Flask(__name__)
app.config.from_object(__name__)
DEBUG = True


@app.route('/', methods=['GET'])
def helloworld():
    return "Hello World!"
