from flask import Flask, render_template, request
import paho.mqtt.publish as publish

app = Flask(__name__)
app.config.from_object(__name__)

HOST = 'localhost'
PORT = 5888
AUTH = {'username': 'home', 'password': '1234root'}

dict_value = {
    'Tutta': '',
    'Piano seminterrato': ['Garage', 'Bagno'],
    'Piano terra': ['Sala Da Pranzo', 'Cucina', 'Bagno', 'Disimpegno'],
    'Primo piano': ['Studio', 'Camera Da Letto', 'Camera Da Letto Matrimoniale', 'Bagno', 'Disimpegno']
}


@app.route('/', methods=['POST', 'GET'])
def main():
    if request.method == 'GET':
        return render_template('list.html', value_list=dict_value)
    floor = request.form.get('select_value')
    checkbox = request.form.get('checkbox') == 'on'
    value = request.form.get('slider')

    if floor == 'Tutta':
        floor = ['Piano seminterrato', 'Piano Terra', 'Primo Piano']
    else:
        floor = dict_value[floor]
    msgs = []
    for room in floor:
        if checkbox:
            msgs.append((u'Home/{}/{}/Lights'.format(floor, room), checkbox))
        msgs.append((u'Home/{}/{}/Shades'.format(floor, room), value))
    publish.multiple(msgs, hostname=HOST, port=PORT, auth=AUTH)
    return render_template('list.html', value_list=dict_value, inviato = True)


if __name__ == '__main__':
    app.run('0.0.0.0', debug=True)
