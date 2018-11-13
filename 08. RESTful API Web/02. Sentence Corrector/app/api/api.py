from flask_restful import Resource, reqparse, inputs

from app.flask_app import api
from app.models.models import Phrase, Frequent, Word

parser = reqparse.RequestParser(bundle_errors=True)
parser.add_argument('num', type=int, default=10, location=['args', 'json'])
parser.add_argument('order', type=inputs.boolean, default=True, location=['args', 'json'])
parser.add_argument('errors', type=str, action='append')


class Last(Resource):

    def get(self):
        """
            Restituisce la lista delle ultime dieci frasi con parole sbagliate

        :return:
        """
        phrase_query = Phrase.query().order(-Phrase.counter)
        phrase_list = list()
        for phrase in phrase_query.fetch(10):
            phrase_list.append({
                'Originale': phrase.original,
                'Suggerita': phrase.suggestion,
                'Numero Occorrenze': phrase.counter,
                'Data Creazione': str(phrase.created)
            })
        return {"Frasi": phrase_list}, 200


class Frequents(Resource):
    def get(self):
        """
            Restituisce le parole maggiormente sbagliate in ordine di frequenza. I
            paramentri 'num' e 'order' della query HTTP definiscono il numero di termini ritornati
            e se l'ordine e' crescente o decrescente.

        :return:
        """
        args = parser.parse_args()
        num = args.get('num')
        order = args.get('order')
        if order:
            frequent_query = Frequent.query().order(-Frequent.counter)
        else:
            frequent_query = Frequent.query().order(Frequent.counter)
        frequents_list = list()
        for frequent in frequent_query.fetch(num):
            frequents_list.append({
                'Parola': frequent.error,
                'Numero occorrenze': frequent.counter,
                'Data creazione': str(frequent.created),
                'Possibili correzioni': frequent.list_suggestion,
            })
        return {'Parole': frequents_list}, 200


class Words(Resource):
    def get(self, value):
        """
            Ritorna tutte le correzioni scelte in precedenza dagli utenti tramite
            l'interfaccia web per la parola selezionata

        :param word:
        :return:
        """
        word = Word.get_by_id(value.title())
        if not word:
            return {'Error': 'Parola non trovata'}, 404
        word_dict = {
            'Parola': word.correct,
            'Numero occorrenze': word.counter,
            'Errori associati': word.errors
        }
        return word_dict, 200

    def post(self, value):
        """
            Aggiunge una lista di errori noti per la parola indicata.
            In particolare, se la parola e' gia' presente incrementa il
            contatore. Successivamente aggiunge le parole errate associate
        :param word:
        :return:
        """
        word = Word.get_by_id(value.title())
        if not word:
            return {'Error': 'Parola non trovata'}, 404
        args = parser.parse_args()
        errors = args.get('errors')
        for error in errors:
            error = error.title()
            if len(error.split()) < 2 and error not in word.errors:
                word.errors.append(error.title())
        word.counter = word.counter + 1
        word.put()
        word_dict = {
            'Parola Corretta': word.correct,
            'Numero occorrenze': word.counter,
            'Parole errate associate': word.errors
        }
        return word_dict


api.add_resource(Last, '/api/corrections/last')
api.add_resource(Frequents, '/api/corrections/frequents')
api.add_resource(Words, '/api/correct/<string:value>')
