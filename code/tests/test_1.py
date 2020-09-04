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

sys.path.insert(1, '../util')

import my_constants as const


def main():	
	# C/2020 F3 (Neowise)
	# 2020-Jul-28 00:00:00.0000
	# Coordinate Origin [change] : 	Sun (body center) [500@10]
	X =-4.313004534071243E-03
	Y =-6.365798630096369E-01
	Z = 3.771839684898292E-01
	VX=-1.320373168048227E-02
	VY=-2.498337721153771E-02
	VZ= 6.922421576828086E-04
	
	r=np.array([X,Y,Z])
	v=np.array([VX,VY,VZ])
	
	Neowise=getOrbitalElements(r,v,name='Neowise')
	print(Neowise)
	
	
	# Pluto (134340)
	# 2020-Jul-30 00:00:00
	# Coordinate Origin [change] : 	Sun (body center) [500@10]
	X = 1.360331705206759E+01
	Y =-3.125206011232465E+01
	Z =-5.899308701769594E-01
	VX= 2.957116648122905E-03
	VY= 5.918881094962256E-04
	VZ=-9.034849073268278E-04
	
	r=np.array([X,Y,Z])
	v=np.array([VX,VY,VZ])
	
	Pluto=getOrbitalElements(r,v,name='Pluto')
	print(Pluto)
	
	
	# Comet 1P/Halley
	# 2020-Jul-30 00:00:00
	# Coordinate Origin [change] : 	Sun (body center) [500@10]
	X =-2.025668768956410E+01
	Y = 2.670613007527469E+01
	Z =-9.977608854116756E+00
	VX= 2.546850007825364E-04
	VY= 5.462369075113827E-04
	VZ=-2.239645875253460E-05
	
	r=np.array([X,Y,Z])
	v=np.array([VX,VY,VZ])
	
	Halley=getOrbitalElements(r,v,name='Halley')
	print(Halley)
	
	
	r=np.array([ 2.53436621,-1.48439324,-0.51379219])
	v=np.array([ 0.00478149,0.00826443,-0.0006202 ])
	
	Ceres=getOrbitalElements(r,v,name='Ceres')
	print(Ceres)
	
	
	orbits=list([const.Earth, Neowise, Halley, Pluto])
	plotOrbit(orbits,sun_center=False)
	
if __name__ == '__main__':
	main()

