from flask import render_template
import unirest

from app.flask_app import app
from app.models.models import CityModel
from app_secrets import mashape_key

URL_LL = "https://devru-latitude-longitude-find-v1.p.mashape.com/latlon.php?location="
URL_WEATHER = "https://weatherbit-v1-mashape.p.mashape.com/forecast/3hourly?lat={}&lon={}"


@app.route('/', methods=['GET', 'POST'])
def main():
    city_fetch = CityModel.query().order(CityModel.name).fetch()
    cities = list()
    for c in city_fetch:
        cities.append((c.name, c.zone))
    return render_template('list.html', list=city_fetch)


@app.route('/show_city/<string:name_city>', methods=['GET', 'POST'])
def show_city(name_city):
    result = ((unirest.get(URL_LL + name_city,
                           headers={"X-Mashape-Key": mashape_key,
                                    "Accept": "application/json"})).body['Results'])[0]
    response = unirest.get(URL_WEATHER.format(result['lat'], result['lon']),
                           headers={
                               "X-Mashape-Key": mashape_key,
                               "Accept": "application/json"})
    print response.body
    return ""


@app.errorhandler(404)
def handle_bad_request(error):
    return render_template('page_not_found.html'), 400
