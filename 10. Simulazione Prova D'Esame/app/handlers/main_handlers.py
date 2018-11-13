import re, random, unirest, base64
from flask import render_template, request, session, redirect, url_for

from app.flask_app import app
from app.models.models import Parking, Booking

REGEX_EMAIL = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"


@app.route('/', methods=['GET', 'POST'])
def main():
    if request.method == 'GET':
        return render_template('list.html')
    elif request.method == 'POST':
        email = request.form.get('email')
        if not re.match(REGEX_EMAIL, email):
            return render_template('list.html', error=str(email) + " non valida"), 400
        parking_list = Parking.query(Parking.state == True).fetch()
        if len(parking_list) == 0 or not parking_list:
            return render_template('list.html', error='Nessun posto disponibile.')
        random.shuffle(parking_list)
        parking = parking_list[0]
        code = random.randint(10000, 100000)
        booking = Booking(id=email,
                          user_id=email,
                          parking=parking.parking_id,
                          code=code)
        parking.state = False
        booking.put()
        parking.put()
        session['prenotazione'] = {
            'ID': booking.user_id,
            'Parking': booking.parking,
            'Code': booking.code,
            'Created': booking.date
        }
        return redirect(url_for('show_details'))
    else:
        return "ERROR"


@app.route('/show_parking', methods=['GET'])
def show_parking():
    parking_list = Parking.query().fetch()
    return render_template('show_parking.html', parkings=parking_list)


@app.route('/show_details', methods=['GET'])
def show_details():
    booking = prenotazione = session.pop('prenotazione', None)
    print(booking)
    return render_template("show_details.html", prenotazione=booking)


@app.errorhandler(404)
def error(error):
    return render_template('page_not_found.html'), 404