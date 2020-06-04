import time
import os
import sys
import threading

sys.path.append('./services/nmea-vessels/devices/')

from Gps import Gps
from Depth import Depth
from Wind import Wind
from J1939 import J1939

class Vessel(threading.Thread):
    def __init__(self, logging, vessel, mqtt_publisher):
        threading.Thread.__init__(self)
        self.logging = logging

        self.vessel = vessel
        self.mqtt_publisher = mqtt_publisher

    def run(self):
        self.logging.info("Running Gps..")

        self.logging.info("Init Gps...")
        gps = Gps(self.logging, self.vessel, self.mqtt_publisher)
        gps.start()

        self.logging.info("Init Depth Sounder...")
        depth = Depth(self.logging, self.vessel, self.mqtt_publisher)
        depth.start()

        self.logging.info("Init Anometer...")
        wind = Wind(self.logging, self.vessel, self.mqtt_publisher)
        wind.start()

        self.logging.info("Engine 1...")
        engine1 = J1939(self.logging, self.vessel, self.mqtt_publisher, 1)
        engine1.start()

        self.logging.info("Engine 2...")
        engine2 = J1939(self.logging, self.vessel, self.mqtt_publisher, 2)
        engine2.start()
