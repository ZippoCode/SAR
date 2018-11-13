import argparse
import paho.mqtt.client as mqtt

parser = argparse.ArgumentParser()
parser.add_argument('postazione', type=str, help='Richiesta la postazione', choices=['01', '02', '03'])


class MQTTHandler:
    def __init__(self, id_postazione):
        self._id_postazione = id_postazione

    def on_connect(self, client, userdata, flags, rc):
        if rc != 0:
            print("{}", format(rc))
            exit()
        print("Connesso con codice: {}".format(rc))
        client.subscribe("Play/#".format(self._id_postazione))
        print("Avviato Karaoke alla postazione {}".format(self._id_postazione))

    def on_message(self, client, userdata, message):
        print(message.payload)

if __name__ == '__main__':
    args = parser.parse_args()
    postazione_id = args.postazione

    client = mqtt.Client("postazione {}".format(postazione_id))
    client.username_pw_set('postazione', 'passpo')
    client.connect("localhost", 7000, 60)
    mqttHandler = MQTTHandler(postazione_id)

    client.on_connect = mqttHandler.on_connect
    client.on_message = mqttHandler.on_message

    client.loop_forever()
