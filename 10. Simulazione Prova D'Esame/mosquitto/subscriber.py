import argparse
import paho.mqtt.client as mqtt

parser = argparse.ArgumentParser()
parser.add_argument('num_piano', type=int, choices=[1, 2, 3], help='Il piano deve essere compreso tra 1 e 3')

NUM_SLOT = 10


class MQTTHandler:
    def __init__(self, piano, numero_slot):
        self._piano = piano
        self._numero_slot = numero_slot
        self._slot_liberi = NUM_SLOT

    def on_connect(self, client, userdata, flags, rc):
        if rc != 0:
            print("{}", format(rc))
            exit()
        print("Connesso con codice: {}".format(rc))
        client.subscribe("{}/#".format(self._piano))
        print("SETTING: Piano {} - Numero Slot {}".format(self._piano, NUM_SLOT))

    def on_message(self, client, userdata, flags, rc):
        if message.payload == b'free':
            self._slot_liberi += 1
            print("Nuovo slot disponibile. Stato corrente: {}::{}".format(
                self._numero_slot, self._slot_liberi))
        elif message.payload == b'occupied':
            self._slot_liberi -= 1
            print("Nuovo slot occupato. Stato corrente: {}::{}".format(
                self._numero_slot, self._slot_liberi))
        else:
            print('ERRORE: {}'.format(message.payload))


if __name__ == '__main__':
    args = parser.parse_args()
    num_floor = args.num_piano

    client = mqtt.Client("sub{}".format(num_floor))
    client.connect("localhost", 8585, 60)

    handler = MQTTHandler(num_floor, NUM_SLOT)
    client.on_connect = handler.on_connect
    client.on_message = handler.on_message
    client.loop_forever()
