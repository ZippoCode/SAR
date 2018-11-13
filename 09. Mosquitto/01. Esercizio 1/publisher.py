import time, random, argparse
from threading import Thread, Lock
import paho.mqtt.client as mqtt

HOST = 'localhost'
PORT = 5656

parse = argparse.ArgumentParser()
parse.add_argument('num_car', type=int, default=2)
parse.add_argument('num_laps', type=int, default=20)


class Car(Thread):
    def __init__(self, name, id_car, num_laps):
        Thread.__init__(self)
        self._topic = "{}/{}".format(name, id_car)
        self._client = mqtt.Client('PUB - {} # {}'.format(name, id_car))
        self._client.username_pw_set(name, 'password{}'.format(name))
        self._vlock = Lock()
        self._num_labs = num_laps

        self._client.loop_start()
        self._client.connect(HOST, PORT)
        self._client.loop_stop()

    def run(self):
        num_giro = 0
        speed = 0
        torque = 0
        gear = 1
        tires = 100

        while num_giro <= self._num_labs:
            self._vlock.acquire()
            self._client.loop_start()
            if gear <= 5:
                delta_speed = random.randint(10, 21)
                delta_torque = random.randint(100, 201)
            elif gear <= 8:
                delta_speed = random.randint(8, 17)
                delta_torque = random.randint(80, 161)
            else:
                delta_speed = random.randint(10, 13)
                delta_torque = random.randint(100, 121)

            if random.uniform(0, 1.1) < 0.95:
                speed += delta_speed
                torque += delta_torque
            else:
                speed -= delta_speed
                torque -= delta_torque

            if speed < 0:
                speed = 0
            if torque < 0:
                torque = 0

            if speed < 30:
                gear = 1
            elif speed < 50:
                gear = 2
            elif speed < 80:
                gear = 3
            elif speed < 120:
                gear = 4
            elif speed < 150:
                gear = 5
            elif speed < 180:
                gear = 6
            elif speed < 210:
                gear = 7
            elif speed < 240:
                gear = 8
            elif speed < 260:
                gear = 9
            else:
                gear = 10
            tires = tires - tires * random.uniform(0.05, 0.1) / 100
            tires = round(tires, 3)

            self._client.publish(self._topic + "/Engine/Speed", speed)
            self._client.publish(self._topic + "/Engine/Torque", torque)
            self._client.publish(self._topic + "/Engine/Gear", gear)
            self._client.publish(self._topic + "/Body/Tires", tires)
            self._client.loop_stop()
            num_giro += 1
            self._vlock.release()

            time.sleep(1)

        self._vlock.acquire()
        self._client.loop_start()
        self._client.publish(self._topic, "END")
        self._client.loop_stop()
        self._client.disconnect()
        self._vlock.release()


if __name__ == '__main__':
    args = parse.parse_args()
    NUM_CAR = args.num_car
    num_laps = args.num_laps
    for num in range(1, NUM_CAR + 1):
        Car('Ferrari', num, num_laps).start()
        Car('Mercedes', num, num_laps).start()
