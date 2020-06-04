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
from geopy.distance import distance as geopy_distance

class Gps(threading.Thread):
    def __init__(self, logging, vessel, mqtt_publisher):
        threading.Thread.__init__(self)
        self.logging = logging

        self.vessel = vessel
        self.mqtt_publisher = mqtt_publisher
        self.random_sleep = random.randrange(5, 10, 2)
        self.log_prefix = "{} - ".format(self.vessel['name'])

        self.talkerid = "GP"

    def run(self):
        self.logging.info("Running Gps..")

        nm2km = 1.852
        idx = 0

        self.current_position = self.vessel["start_point"]
        self.next_waypoint = self.vessel["waypoints"][idx]

        while True:
            # Coordinates
            lat1 = self.current_position["lat"]
            lon1 = self.current_position["lon"]

            lat2 = self.next_waypoint["lat"]
            lon2 = self.next_waypoint["lon"]

            kts = self.current_position["kts"]

            # Nm travelled over the last random_sleep
            distance = (kts / 3600) * self.random_sleep
            bearing = self.get_bearing(lat1, lon1, lat2, lon2)

            origin = geopy.Point(lat1, lon1)
            destination = geodesic(kilometers=(distance * nm2km)).destination(origin, bearing)

            msg = self.gll(destination.latitude, destination.longitude)
            self.logging.info("{}{}".format(self.log_prefix, msg))
            self.mqtt_publisher.publish(self.vessel["id"], msg)

            msg = self.hdt(bearing)
            self.logging.info("{}{}".format(self.log_prefix, msg))
            self.mqtt_publisher.publish(self.vessel["id"], msg)

            msg = self.vhw(bearing, kts)
            self.logging.info("{}{}".format(self.log_prefix, msg))
            self.mqtt_publisher.publish(self.vessel["id"], msg)

            self.current_position["lat"] = destination.latitude
            self.current_position["lon"] = destination.longitude

            # Work out how close to waypoint we are.
            distanceToWaypoint = geopy_distance(geopy.Point(self.current_position["lat"], self.current_position["lon"]), geopy.Point(lat2, lon2)).miles
            if distanceToWaypoint < 1:
                if idx == (len(self.vessel["waypoints"]) - 1):
                    idx = 0
                else:
                    idx +=1

                self.current_position = self.next_waypoint
                self.next_waypoint = self.vessel["waypoints"][idx]

            # print("DISTANCE", distanceToWaypoint)
            
            time.sleep(self.random_sleep)

    def hdt(self, bearing):
        # Using bearing as heading until we introduce set/drift
        heading = bearing

        prefix = "HDT"
        return "${}{},{},T*03".format(self.talkerid, prefix, heading)

    def vhw(self, kts, bearing):
        # Using bearing as heading until we introduce set/drift
        heading = bearing

        prefix = "VHW"
        return "${}{},{},T,0,M,{},N,0,K,*03".format(self.talkerid, prefix, heading, kts)

    def gll(self, lat, lon):
        prefix = "GLL"

        lat, latCardinal = self.getLatCardinal(lat)
        lon, lonCardinal = self.getLonCardinal(lon)
        
        encoded_lat = self.encodeCoord(lat)
        encoded_lon = self.encodeCoord(lon)
        nowtime = self.encodeDate()

        return "${}{},{},{},{},{},{},{},{}".format(self.talkerid, prefix, encoded_lat, latCardinal, encoded_lon, lonCardinal, nowtime, "A", "A*67")

    def getLatCardinal(self, coord):

        if coord < 0:
            cardinal = "S"
            coord = -coord
        else:
            cardinal = "N"

        return coord, cardinal

    def getLonCardinal(self, coord):

        if coord < 0:
            cardinal = "W"
            coord = -coord
        else:
            cardinal = "E"
            
        return coord, cardinal


    def encodeCoord(self, coord):
        d = int(coord)
        m = 60 * (coord - d)

        return '{}{:09.6f}'.format(d,m)

    def encodeDate(self):
        now = datetime.now()
        return now.strftime("%H%M%S.%f")

    def get_bearing(self, lat1,lon1,lat2,lon2):
        dLon = lon2 - lon1
        y = math.sin(dLon) * math.cos(lat2)
        x = math.cos(lat1)*math.sin(lat2) - math.sin(lat1)*math.cos(lat2)*math.cos(dLon)
        brng = np.rad2deg(math.atan2(y, x))
        if brng < 0: brng+= 360
        return brng
