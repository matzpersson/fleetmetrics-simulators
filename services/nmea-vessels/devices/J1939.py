# Simulator device for J1939 engine interfaces

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

# This is a completely bogus structure of NMEA 2000 sentences. This is simply intended as
# a place holder and demo data simulation for delivering J1939 style data from an engine across mqtt to the gateway
# server. The PGN Sentences in this class are completely open text which would not be true in a real NMEA sentence.
# Talker ID's and message are made up.

# -- NMEA Example PGN's:
# 127488 - Engine Speed (RPM)
# 127488 - Engine Load (%)
# 127488 - Engine Turbocharger Boost Pressure (kPa)
# 127489 - Engine Oil Pressure (kPa)
# 127489 - Engine Oil Temperature (C)
# 127489 - Engine Coolant Temperature (C)
# 127489 - Alternator Voltage (V)
# 127489 - Engine Fuel Rate (l/h)
# 127489 - Engine Total Hours ()
# 127489 - Engine Coolant Pressure (kPa)
# 127489 - Engine Fuel Delivery Pressure (kPa)
# 127489 - Electrical Voltage (V)
# 127489 - Battery Voltage (V)
# 127498 - Engine Rated Speed (RPM)
# 127498 - Vehicle Identification Number
# 127493 - Transmission Current Gear ()
# 127493 - Transmission Oil Pressure (kPa)
# 127493 - Transmission Oil Temperature (C)

# -- NMEA 2000 PGN sentence breakdown example:
# PGN 127245:
# Name: Rudder
# Source: 115, Destination: 255
# Priorty: 2, Length:8
# Number of Fields: 6
# Field 1: Rudder Instance = 255
# Field 2: Direction Order = 0
# Field 3: Reserved Field
# Field 4: Angle Order = -0.0001 Radians
# Field 5: Position = -1.0821
# Field 6: Reserved Field

class J1939(threading.Thread):
    def __init__(self, logging, vessel, mqtt_publisher, number):
        threading.Thread.__init__(self)
        self.logging = logging

        self.vessel = vessel
        self.mqtt_publisher = mqtt_publisher
        self.random_sleep = random.randrange(5, 10, 2)
        self.log_prefix = "{} - ".format(self.vessel['name'])

        # This would never happen
        self.talkerid = "XP{}".format(number)

    def run(self):
        self.logging.info("Engine parameters..")

        while True:
            msg = self.engineSpeed()
            self.logging.info("{}{}".format(self.log_prefix, msg))
            self.mqtt_publisher.publish(self.vessel["id"], msg)
            time.sleep(1)

            msg = self.engineLoad()
            self.logging.info("{}{}".format(self.log_prefix, msg))
            self.mqtt_publisher.publish(self.vessel["id"], msg)
            time.sleep(1)

            msg = self.engineOilPressure()
            self.logging.info("{}{}".format(self.log_prefix, msg))
            self.mqtt_publisher.publish(self.vessel["id"], msg)
            time.sleep(1)

            msg = self.engineOilTemperature()
            self.logging.info("{}{}".format(self.log_prefix, msg))
            self.mqtt_publisher.publish(self.vessel["id"], msg)
            time.sleep(1)

            msg = self.engineCoolantTemperature()
            self.logging.info("{}{}".format(self.log_prefix, msg))
            self.mqtt_publisher.publish(self.vessel["id"], msg)
            time.sleep(1)

            msg = self.engineCoolantPressure()
            self.logging.info("{}{}".format(self.log_prefix, msg))
            self.mqtt_publisher.publish(self.vessel["id"], msg)
            time.sleep(1)

            msg = self.alternatorVoltage()
            self.logging.info("{}{}".format(self.log_prefix, msg))
            self.mqtt_publisher.publish(self.vessel["id"], msg)
            time.sleep(1)

            msg = self.batteryVoltage()
            self.logging.info("{}{}".format(self.log_prefix, msg))
            self.mqtt_publisher.publish(self.vessel["id"], msg)
            time.sleep(1)

            msg = self.transmissionOilTemperature()
            self.logging.info("{}{}".format(self.log_prefix, msg))
            self.mqtt_publisher.publish(self.vessel["id"], msg)
            time.sleep(1)

            msg = self.transmissionOilPressure()
            self.logging.info("{}{}".format(self.log_prefix, msg))
            self.mqtt_publisher.publish(self.vessel["id"], msg)
            time.sleep(1)

            msg = self.engineFuelRate()
            self.logging.info("{}{}".format(self.log_prefix, msg))
            self.mqtt_publisher.publish(self.vessel["id"], msg)
            time.sleep(1)

            msg = self.engineTotalHours()
            self.logging.info("{}{}".format(self.log_prefix, msg))
            self.mqtt_publisher.publish(self.vessel["id"], msg)

            time.sleep(self.random_sleep)

    def engineSpeed(self):
        prefix = "ESR"

        rpm = random.randrange(1800, 2000, 2)
        return "${}{},{},M,A,A*03".format(self.talkerid, prefix, rpm)

    def engineLoad(self):
        prefix = "ELL"

        load = random.randrange(60, 70, 2)
        return "${}{},{},M,A,A*03".format(self.talkerid, prefix, load)

    def engineOilPressure(self):
        prefix = "EOP"

        kpa = random.randrange(350, 400, 2)
        return "${}{},{},M,A,A*03".format(self.talkerid, prefix, kpa)

    def engineOilTemperature(self):
        prefix = "EOT"

        temp = random.randrange(60, 70, 2)
        return "${}{},{},M,A,A*03".format(self.talkerid, prefix, temp)

    def engineCoolantTemperature(self):
        prefix = "ECT"

        temp = random.randrange(40, 55, 2)
        return "${}{},{},M,A,A*03".format(self.talkerid, prefix, temp)

    def engineCoolantPressure(self):
        prefix = "ECP"

        kpa = random.randrange(50, 60, 2)
        return "${}{},{},M,A,A*03".format(self.talkerid, prefix, kpa)

    def alternatorVoltage(self):
        prefix = "VOA"

        v = round(random.uniform(12.1, 14.0),2)
        return "${}{},{},M,A,A*03".format(self.talkerid, prefix, v)

    def batteryVoltage(self):
        prefix = "VOA"

        v = round(random.uniform(12.1, 14.0),2)
        return "${}{},{},M,A,A*03".format(self.talkerid, prefix, v)

    def transmissionOilTemperature(self):
        prefix = "TOT"

        temp = random.randrange(40, 55, 2)
        return "${}{},{},M,A,A*03".format(self.talkerid, prefix, temp)

    def transmissionOilPressure(self):
        prefix = "TOP"

        kpa = random.randrange(70, 90, 2)
        return "${}{},{},M,A,A*03".format(self.talkerid, prefix, kpa)

    def engineFuelRate(self):
        prefix = "EFR"

        lph = random.randrange(40, 60, 2)
        return "${}{},{},M,A,A*03".format(self.talkerid, prefix, lph)

    def engineTotalHours(self):
        prefix = "ETH"

        # Date of last rebuild
        d1 = datetime.strptime("2018-01-01", "%Y-%m-%d")
        now = datetime.now()

        # 20% utilisation (Again, just crazy numbers for demos)
        hours = ((now - d1).days * 24) * .2
        return "${}{},{},M,A,A*03".format(self.talkerid, prefix, hours)
