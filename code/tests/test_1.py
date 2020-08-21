#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 21 11:03:37 2020

@author: simon
"""

import numpy as np

# Para modificar en ejecución el directorio desde el que importar
import sys
sys.path.insert(1, '../scripts')

from orbital_elements import getOrbitalElements
from orbital_plot import plotOrbit

sys.path.insert(1, '../utils')

import my_constants as const


def main():	
	'''
	# Marte
	# 2020-Jul-28 00:00:00.0000
	# Coordinate Origin [change] : 	Sun (body center) [500@10]
	X = 1.220019371704684E+00
	Y =-6.470577187040094E-01
	Z =-4.348794194489423E-02
	VX= 7.090666373969929E-03
	VY= 1.355900871701440E-02
	VZ= 1.101801802943566E-04
	'''
	
	'''
	# Urano
	# 2020-Jul-28 00:00:00.0000
	# Coordinate Origin [change] : 	Sun (body center) [500@10]
	X = 1.573553246967107E+01
	Y = 1.200453525995092E+01
	Z =-1.592451238694909E-01
	VX=-2.407903101224412E-03
	VY= 2.946972796014599E-03
	VZ= 4.194955948634716E-05
	'''
	
	'''
	# C/2020 F3 (Neowise)
	# 2020-Jul-28 00:00:00.0000
	# Coordinate Origin [change] : 	Sun (body center) [500@10]
	X =-4.313004534071243E-03
	Y =-6.365798630096369E-01
	Z = 3.771839684898292E-01
	VX=-1.320373168048227E-02
	VY=-2.498337721153771E-02
	VZ= 6.922421576828086E-04
	'''
	
	X = 1.359741522403668E+01
	Y =-3.125322406604633E+01
	Z =-5.881149104622369E-01
	VX= 2.950200674787515E-03
	VY= 5.745585982807115E-04
	VZ=-9.180472035906128E-04
	
	
	r=np.array([X,Y,Z])
	v=np.array([VX,VY,VZ])
	
	Pluto=getOrbitalElements(r,v,name='Pluto')
	print(Pluto)
	orbits=list([Pluto,const.Saturn,const.Jupiter])
	
	plotOrbit(orbits,True)
	
if __name__ == '__main__':
	main()

