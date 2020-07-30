#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 30 12:08:44 2020

@author: simon
"""

from orbital import earth, uranus, KeplerianElements, Maneuver, plot3d, mars, saturn

from scipy.constants import kilo
import matplotlib.pyplot as plt

orbit = KeplerianElements(1000 * kilo, body=earth)
man = Maneuver.hohmann_transfer_to_altitude(10000 * kilo)
print(orbit)
plot3d(orbit, title='Maneuver 1', maneuver=man)
plt.show()