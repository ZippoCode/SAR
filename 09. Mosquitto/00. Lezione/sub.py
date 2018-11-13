import paho.mqtt.client as mqtt


def on_connect(client, userdata, flags, rc):
    """
        Invocato quando il client si connette
        Per sottoscrivere il client ad un topic di utilizza il metodo 'subscribe'
        e si utilizzato due parametri, il primo e' una stringa per il nome del topic
        mentre il secondo parametro - int: 0,1,2 - identifica la QoS (di default e' massima)
    :param client:
    :param userdata:
    :param flags:
    :param rc:
    :return:
    """
    if rc != 0:
        print("{}", format(rc))
        exit()
    client.subscribe('sar/#')


def on_message(client, userdata, message):
    """
        Invocato quando ri riceve un messaggio

    :param client:
    :param userdata:
    :param message:
    :return:
    """
    print("{}::{}".format(message.topic, message.payload))


client = mqtt.Client()
client.username_pw_set("sar", "password")
# Per la connessione e' necessario specificare il KEEP A LIVE dei messaggi
client.connect("localhost", 8585, 60)

client.on_connect = on_connect
client.on_message = on_message

client.loop_forever()
