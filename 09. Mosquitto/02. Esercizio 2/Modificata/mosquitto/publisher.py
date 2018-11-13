import paho.mqtt.publish as publish
from requests import get
from sys import exit
from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument('num_floor', type=int, choices=[0, 1, 2])

HOST = 'localhost'
PORT = 5666
URI = "http://localhost:8080/api/v1.0/state_floor/{}"
AUTH = {'username': 'publisher', 'password': 'passwdPub'}


def call_api(num_piano):
    try:
        request_get = get(URI.format(num_piano))
    except:
        print('ERROR. The APIs not available.')
        return 0
    if request_get.status_code == 200:
        json_body = request_get.json()
        for room in json_body['Rooms']:
            TOPIC = 'Home/{}/{}'.format(json_body['Floor'], room['Name'])
            state = room['State Light Bulb']
            percentage = room['Percentage']
            publish.single(TOPIC, hostname=HOST, port=PORT, payload=percentage, auth=AUTH)
    if request_get.status_code == 404:
        print('Room not found')


if __name__ == '__main__':
    args = parser.parse_args()
    exit(call_api(args.num_floor))
