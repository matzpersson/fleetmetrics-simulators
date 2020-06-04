import uuid
import subprocess
import time
from datetime import datetime
import os
import sys
import threading
import math, numpy as np
import geopy
import json
import random
from geopy.distance import geodesic

class Depth(threading.Thread):
    def __init__(self, logging, vessel, mqtt_publisher):
        threading.Thread.__init__(self)
        self.logging = logging

        self.vessel = vessel
        self.mqtt_publisher = mqtt_publisher
        self.random_sleep = random.randrange(5, 10, 2)
        self.log_prefix = "{} - ".format(self.vessel['name'])

        self.talkerid = "IN"

    def run(self):
        self.logging.info("Running Gps..")

        self.current_position = self.vessel["start_point"]
        while True:
            msg = self.dpt(self.current_position)
            self.logging.info("{}{}".format(self.log_prefix, msg))
            self.mqtt_publisher.publish(self.vessel["id"], msg)

            time.sleep(self.random_sleep)

    def dpt(self, current_position):
        prefix = "DPT"

        depth = random.randrange(current_position["depth"]["min"], current_position["depth"]["max"], 2)
        return "${}{},{},T*03".format(self.talkerid, prefix, depth)

