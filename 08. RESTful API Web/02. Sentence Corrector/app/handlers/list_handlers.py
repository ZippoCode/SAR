from flask import render_template

from app.flask_app import app
from app.models.models import Phrase, Frequent


@app.route('/list_phrases', methods=['GET'])
def list_phrases():
    """
        Mostra la lista delle frasi ordinate dalle piu' frequenti

    :return:
    """
    phrase_query = Phrase.query().order(-Phrase.counter).fetch()
    phrase_list = list()
    for phrase in phrase_query:
        phrase_list.append(phrase.original)
    return render_template("view_list.html", list=phrase_list, type='phrase')


@app.route('/list_frequents', methods=['GET'])
def list_frequents():
    """
        Mostra la lista delle parole maggiormente sbagliate ordinate dalle
        piu' frequenti

    :return:
    """
    frequent_query = Frequent.query().order(-Frequent.counter).fetch()
    frequent_list = list()
    for frequent in frequent_query:
        frequent_list.append(frequent.error)
    return render_template("view_list.html", list=frequent_list, type='frequents')
