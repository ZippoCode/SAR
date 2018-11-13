import paho.mqtt.client as mqtt
from argparse import ArgumentParser

HOST = 'localhost'
PORT = 5666

parser = ArgumentParser()
parser.add_argument('name_floor', type=str, choices=['Piano seminterrato',
                                                     'Piano terra', 'Primo piano'])


def on_connect(client, username, flags, rc):
    if rc != 0:
        print('Error: Reconnection Code: {}'.format(rc))
        exit()
    print('Connected')


def on_message(client, username, message):
    folds = message.topic.split('/')
    print('Stato Room {} is {}'.format(folds[2], message.payload))


if __name__ == '__main__':
    args = parser.parse_args()

    client = mqtt.Client('SUB')
    client.username_pw_set('subscriber', 'passwdSub')

    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(HOST, PORT)
    client.subscribe('Home/{}/#'.format(args.name_floor))
    print('Sottoscritto al TOPIC: Home/{}/#'.format(args.name_floor))

    client.loop_forever()
