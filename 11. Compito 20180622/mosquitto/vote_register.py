from requests import put
import paho.mqtt.client as mqtt


def on_connect(client, userdata, flags, rc):
    if rc != 0:
        print("{}", format(rc))
        exit()
    print("Connesso con codice: {}".format(rc))
    client.subscribe('Poll/#')
    print("Sottoscritto al topic: 'Poll/#'")


def on_message(client, userdata, message):
    poll_id = message.topic.split("/", 1)[1]
    http = "http://localhost:8080/api/v0.1/poll/{}".format(poll_id)
    if message.payload == b"P":
        r = put(http, json={'vote': 'P'})
    elif message.payload == b"N":
        r = put(http, json={'vote': 'N'})
    elif message.payload == b"A":
        r = put(http, json={'vote': 'R'})
    else:
        print("Errore: value {} sconosciuto".format(message.payload))
        return
    if r.status_code == 200:
        print("Richiesta effettuata. Aggiornato il valore di {} con {}".format(poll_id, message.payload))
    elif r.status_code == 404:
        print("Il sondaggio con ID {} non e' stato trovato".format(poll_id))


if __name__ == '__main__':
    client = mqtt.Client("Vote register")
    client.username_pw_set('compito20180622','password20180622')
    client.connect("localhost", 8585, 60)

    client.on_connect = on_connect
    client.on_message = on_message
    client.loop_forever()
