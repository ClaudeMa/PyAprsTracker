#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2024 F4IKH
#
# This file is part of PyAprstracker.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, see <http://www.gnu.org/licenses/>.
import os
import sys
from datetime import date, datetime
from sys import argv
import time
from serial import Serial
from pynmeagps import NMEAReader
from ax253 import Frame
from aprs import geo_util
import kiss
import logging
import zulu
import timesetter

import constants
import config

speed = 0.0  # km/h
turn_angle = 0.0  # degré
current_millis = 0  # temps courant millisecondes
last_tx_time_millis = 0  # temps dernier beacon envoyé miliisecondes
nofix = True
rate = dict()
logger = logging.getLogger(__name__)


def debug(s):
    if config.debug['debug']:
        print(s)


def errhandler(err):
    global logger
    logger.critical(f"\nERROR: {err}\n")


def aprstime():
    dt = zulu.now()
    return bytes(dt.format('ddHHmm').strip() + "z", 'utf-8')


def setsystemtimefromgps(mdate, mtime):
    gpstime = datetime(year=mdate.year,
                       month=mdate.month,
                       day=mdate.day,
                       hour=mtime.hour,
                       minute=mtime.minute,
                       second=mtime.second)
    systemdate = zulu.now()
    if systemdate.timestamp() < gpstime.timestamp():
        logger.info("System  date set to {str(gpstime)}")
        os.system('sudo date -–set=”%s”' % gpstime)

def init_logging():
    global logger
    if config.debug['debug']:
        logFormatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")
        logger = logging.getLogger()
        numeric_level = getattr(logging, str(config.debug['loglevel']).upper(), None)
        if not isinstance(numeric_level, int):
            raise ValueError('Invalid log level: %s' % config.debug['loglevel'])
        logger.setLevel(numeric_level)
        if config.debug['logfile']:
            today = date.today()
            filename = today.strftime("%d%m%Y")
            logpath = config.debug['logfilepath']
            fileHandler = logging.FileHandler("{0}/{1}.log".format(logpath, filename))
            fileHandler.setFormatter(logFormatter)
            logger.addHandler(fileHandler)
            logger.setLevel(numeric_level)
        else:
            consoleHandler = logging.StreamHandler()
            consoleHandler.setFormatter(logFormatter)
            logger.addHandler(consoleHandler)


def current_milli_time():
    return round(time.time() * 1000)


def sendaprs(ki, latitude, longitude, comment=b""):
    global last_tx_time_millis
    lat = geo_util.dec2dm_lat(latitude)
    lon = geo_util.dec2dm_lng(longitude)
    position = b"/" + aprstime() + lat + config.symbol['symboltable'] + lon + config.symbol['symbolcode']
    if comment:
        position = position + config.comment
    frame = Frame.ui(
        destination="APZ063",
        source=config.mycall,
        path=config.path,
        info=position,
    )
    logging.info(f"Frame : {frame}")
    ki.write(frame)
    last_tx_time_millis = current_milli_time()


def smartbeacon_decision(speed_kmh, turn_angle):
    global current_millis
    global last_tx_time_millis
    global rate
    global logger
    secs_since_beacon = (current_milli_time() - last_tx_time_millis) / 1000
    logger.info(f"Secs since last beacon: {secs_since_beacon:10.2f}")
    beacon_rate = rate['SB_BEACON_RATE']
    if speed_kmh < rate['SB_LOW_SPEED']:  # Stopped/very slow - slow rate beacon
        beacon_rate = rate['SB_SLOW_RATE']
        logger.info("SmartBeacon: Using Slow Rate")
    else:  # Moving - varies with speed
        if speed_kmh > rate['SB_HIGH_SPEED']:  # fast speed = fast rate beacon
            beacon_rate = rate['SB_FAST_RATE']
            logger.info("SmartBeacon: Using Fast Rate")
        else:  # Intermediate beacon rate
            beacon_rate = rate['SB_FAST_RATE'] * rate['SB_HIGH_SPEED'] / speed_kmh
            logger.info("SmartBeacon: Using Intermediate Rate")
    # Corner pegging - if not stopped
    if speed_kmh > 0:
        turn_threshold = rate['SB_TURN_MIN_ANGLE'] + rate['SB_TURN_SLOPE'] / speed_kmh  # turn threshold speed-dependent
        logger.info(f"turn_threshold : {turn_threshold:10.2f}°")
        if turn_angle > turn_threshold and secs_since_beacon > rate['SB_TURN_TIME']:
            logging.info("SmartBeacon: Requesting transmit (due to turn)")
            return True  # transmit beacon now
    if secs_since_beacon > beacon_rate:
        logger.info("SmartBeacon: Requesting transmit")
        return True  # send beacon and loop
    return False


