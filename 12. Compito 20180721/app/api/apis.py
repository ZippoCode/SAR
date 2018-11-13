from flask_restful import Resource, request
from google.appengine.ext.db import BadValueError

from app.flask_app import api
from app.models.models import CityModel


class City(Resource):
    def get(self, city):
        city = CityModel.query(CityModel.name == city).fetch()
        if not city:
            return {'Error 404': 'City not found.'}, 404
        rules_list = list()
        for c in city:
            rules_list.append(c.zone)
        return {'zones': rules_list}


class Zone(Resource):
    def get(self, city, zone):
        city_gae = CityModel.query(CityModel.name == city, CityModel.zone == zone).get()
        if not city_gae:
            return {'Error 404': 'City or Zone not found.'}, 404
        return {'name': city_gae.rule, 'info': {'time': city_gae.time, 'intensity': city_gae.intensity}}

    def post(self, city, zone):
        if CityModel.query(CityModel.name == city, CityModel.zone == zone).get():
            return {'Error 409:': 'Zone with the given name already exists.'}, 409
        body = request.get_json()
        if not body:
            return {'Error:': 'Invalid inputs'}, 400
        try:
            for rule in body:
                name_rule = str(rule['name'])
                time = (rule['info'])['time']
                intensity = int((rule['info'])['intensity'])
                new_city = CityModel(name=city, zone=zone, rule=name_rule,
                                     time=time, intensity=intensity)
        except KeyError:
            return {'Error:': 'Invalid inputs'}, 400
        except BadValueError:
            return {'Error:': 'Invalid inputs'}, 400
        new_city.put()
        return {'Success': 'Zone created'}

    def put(self, city, zone):
        city_q = CityModel.query(CityModel.name == city, CityModel.zone == zone).get()
        if not city_q:
            return {'Error 404': 'City or Zone not exits.'}, 404
        body = request.get_json()
        if not body:
            return {'Error:': 'Invalid inputs'}, 400
        try:
            for rule in body:
                name_rule = str(rule['name'])
                time = (rule['info'])['time']
                intensity = int((rule['info'])['intensity'])
                city_q.rule = name_rule
                city_q.time = time
                city_q.intensity = intensity
        except KeyError:
            return {'Error:': 'Invalid inputs'}, 400
        except BadValueError:
            return {'Error:': 'Invalid inputs'}, 400
        city_q.put()
        return {'Success': 'Zone updated'}, 201


class Rule(Resource):
    def get(self, city, zone, rule):
        rule_q = CityModel.query(CityModel.name == city, CityModel.zone == zone,
                                 CityModel.rule == rule).get()
        if not rule_q:
            return {'Error 404': 'The rule does not exist.'}, 404
        return {'time': rule_q.time, 'intensity': rule_q.intensity}

    def post(self, city, zone, rule):
        if CityModel.query(CityModel.name == city, CityModel.zone == zone,
                           CityModel.rule == rule).get():
            return {'Error 409:': 'Rule with the given name already exists.'}, 409
        body = request.get_json()
        if not body:
            return {'Error:': 'Invalid inputs'}, 400
        try:
            time = body['time']
            intensity = int(body['intensity'])
            new_city = CityModel(name=city, zone=zone, rule=rule,
                                 time=time, intensity=intensity)
        except KeyError:
            return {'Error:': 'Invalid inputs'}, 400
        except BadValueError:
            return {'Error:': 'Invalid inputs'}, 400
        new_city.put()
        return {'Success': 'Rule created'}

    def put(self, city, zone, rule):
        rule_q = CityModel.query(CityModel.name == city, CityModel.zone == zone,
                                 CityModel.rule == rule).get()
        if not rule_q:
            return {'Error 404:': 'Rule does not exist.'}, 404
        body = request.get_json()
        if not body:
            return {'Error:': 'Invalid inputs'}, 400
        try:
            time = body['time']
            intensity = int(body['intensity'])
            rule_q.time = time
            rule_q.intensity = intensity
        except KeyError:
            return {'Error:': 'Invalid inputs'}, 400
        except BadValueError:
            return {'Error:': 'Invalid inputs'}, 400
        rule_q.put()
        return {'Success': 'Rule modified'}


api.add_resource(City, '/api/v0.1/city/<string:city>')
api.add_resource(Zone, '/api/v0.1/city/<string:city>/zone/<string:zone>')
api.add_resource(Rule, '/api/v0.1/city/<string:city>/zone/<string:zone>/rule/<string:rule>')
