
# NMEA Vessel simulation service - Imports vessel definition and lauches voyages

import os
import time
import json
import sys

from Vessel import Vessel

class NmeaVessels():
    def __init__(self, logging, mqtt_publisher):
        self.logging = logging
        self.mqtt_publisher = mqtt_publisher

    def start(self):
        print(os.getcwd())
        filepath = "./services/nmea-vessels/vessels/"
        for filename in os.listdir(filepath):
            if filename.endswith('.json'):
                with open(filepath + filename) as json_file:
                    vessel = json.load(json_file)

                vessel = Vessel(self.logging, vessel, self.mqtt_publisher)
                vessel.start()
