import argparse
import base64
from sys import exit

import paho.mqtt.publish as publish

parser = argparse.ArgumentParser()
parser.add_argument('poll_id', type=str, help="Richiesta")
parser.add_argument('vote', choices=['P', 'N', 'A'])

AUTH = {
    'username': "compito20180622",
    'password': "password20180622"
}
HOSTNAME = 'localhost'
PORT = 8585


def send_message():
    args = parser.parse_args()
    state_id = args.poll_id
    type_vote = args.vote
    print('Setting: Edit POLL-ID  {} as {}'.format(state_id, type_vote))
    publish.single('Poll/{}'.format(state_id), hostname=HOSTNAME, port=PORT,
                   payload=type_vote, client_id="PUB", auth=AUTH)
    print("La modifica e' stata pubblicate nella rete MQTT")
    return 0


if __name__ == '__main__':
    exit(send_message())
