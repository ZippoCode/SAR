import uuid
from flask_restful import Resource, request

from app.flask_app import api
from app.models.models import ArtistModel


class Artist(Resource):
    def get(self):
        artists = ArtistModel.query().order(-ArtistModel.num_search).fetch(5)
        if not artists:
            return {'Error 404': 'Artists not found.'}, 404
        artists_list = list()
        for a in artists:
            artists_list.append({'artist': a.name, 's_num': a.num_search})
        return artists_list


class ArtistsPOST(Resource):

    def post(self):
        body = request.get_json()
        if ArtistModel.query(ArtistModel.name == body['artist']).get():
            return {'Error 409': 'An artist with the same name is already stored in the database.'}, 409
        id_artist = id = str(uuid.uuid1())
        name_artist = body['artist']
        num_search_artist = body['s_num']
        artist = ArtistModel(id=id_artist, name=name_artist, num_search=num_search_artist)
        artist.put()
        return {'id': id_artist}


class ArtistsGET(Resource):

    def get(self, id):
        artist = ArtistModel.query(ArtistModel.id == id).get()
        if not artist:
            return {'Error 404': 'The artist does not exist'}, 404
        return {'artist': artist.name, 's_num': artist.num_search}


api.add_resource(Artist, '/api/1/artist')
api.add_resource(ArtistsPOST, '/api/1/artists')
api.add_resource(ArtistsGET, '/api/1/artists/<string:id>')
