import argparse
from requests import put
from sys import exit

import paho.mqtt.publish as publish

parser = argparse.ArgumentParser()
parser.add_argument('slot_id', type=int)
parser.add_argument('state', type=str, choices=['free', 'occupied'])


def operation():
    args = parser.parse_args()
    slot_id = args.slot_id
    state = args.state

    piano = slot_id // 100
    numero = slot_id % 100
    print('Setting: SLOT {} (Numero {} e piano {}) in {}'.format(slot_id, numero, piano, state))
    try:
        r = put("http://localhost:8080/api/v1.0/slot/{}".format(slot_id), json={'state': (state == 'free')})
    except IOError as error:
        print('Impossibile contattare le APIs: {}'.format(error))
        return 0
    if r.status_code == 200:
        publish.single('{}/{}'.format(piano, numero), hostname='localhost', port=5666,
                       payload=args.state.encode(), client_id="pub")
        print("La modifica e' stata pubblicate nella rete MQTT")
        return 0

    if r.status_code == 400:
        print("La modifica non e' avvenuta, e il messaggio non verra' pubblicato")
        return 0

    if r.status_code == 404:
        print('Parking slot {} non esiste'.format(slot_id))
        return 1

    print('Errore inaspettato: {}'.format(r.status_code))
    return 1


if __name__ == '__main__':
    exit(operation())
