from flask import request, render_template, redirect, url_for, session

from app.flask_app import app
from app.util.spellcheck import get_dict_spellcheck


@app.route('/', methods=['POST', 'GET'])
def main():
    """
        Analizza la frase scritta dall'utente e aggiunge al DataStore i valori
        di: Phrase e Frequents - Frasi Sbagliate e Parole Sbagliate.
    :return:
    """
    if request.method == 'GET':
        return render_template('list.html')
    elif request.method == 'POST':
        text = request.form['phrase'].strip()
        dict_spellcheck = get_dict_spellcheck(text)
        if not dict_spellcheck:
            return render_template('list.html')
        original = dict_spellcheck['Original']
        suggestion = dict_spellcheck['Suggestion']
        dict_corrections = dict_spellcheck['Corrections']
        phrase_suggestion = dict_spellcheck['Phrase Suggestion']

        if original == suggestion:
            return render_template('list.html', message=original)

        session['Original'] = original
        session['Suggestion'] = suggestion
        session['Corrections'] = dict_corrections
        session['Phrase Suggestion'] = phrase_suggestion
        return redirect(url_for('selected_phrase'))


@app.errorhandler(404)
def error(error):
    return render_template('page_not_found.html'), 404
