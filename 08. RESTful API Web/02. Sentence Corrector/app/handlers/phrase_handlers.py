import logging

from flask import request, render_template, redirect, url_for, session
from app.flask_app import app

from app.models.models import Phrase, Frequent, Word


@app.route('/selected_phrase', methods=['POST', 'GET'])
def selected_phrase():
    """
        Se la richiesta e' di tipo 'GET' mostra salva le informazioni
        inerenti alla richiesta e mostra la scherma di scelta. Altrimenti
        invoca 'redirect' per permettere all'utente di selezionare all'utente una frase
        corretta

    :return:
    """
    if request.method == 'GET':
        original = session['Original']
        suggestion = session['Suggestion']
        dict_corrections = session['Corrections']
        phrase_suggestion = session['Phrase Suggestion']

        phrase = Phrase.get_by_id(original)
        if phrase:
            phrase.counter = phrase.counter + 1
        else:
            phrase = Phrase(id=original,
                            original=original,
                            suggestion=suggestion)
        phrase.put()

        for word in dict_corrections:
            frequent = Frequent.get_by_id(word)
            if frequent:
                frequent.counter = frequent.counter + 1
            else:
                frequent = Frequent(id=word, error=word.title())
            for word_correction in dict_corrections[word]:
                if word_correction not in frequent.list_suggestion:
                    frequent.list_suggestion.append(word_correction.title())
            frequent.put()
        return render_template('choosed_page.html', phrase=original, corrections=phrase_suggestion)
    elif request.method == 'POST':
        return redirect(url_for('choosed_correction'))


@app.route('/choosed_correction', methods=['POST', 'GET'])
def choosed_correction():
    """
        Modifica la phrase sbagliata con la correzione scelta e aggiorna
        la lista delle parole sbagliate con le correzioni scelte

    :param original:
    :return:
    """
    original = session['Original']
    selected = session['Suggestion']
    original = "%s%s" % (original[0].upper(), original[1:].lower())
    #selected = request.form.get('phrase_select')
    print(selected)
    phrase = Phrase.get_by_id(str(original))
    if phrase:
        phrase.suggestion = "%s%s" % (selected[0].upper(), selected[1:].lower())
        phrase.put()
    for correct, error in zip(selected.split(), original.split()):
        if correct != error:
            correct = correct.title()
            word = Word.get_by_id(correct)
            if not word:
                word = Word(id=correct,
                            correct=correct)
            else:
                word.counter = word.counter + 1
            if error not in word.errors:
                word.errors.append(error.title())
            word.put()

    return render_template('show_details.html', type='phrase', value=phrase)
