import paho.mqtt.publish as publish
import argparse

HOST = 'localhost'
PORT = 5665
AUTH = {
    'username': 'ordinazione',
    'password': '0rd1n3'}

sala_name = ['sala1', 'sala2', 'sala3', 'sala4', 'sala5', 'sala6']

parse = argparse.ArgumentParser()
parse.add_argument('sala', type=str, choices=sala_name)
parse.add_argument('posto', type=str)
parse.add_argument('item', type=str, choices=['BIBITA', 'POPCORN', 'MENU'])

if __name__ == '__main__':
    args = parse.parse_args()
    sala = args.sala
    posto = args.posto
    item = args.item

    publish.single('{}/{}/{}'.format(sala, item, posto),
                   hostname=HOST, port=PORT, auth=AUTH, payload=item)
    print('Inviato l\'ordine {} nella {} e posto {}'.format(item, sala, posto))
    exit()
