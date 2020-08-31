#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 21 11:14:28 2020

@author: simon
"""


from astropy.coordinates import Angle
from astropy.time import Time

# Para modificar en ejecución el directorio desde el que importar
import sys
sys.path.insert(1, '../scripts')

from laplace_method import Laplace
from orbital_elements import getOrbitalElements
from orbital_plot import plotOrbit

sys.path.insert(1, '../util')

import my_constants as const



def main():
	# NEPTUNE
	
	'''
	ascension_1=Angle('23 24 35.15 hours')
	declination_1=Angle('-05 01 22.3 degrees')
	t_1='2020-08-19 00:00'
	
	ascension_2=Angle('23 24 30.99 hours')
	declination_2=Angle('-05 01 50.1 degrees')
	t_2='2020-08-19 18:20'
	
	ascension_3=Angle(' 23 24 29.24 hours')
	declination_3=Angle('-05 02 01.8  degrees')
	t_3='2020-08-20 02:00'
	'''
	
	
	# Con estos valores m=0.1295350258220578, y dicho valor es erróneo
	# ya que obtenemos solución única que al utilizarla para calcular
	# $\rho$ y $r$ nos da un valor que no se corresponde al real
	'''
	ascension_1=Angle('23 26 17.98 hours')
	declination_1=Angle('-04 49 41.3 degrees')
	t_1='2020-07-28 00:00'
	
	ascension_2=Angle('23 26 16.98 hours')
	declination_2=Angle('-04 49 48.3 degrees')
	t_2='2020-07-28 06:20'
	
	ascension_3=Angle('23 26 16.73 hours')
	declination_3=Angle('-04 49 50.0  degrees')
	t_3='2020-07-28 07:52'
	'''
	
	# Con estos valores, m=-0.034911329608047485, solución válida,
	# pero obtenemos una solución doble
	'''
	ascension_1=Angle('23 26 17.98 hours')
	declination_1=Angle('-04 49 41.3 degrees')
	t_1=2459058.5
	
	ascension_2=Angle('23 26 17.35 hours')
	declination_2=Angle('-04 49 45.7 degrees')
	t_2=2459058.666666667
	
	ascension_3=Angle('23 26 16.71 hours')
	declination_3=Angle('-04 49 50.2 degrees')
	t_3=2459058.833333333
	'''
	
	# Con estos valores, m=0.0030083783084677513
	'''
	ascension_1=Angle('23 26 17.98 hours')
	declination_1=Angle('-04 49 41.3 degrees')
	t_1=2459058.5
	
	ascension_2=Angle('23 26 14.15 hours')
	declination_2=Angle('-04 50 08.1 degrees')
	t_2=2459059.5 # 29 de julio 00:00
	
	ascension_3=Angle('23 26 10.22 hours')
	declination_3=Angle('-04 50 35.5 degrees')
	t_3=2459060.5 # 30 de julio 00:00
	'''
	
	
	
	# MARTE
	'''
	ascension_1=Angle('01 05 07.40 hours')
	declination_1=Angle('+02 51 32.4 degrees')
	t_1=2459058.500000000
	
	ascension_1=Angle('15 43 47.21 hours')
	declination_1=Angle('-19 23 07.0 degrees')
	t_1=2458849.500000000
	
	ascension_2=Angle('01 06 00.31 hours')
	declination_2=Angle('+02 56 19.4  degrees')
	t_2=2459059.000000000
	
	ascension_3=Angle('01 06 35.38 hours')
	declination_3=Angle('+02 59 29.4 degrees')
	t_3=2459059.333333333
	'''
	
	'''
	ascension_1=Angle('15 43 47.21 hours')
	declination_1=Angle('-19 23 07.0 degrees')
	t_1=2458849.500000000 
	
	ascension_2=Angle('15 43 49.52 hours')
	declination_2=Angle('-19 23 15.0  degrees')
	t_2=2458849.513888889
	
	ascension_3=Angle('15 43 51.83 hours')
	declination_3=Angle('-19 23 22.9 degrees')
	t_3=2458849.527777778
	'''
	
	# Saturno
	'''
	ascension_1=Angle('19 59 52.46 hours')
	declination_1=Angle('-20 49 49.6 degrees')
	t_1=2459058.500000000
	
	ascension_2=Angle('19 59 40.26 hours')
	declination_2=Angle('-20 50 27.7  degrees')
	t_2=2459059.166666667
	
	ascension_3=Angle('19 59 19.00 hours')
	declination_3=Angle('-20 51 33.9 degrees')
	t_3=2459060.333333333
	'''
	
	
	# Halley
	'''
	ascension_1=Angle('08 21 57.94 hours')
	declination_1=Angle('+02 52 02.3 degrees')
	t_1=2459058.666666667
	
	ascension_2=Angle('08 22 02.02 hours')
	declination_2=Angle('+02 51 47.8 degrees')
	t_2=2459059.333333333
	
	ascension_3=Angle('08 22 09.14 hours')
	declination_3=Angle('+02 51 21.9 degrees')
	t_3=2459060.500000000
	'''
	
	# Neowise
	ascension_1=Angle('11 51 12.49 hours')
	declination_1=Angle('+35 21 52.1 degrees')
	t_1=2459058.666666667
	
	ascension_2=Angle('11 59 29.02 hours')
	declination_2=Angle('+34 00 53.1 degrees')
	t_2=2459059.333333333
	
	ascension_3=Angle('12 12 44.30 hours')
	declination_3=Angle('+31 39 48.4 degrees')
	t_3=2459060.500000000
	
	
	
	coordinates=list([(ascension_1,declination_1),
				      (ascension_2,declination_2),
					  (ascension_3,declination_3)])
					  #(ascension_4,declination_4),
					  #(ascension_5,declination_5)])
	t=[t_1,t_2,t_3]
	
	if type(t_1) == str:
		times = Time(t, format='iso')
	else:
		times = Time(t, format='jd')
	
	r,v=Laplace(coordinates,times)
	Object=getOrbitalElements(r,v,name='Approximate Mars')
	print('Elementos orbitales obtenidos:')
	print(Object)
	print('')
	
	#plotOrbit(list([Object,const.Mars,const.Earth]))
	
	
	
if __name__ == '__main__':
	main()