def main(**kwargs):
    global MYCALL
    global speed
    global last_tx_time_millis
    global current_millis
    last_tx_time_millis = 0
    current_millis = current_milli_time()
    gps_fix = False
    latitude = 0.0
    longitude = 0.0
    ki = None
    global rate
    rate = constants.Suburban
    init_logging()
    if config.smartbeacon == 'Highway':
        rate = constants.Highway
    if config.smartbeacon == 'Cycling':
        rate = constants.Cycling
    if config.smartbeacon == 'Walking':
        rate = constants.Walking
    if config.smartbeacon == 'Sailing':
        rate = constants.Sailing
    try:
        if config.kiss['mode'] == 'KISS_TCP':
            host = config.kiss['host']
            port = config.kiss['port']
            ki = kiss.TCPKISS(host=host, port=port)
        elif config.kiss['mode'] == 'KISS_SERIAL':
            port = config.kiss['device']
            speed = config.kiss['speed']
            ki = kiss.SerialKISS(port=port, speed=speed)

        else:
            logger.critical(f'ERROR: Unknow KISS mode', config.kiss['mode'])
            sys.exit(1)
        ki.start(TX_DELAY=config.kissconfig['TX_DELAY'],
             PERSISTENCE=config.kissconfig['PERSISTENCE'],
             SLOT_TIME=config.kissconfig['SLOT_TIME'],
             TX_TAIL=config.kissconfig['TX_TAIL'],
             FULL_DUPLEX=config.kissconfig['FULL_DUPLEX'])
        if config.kiss['mode'] == 'KISS_SERIAL' and config.kiss['kisson']:
            logger.info('KISS ON')
            ki.kiss_on()
    except Exception as e:
        logging.critical(e)
        logging.critical("KISS connect call failed.Is your KISS modem started?")
        sys.exit(1)
    count = 0
    try:
        gps_port = config.gps['device']
        gps_baudrate = config.gps['baudrate']
        gps_timeout = float(config.gps['timeout'])
        timeisset = False
        try:
            with Serial(port=gps_port, baudrate=gps_baudrate, timeout=gps_timeout) as stream:
                nmr = NMEAReader(
                    stream, nmeaonly=False, quitonerror=False, errorhandler=errhandler)
                for raw, msg in nmr:
                    logger.debug(msg)
                    if not msg:
                        logger.debug("msg is empty")
                        continue
                    if msg.msgID == "GSA":
                        if msg.navMode == 1:
                            gps_fix = False
                            logger.info("GPS has no fix")
                            print("GPS has no fix")
                        else:
                            gps_fix = True
                    if msg.msgID == "GGA" and gps_fix:
                        if msg.lat == '' or msg.lon == '':
                            logger.error('msg.lat or msg.lon is empty string')
                            continue
                        try:
                            latitude = float(msg.lat)
                        except:
                            logger.critical(f"Cannot convert float from {latitude}")
                            logger.critical(f"Message  {msg}")
                            sys.exit(1)
                        try:
                            longitude = float(msg.lon)
                        except:
                            logger.critical(f"Cannot convert float from {longitude}")
                            logger.critical(f"Message  {msg}")
                            sys.exit(1)
                        logger.info(f"postion : {geo_util.dec2dm_lat(latitude)} - {geo_util.dec2dm_lng(longitude)}")
                    if msg.msgID == "RMC" and gps_fix:
                        print(msg.time)
                        print(msg.date)
                        if config.setsystemtime and timeisset == False:
                            setsystemtimefromgps(msg.date, msg.time)
                            timeisset = True
                        if msg.spd:
                            speed = float(msg.spd) * 1.852
                            logger.info(f"Speed : {speed:10.2f} km/h")
                        else:
                            speed = 0
                    count += 1
                    if gps_fix and smartbeacon_decision(speed, turn_angle) and latitude and longitude:
                        logger.info("Sending APRS beacon")
                        sendaprs(ki, latitude, longitude, config.comment)
                        last_tx_time_millis = current_milli_time()
        except Exception as e:
            logger.critical(e)
            sys.exit(1)

    except KeyboardInterrupt:
        print("\nCTRL + C pressed.\n")
        print("Program interrupted.")
    finally:
        if config.kiss['mode'] == 'KISS_SERIAL' and config.kiss['kisson']:
            logger.info('KISS OFF')
            ki.kiss_off()
        if count == 0:
            print("No messages read from GPS. Check connections")
            logger.debug("No messages read from GPS")
            exit(1)
        logger.info(f"\n{count} messages read.\n")


if __name__ == "__main__":
    main(**dict(arg.split("=") for arg in argv[1:]))
