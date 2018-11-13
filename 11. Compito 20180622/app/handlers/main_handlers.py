from flask import render_template

from app.flask_app import app
from app.models.models import Sondaggio


@app.route('/', methods=['GET', 'POST'])
def main():
    sondaggio_list = Sondaggio.query().fetch()
    return render_template('list.html', value_list=sondaggio_list)

@app.route('/show_details/<string:value>', methods=['GET'])
def show_details(value):
    sondaggio = Sondaggio.get_by_id(value)
    totale = sondaggio.positivi + sondaggio.negativi + sondaggio.astenuti
    return render_template("show_details.html", sondaggio=sondaggio, totale=totale)


@app.errorhandler(404)
def handle_bad_request(error):
    return render_template('page_not_found.html'), 400
