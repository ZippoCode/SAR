import paho.mqtt.client as mqtt

# Il topic deve essere in formato UNICODE
TOPIC = u"sar/example"


def on_connect(client, userdata, flags, rc):
    print('{}'.format(rc))


def on_publish(client, userdata, mid):
    # MID specifica l'identificativo del messaggio
    print("{}:{}:{}".format(client, userdata, mid))
    client.disconnect()


def on_disconnect(client, userdata, rc):
    print("Disconnected with return code: {}".format(rc))


# Connessione
client = mqtt.Client('pub')
client.username_pw_set('sar', "password")
client.connect("localhost", 8585, 60)

client.on_connect = on_connect
client.on_publish = on_publish
client.on_disconnect = on_disconnect

client.loop_start()
client.publish(TOPIC, u"Ciao sub")
client.loop_stop()

client.disconnect()