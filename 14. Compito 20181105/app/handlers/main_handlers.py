import unirest
from flask import render_template

from forms import SearchForm
from app.flask_app import app
from app_secrets import music_key

URL = "http://api.musixmatch.com/ws/1.1/track.search?q_artist={}&page_size=10&page=1&s_track_rating=desc"
URL_LYRICS = "http://api.musixmatch.com/ws/1.1/track.lyrics.get?track_id={}"


@app.route('/', methods=['GET', 'POST'])
def main():
    search = SearchForm()
    if search.validate_on_submit():
        result = unirest.get(url=URL.format(search.name_song.data),
                             params={'apikey': music_key},
                             headers={"Accept": "application/json"})
        result = (result.body)['message']
        list_songs = list()
        for t in (result['body'])['track_list']:
            track = t['track']
            song = {'track_name': track['track_name'],
                    'track_rating': track['track_rating'],
                    'album_name': track['album_name'],
                    'artist_name': track['artist_name'],
                    'album_coverart_100x100': track['album_coverart_100x100'],
                    'track_id': track['track_id']}
            list_songs.append(song)
        return render_template('list.html', list=list_songs)

    return render_template('main.html', form=search)


@app.route('/show_song/<string:lyrics_id>')
def show_song(lyrics_id):
    result = unirest.get(url=URL_LYRICS.format(lyrics_id),
                         params={'apikey': music_key},
                         headers={"Accept": "application/json"})
    lyrics = (((result.body['message'])['body'])['lyrics'])['lyrics_body']
    return render_template('show_song.html', lyrics=lyrics)


@app.errorhandler(404)
def handle_bad_request(error):
    return render_template('page_not_found.html'), 400
