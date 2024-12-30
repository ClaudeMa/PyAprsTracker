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
Constants description
    SB_LOW_SPEED     Below this speed, assume stationary, beacon at slow rate (km/h)
    SB_SLOW_RATE     number of seconds interval between beacons at slow rate (i.e. when stopped)
    SB_HIGH_SPEED    Above this speed beacon at fast rate (km/h)
    SB_FAST_RATE     Fast beacon interval (sec)
    SB_TURN_MIN_ANGLEIf turn is greater than this angle then beacon (subject to speed) (degrees)
    SB_TURN_SLOPE    This number, divided by speed, is added to SB_TURN_MIN_ANGLE to calculate at-speed turn beaconing
    SB_TURN_TIME     Minimum beacon interval during turn
"""
Suburban = {'SB_LOW_SPEED': 10, 'SB_SLOW_RATE': 600, 'SB_HIGH_SPEED': 80, 'SB_FAST_RATE': 20, 'SB_TURN_MIN_ANGLE': 20,
            'SB_TURN_SLOPE': 180, 'SB_TURN_TIME': 30, 'SB_BEACON_RATE': 300}

Highway = {'SB_LOW_SPEED': 10, 'SB_SLOW_RATE': 900, 'SB_HIGH_SPEED': 120, 'SB_TURN_MIN_ANGLE': 28,
                     'SB_TURN_SLOPE': 26, 'SB_TURN_TIME': 30, 'SB_FAST_RATE': 60}
Cycling = {'SB_LOW_SPEED': 3, 'SB_SLOW_RATE': 600, 'SB_HIGH_SPEED': 24, 'SB_FAST_RATE': 90, 'SB_TURN_MIN_ANGLE': 15,
            'SB_TURN_SLOPE': 24, 'SB_TURN_TIME': 15}

Walking = {'SB_LOW_SPEED': 2, 'SB_SLOW_RATE': 120, 'SB_HIGH_SPEED': 10, 'SB_FAST_RATE': 60, 'SB_TURN_MIN_ANGLE': 30,
            'SB_TURN_SLOPE': 24, 'SB_TURN_TIME': 30}

Sailing = {'SB_LOW_SPEED': 2, 'SB_SLOW_RATE': 180, 'SB_HIGH_SPEED': 15, 'SB_FAST_RATE': 90, 'SB_TURN_MIN_ANGLE': 45,
            'SB_TURN_SLOPE': 25, 'SB_TURN_TIME': 15}
 

