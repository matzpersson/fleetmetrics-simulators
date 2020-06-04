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

class Wind(threading.Thread):
    def __init__(self, logging, vessel, mqtt_publisher):
        threading.Thread.__init__(self)
        self.logging = logging

        self.vessel = vessel
        self.mqtt_publisher = mqtt_publisher
        self.random_sleep = random.randrange(5, 10, 2)
        self.log_prefix = "{} - ".format(self.vessel['name'])

        self.talkerid = "IN"

    def run(self):
        self.logging.info("Running Wind Speed..")

        self.current_position = self.vessel["start_point"]
        while True:
            msg = self.mwv(self.current_position)
            self.logging.info("{}{}".format(self.log_prefix, msg))
            self.mqtt_publisher.publish(self.vessel["id"], msg)

            time.sleep(self.random_sleep)

    def mwv(self, current_position):
        prefix = "MWV"

        angle = random.randrange(110, 180, 2)
        kts = random.randrange(18, 25, 2)
        return "${}{},{},T,{},M,A,A*03".format(self.talkerid, prefix, angle, kts)