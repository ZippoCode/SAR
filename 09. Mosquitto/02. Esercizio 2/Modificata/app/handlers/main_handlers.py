from flask import render_template, request


from app.flask_app import app
from app.models.home_models import Floor, Room

dict_value = {
    'Piano seminterrato': ['Garage', 'Bagno'],
    'Piano terra': ['Sala Da Pranzo', 'Cucina', 'Bagno', 'Disimpegno'],
    'Primo piano': ['Studio', 'Camera Da Letto', 'Camera Da Letto Matrimoniale', 'Bagno', 'Disimpegno']
}


@app.route('/', methods=['GET', 'POST'])
def main():
    if request.method == 'GET':
        return render_template('list.html', value_select=dict_value.keys())
    piano = request.form.get('selection')
    state = request.form.get('state') == 'ON'
    if state:
        percentage = request.form.get('range_value')
    else:
        percentage = 0

    list_rooms = list()
    for room in dict_value[piano]:
        list_rooms.append(Room(
            id=room,
            name=room.encode('UTF-8'),
            state_light_bulb=state,
            percentage=int(percentage)
        ))

    piano = Floor(
        id=piano,
        name=piano,
        rooms=list_rooms
    )
    piano.put()
    return 'OK'


@app.errorhandler(404)
def error(error):
    return render_template('page_not_found.html'), 404
