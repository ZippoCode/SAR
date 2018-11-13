from flask import render_template

from app.flask_app import app
from app.models.models import Phrase, Frequent


@app.route('/show/<string:type>/<string:value>', methods=['GET'])
def show(type, value):
    if type == 'phrase':
        phrase = Phrase.get_by_id(value)
        return render_template("show_details.html", type='phrase', value=phrase)
    else:
        frequent = Frequent.get_by_id(value)
        return render_template("show_details.html", type='frequent', value=frequent)
