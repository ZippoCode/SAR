import paho.mqtt.client as mqtt
import time, sys
from threading import Thread, Lock

HOST = 'localhost'
PORT = 5665
KEEPALEAVE = 60

threadLock = Lock()


class MQTTHandler():

    def __init__(self, robot, sala, tipologia):
        self.id_robot = robot
        self.id_sala = sala
        self.id_type = tipologia

    def on_connect(self, client, userdata, flags, rc):
        if rc != 0:
            print('Error with Result Connection: {}'.format(rc))
            exit()
        print('Avviato Robot #{}'.format(self.id_robot))
        client.subscribe('{}/{}/#'.format(self.id_sala, self.id_type))
        print("Subscribe Robot {} to topic: {}/{}".format(self.id_robot, self.id_sala, self.id_type))

    def on_message(self, client, userdata, message):
        threadLock.acquire()
        sys.stdout.write('Lavorazione Robot#{}...'.format(self.id_robot))
        sys.stdout.flush()
        for i in range(5):
            time.sleep(1)
            sys.stdout.write('...')
            sys.stdout.flush()
        ordine = message.topic.split('/')
        print(' Ordine {} inviato al posto {}'.format(message.payload, ordine[2]))
        threadLock.release()


class MQTTRobot(Thread):

    def __init__(self, handler):
        Thread.__init__(self)
        self.client = mqtt.Client('Robot {}'.format(i))
        self.client.username_pw_set('robot', 'r0b0t')
        self.client.on_connect = handler.on_connect
        self.client.on_message = handler.on_message

    def run(self):
        threadLock.acquire()
        self.client.connect(HOST, PORT, KEEPALEAVE)
        threadLock.release()
        self.client.loop_forever()


if __name__ == '__main__':
    for i in range(2):
        mqttHandler = MQTTHandler(i, 'sala1', 'BIBITA')
        mqttRobot = MQTTRobot(mqttHandler)
        mqttRobot.start()
    for i in range(2, 4):
        mqttHandler = MQTTHandler(i, 'sala1', 'MENU')
        mqttRobot = MQTTRobot(mqttHandler)
        mqttRobot.start()
    for i in range(5, 6):
        mqttHandler = MQTTHandler(i, 'sala1', 'POPCORN')
        mqttRobot = MQTTRobot(mqttHandler)
        mqttRobot.start()
