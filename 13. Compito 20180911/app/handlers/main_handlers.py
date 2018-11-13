from flask import render_template, json, session, redirect, url_for
from google.appengine.api import urlfetch

from app.flask_app import app
from app.models.models import Sala
from forms import FrontEnd
from app_secrets import api_key

url_omdb = "http://www.omdbapi.com/?apikey=" + api_key + "&"


@app.route('/', methods=['GET', 'POST'])
def main():
    frontEnd = FrontEnd()
    if frontEnd.validate_on_submit():
        sala = Sala.query(Sala.id_sala == frontEnd.sala.data, Sala.time == frontEnd.orario.data).get()
        for posto in sala.posti:
            if posto.disponibile:
                session['ID_SALA'] = frontEnd.sala.data
                session['ORARIO'] = frontEnd.orario.data
                session['IMDB_ID'] = frontEnd.id_film.data
                return redirect(url_for('show_details'))
        return 'Alcun Posto Disponibile'
    return render_template('list.html', form=frontEnd)


@app.route('/show_details', methods=['GET'])
def show_details():
    try:
        result = urlfetch.fetch(url_omdb + "i=" + session['IMDB_ID'] + "&r=json&plot=short")
        film = json.loads(result.content)
        details_film = {
            'Title': film['Title'],
            'Director': film['Director'],
            'Year': film['Year'],
            'Ranking': film['imdbRating'],
            'Img': film['Poster']
        }
    except urlfetch.Error:
        return "Servizio non disponibile", 500
    except KeyError:
        return "Film non presente", 404
    return render_template('show_song.html', film=details_film)


@app.errorhandler(404)
def handle_bad_request(error):
    return render_template('page_not_found.html'), 400
