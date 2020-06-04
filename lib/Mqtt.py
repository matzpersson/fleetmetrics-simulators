import time
import os
import sys
import paho.mqtt.client as mqtt
import threading
from datetime import datetime

class MqttPublisher(threading.Thread):
    def __init__(self, logging, broker="localhost", port=1883):
        self.logging = logging

        threading.Thread.__init__(self)

        self.broker = broker
        self.port = port
        self.client = mqtt.Client()
        # self.client.on_publish = self.on_publish

    def run(self):
        while True:
            try:
                self.logging.info("Attempting to connect to MttqPublisher on {}:{}".format(self.broker, self.port))
                self.client.connect(self.broker, self.port)
                self.client.loop_start()
            except OSError as err:
                print("OS error: {0}".format(err))
            except Exception as err:
                self.logging.info("... Failed to connect. Try again in 10s {0}".format(err))

            time.sleep(10)

    def publish(self, topic, msg):
        now = datetime.utcnow()
        payload = "{},{}".format(now.strftime("%Y-%m-%d %H:%M:%S.%f"), msg)

        self.client.publish(topic, payload=payload, qos=1, retain=True)
        # self.logging.info("MttqPublisher sending: {} for topic: {}".format(payload, topic))

    def on_publish(self, client, userdata, mid):
        # self.logging.info("Mttq published!")
        pass
