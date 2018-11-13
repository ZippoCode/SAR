import paho.mqtt.client as mqtt

HOST = 'localhost'
PORT = 5656
KEEPALIVE = 60

TOPIC = 'Gara/#'


def on_connect(client, userdata, flags, rc):
    if rc != 0:
        print('Error with Result Connection: {}'.format(rc))
        exit()
    client.subscribe('#')
    print("Subscribe to topic: {} ".format(TOPIC))


def on_message(client, userdata, message):
    value_topic = message.topic.split('/', 4)
    if len(value_topic) >= 3:
        value_type = value_topic[3]
        print('Value from {} # {} for {} is {}'.format(value_topic[0], value_topic[1], value_type,
                                                  message.payload))
    else:
        print("Value from {} # {} is {}".format(value_topic[0], value_topic[1], message.payload))


if __name__ == '__main__':
    client = mqtt.Client('subscriber')
    client.username_pw_set('subscriber', 'passwordSubscriber')
    client.connect(HOST, PORT, KEEPALIVE)

    client.on_connect = on_connect
    client.on_message = on_message

    client.loop_forever()
