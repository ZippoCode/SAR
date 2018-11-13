import unirest
import re
import string
import random
from app_secrets import mashape_key


regex = re.compile('[%s]' % re.escape(string.punctuation))

DEFAULT_KEY = "https://montanaflynn-spellcheck.p.mashape.com/check/?text="


def get_dict_spellcheck(text):
    """
    Effettua una GET sulle API si Spellcheck. Restituisce un dizionario che contiene:
        - La frase originale
        - La frase suggerita
        - Un dizionario che contiene la coppia 'Parola errata' : 'Lista di correzioni'
        - La lista delle possibili frasi corrette
    In particolare, le frasi vengono 'pulite' dalla punteggiatura
    :param text:
    :return: dict
    """
    # Pulizia testo
    text = "%s%s" % (text[0].upper(), text[1:].lower())
    text = regex.sub(' ', text)
    text = re.sub(' +', ' ', text)
    response = unirest.get(DEFAULT_KEY + text,
                           headers={
                               "X-Mashape-Key": mashape_key,
                               "Accept": "application/json"
                           })
    if response.code != 200:
        return None
    original = response.body['original']
    suggestion = response.body['suggestion']

    # Costruzione del Dizionario
    dict_corrections = {}
    response_corrections = response.body['corrections']
    phrase_suggestion = list()
    for word_original in response_corrections:
        list_word_corrections = list()
        for correction in response_corrections[word_original]:
            list_word_corrections.append(correction.title())
            phrase_suggestion.append(original.replace(word_original, correction.upper()))
        dict_corrections[word_original.title()] = list_word_corrections

    # Costruzione della frase suggerita con le parole modificate
    original_correct = original
    for wo, ws in zip(original_correct.split(), suggestion.split()):
        if wo != ws:
            original_correct = original_correct.replace(wo, ws.upper())
    phrase_suggestion.append(original_correct)

    random.shuffle(phrase_suggestion)

    response_dict = {
        "Original": original,
        "Suggestion": suggestion,
        'Phrase Suggestion': phrase_suggestion,
        "Corrections": dict_corrections
    }
    return response_dict
