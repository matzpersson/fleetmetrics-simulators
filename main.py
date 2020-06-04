# --- MQTT Sensor/Sentence Simulator

# Dedency: pip install geopy, numpy, paho-mqtt

import datetime
import logging
import sys
import time
import json
import os

sys.path.append('./lib/')
# sys.path.append('./devices/')
sys.path.append('./services/nmea-vessels/')

from Mqtt import MqttPublisher
# from Vessel import Vessel
from NmeaVessels import NmeaVessels

# -- Start logging
format = "%(asctime)s: %(message)s"
logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")

logging.info("Starting Nmea 0183 Simulator...")

# -- MQTT Connection
mqtt_host = os.getenv('MQTT_HOST') if os.getenv('MQTT_HOST') else 'localhost'
mqtt_port = int(os.getenv('MQTT_PORT')) if os.getenv('MQTT_PORT') else 1883

logging.info("Starting MQTT client on {}:{}".format(mqtt_host, mqtt_port))
mqtt_publisher = MqttPublisher(logging, mqtt_host, mqtt_port)
mqtt_publisher.start()

# -- Services
# Nmea Vessel simulation service
vessels = NmeaVessels(logging, mqtt_publisher)
vessels.start()

while True:
    time.sleep(1)
