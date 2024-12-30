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


"""
Callsign of the tracker with or without SSID
"""
from os import MFD_ALLOW_SEALING

mycall = "N0CALL-9"

""" 
Serial GPS setting
device: the device where GPS is attached
baudrate: GPS baudrate
timeout: timeout for reading
"""

gps = dict(
    device = '/dev/ttyGPS',
    baudrate = 4800,
    timeout = 3
)
"""
KISS setting
mode: must be KISS_TCP or KISS_SERIAL
    KISS_TCP can be use with Direwolf, Soundmodem or WinRPR modem
    KISS_SERIAL can be use with a KISS TNC or other modem set in KISS mode
host: must be the address or name of the machine hosting the modem. This configuration parameter is ignored in "KISS_SERIAL"
port: must be the port where the modem is listening. This configuration parameter is ignored in "KISS_SERIAL"
device: The device where the serial modem is attached. This configuration parameter is ignored in "KISS_STCP"
speed: The serial modem speed. This configuration parameter is ignored in "KISS_TCP"
"""

kiss = dict(
    mode='KISS_TCP',
    host='localhost',
    port="8002",
    device='/dev/ttyPTT',
    speed=9600,
    kisson = True
)
"""
KISS  Command Codes sent at startup to attached device.
    see http://en.wikipedia.org/wiki/KISS_(TNC)#Command_Codes
"""
kissconfig = dict(
    TX_DELAY = 40,
    PERSISTENCE = 63,
    SLOT_TIME = 20,
    TX_TAIL = 30,
    FULL_DUPLEX = 0,
)

""" 
APRS SYMBOL
see http://www.aprs.org/symbols/symbolsX.txt or https://blog.thelifeofkenneth.com/2017/01/aprs-symbol-look-up-table.html for a list
    symboltable: Symbol table
    symbolcode: Symbol code from table
these settings are bytes don't remove "b" before the string
"""
symbol = dict(
    symboltable = b'/',
    symbolcode = b'>'
)
''' 
Beacon comment 
    can be empty
this setting is bytes don't remove "b" before the string    
'''
comment = b'En route!'

"""
APRS path
an array of path 
"""
path=["WIDE1-1", "WIDE2-2"]

"""
Smartbeacon model
choose between Suburban, Highway, Cycling, Walking or Sailing
see file constants.py for values and description
"""
smartbeacon = "Suburban"

"""
debug
    debug: debug if True
    logfile: log to file if true filename is ddmmyyyy.log
    logfilepath: path to the loggin folder
    loglevel: must be
        DEBUG  for detailed information, typically of interest only when diagnosing problems.
        INFO   for confirmation that things are working as expected.
        WARNING for indication that something unexpected happened, or indicative of some problem in the near future (e.g. ‘disk space low’). The software is still working as expected.
        ERROR Due to a more serious problem, the software has not been able to perform some function.
        CRITICAL A serious error, indicating that the program itself may be unable to continue running.
"""
debug = dict(
    debug=False,
    logfile = False,
    logfilepath = "./",
    loglevel = "INFO"
)





