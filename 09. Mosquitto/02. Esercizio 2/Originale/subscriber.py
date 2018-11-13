from sys import exit
import paho.mqtt.client as mqtt
from argparse import ArgumentParser

HOST = 'localhost'
PORT = 5888
USER = 'home'
PASSWORD = "1234root"

parser = ArgumentParser()
parser.add_argument('num_floor', type=int, choices=[0, 1, 2])


def on_connect(client, username, flags, rc):
    if rc != 0:
        print("Error: Reconnection Code: {}".format(rc))
        exit()
    print('Connection...')


def on_message(client, username, message):
    print("Value from {} is: {}".format(message.topic, message.payload))


def run_subscriber(floor):
    client = mqtt.Client('SUB')
    client.username_pw_set(USER, PASSWORD)
    client.connect(host=HOST, port=PORT)

    client.on_connect = on_connect
    client.on_message = on_message

    client.subscribe('Home/{}/#'.format(floor), 1)
    print('Subscriber to Topic: Home/{}'.format(floor))

    client.loop_forever()


if __name__ == '__main__':
    args = parser.parse_args()
    num_floor = args.num_floor
    if num_floor == 0:
        floor = 'Piano seminterrato'
    elif num_floor == 1:
        floor = 'Piano terra'
    else:
        floor = 'Primo piano'
    exit(run_subscriber(floor))
