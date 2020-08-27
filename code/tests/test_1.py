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
	
	# Urano
	# 2020-Jul-28 00:00:00.0000
	# Coordinate Origin [change] : 	Sun (body center) [500@10]
	X = 1.573553246967107E+01
	Y = 1.200453525995092E+01
	Z =-1.592451238694909E-01
	VX=-2.407903101224412E-03
	VY= 2.946972796014599E-03
	VZ= 4.194955948634716E-05
	
	r=np.array([X,Y,Z])
	v=np.array([VX,VY,VZ])
	
	Uranus=getOrbitalElements(r,v,name='Uranus')
	print(Uranus)
	
	
	
	# Pluto (134340)
	# 2020-Aug-19 03:00:00.0000
	# Coordinate Origin [change] : 	Sun (body center) [500@10]
	X = 1.366284276939564E+01
	Y =-3.124021192243405E+01
	Z =-6.083561990226184E-01
	VX= 2.963878185732496E-03
	VY= 6.017113459089684E-04
	VZ=-9.111348138954932E-04
	
	r=np.array([X,Y,Z])
	v=np.array([VX,VY,VZ])
	
	Pluto=getOrbitalElements(r,v,name='Pluto')
	print(Pluto)
	
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
	
	# Comet 1P/Halley
	# 2020-Aug-19 01:20:00.0000
	# Coordinate Origin [change] : 	Sun (body center) [500@10]
	X =-2.025155302422777E+01
	Y = 2.671705015412066E+01
	Z =-9.978044112706311E+00
	VX= 2.573598999305888E-04
	VY= 5.427428636675992E-04
	VZ=-2.100916318710593E-05
	
	r=np.array([X,Y,Z])
	v=np.array([VX,VY,VZ])
	
	Halley=getOrbitalElements(r,v,name='Halley')
	print(Halley)
	
	
	
	orbits=list([Uranus,Pluto, Halley,const.Saturn,const.Jupiter,const.Neptune])
	
	plotOrbit(orbits)
	
if __name__ == '__main__':
	main()

