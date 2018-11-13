import argparse
from sys import exit

import paho.mqtt.publish as publish

parser = argparse.ArgumentParser()
parser.add_argument('track_id', type=int, help="Richiesta ID traccia")
parser.add_argument('postazione', type=str, help='Richiesta la postazione', choices=['01', '02', '03'])
AUTH = {
    'username': "karaoke",
    'password': "passka"
}
HOSTNAME = 'localhost'
PORT = 7000


def send_message():
    args = parser.parse_args()
    track_id = args.track_id
    postazione_id = args.postazione
    print('Start Karaoke - TRACK ID: {}'.format(track_id))
    publish.single('Play/{}'.format(postazione_id), hostname=HOSTNAME, port=PORT,
                   payload=track_id, client_id="postazione", auth=AUTH)
    print("La modifica e' stata pubblicate nella rete MQTT")
    return 0


if __name__ == '__main__':
    exit(send_message())
