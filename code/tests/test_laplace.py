#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 21 11:14:28 2020

@author: simon
"""


from astropy.coordinates import Angle
from astropy.time import Time

import os

os.chdir('..')

# Para modificar en ejecución el directorio desde el que importar
import sys
sys.path.insert(1, './scripts')

from laplace_method import Laplace
from orbital_elements import getOrbitalElements
from orbital_plot import plotOrbit
from error_rate import getApproximationError

sys.path.insert(1, './util')

import my_constants as const
from utilities import ICRS_to_ecliptic



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
	
	
	ascension_1=Angle('23 26 17.98 hours')
	declination_1=Angle('-04 49 41.3 degrees')
	t_1='2020-07-28 00:00'
	
	ascension_2=Angle('23 26 16.98 hours')
	declination_2=Angle('-04 49 48.3 degrees')
	t_2='2020-07-28 06:20'
	
	ascension_3=Angle('23 26 16.73 hours')
	declination_3=Angle('-04 49 50.0  degrees')
	t_3='2020-07-28 07:52'
	
	
	ascension_1=Angle('23 26 17.98 hours')
	declination_1=Angle('-04 49 41.3 degrees')
	t_1=2459058.5
	
	ascension_2=Angle('23 26 17.35 hours')
	declination_2=Angle('-04 49 45.7 degrees')
	t_2=2459058.666666667
	
	ascension_3=Angle('23 26 16.71 hours')
	declination_3=Angle('-04 49 50.2 degrees')
	t_3=2459058.833333333
	
	# Con estos valores, m=0.0030083783084677513
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
	
	
	# Neowise (El segundo funciona pero no plotea)
	'''
	ascension_1=Angle('11 51 12.49 hours')
	declination_1=Angle('+35 21 52.1 degrees')
	t_1=2459058.666666667
	
	ascension_2=Angle('11 59 29.02 hours')
	declination_2=Angle('+34 00 53.1 degrees')
	t_2=2459059.333333333
	
	ascension_3=Angle('12 12 44.30 hours')
	declination_3=Angle('+31 39 48.4 degrees')
	t_3=2459060.500000000
	
	ascension_1=Angle('14 18 02.55 hours')
	declination_1=Angle('-01 13 53.6 degrees')
	t_1=2459089.833333333
	
	ascension_2=Angle('14 18 57.96 hours')
	declination_2=Angle('-01 29 33.8 degrees')
	t_2=2459090.333333333
	
	ascension_3=Angle('14 20 10.65 hours')
	declination_3=Angle('-01 50 00.1 degrees')
	t_3=2459091.000000000 
	'''
	
	
	# Ceres (Funciona)
	
	ascension_1=Angle('23 13 15.59 hours')
	declination_1=Angle('-20 17 00.5 degrees')
	t_1=2459058.666666667
	
	ascension_2=Angle('23 13 01.31 hours')
	declination_2=Angle('-20 21 27.5 degrees')
	t_2=2459059.333333333
	
	ascension_3=Angle('23 12 34.89 hours')
	declination_3=Angle('-20 29 18.9 degrees')
	t_3=2459060.500000000
	
	
	# Pluto
	'''
	ascension_1=Angle('19 40 42.26 hours')
	declination_1=Angle('-22 27 23.7 degrees')
	t_1=2459058.666666667
	
	ascension_2=Angle('19 40 38.29 hours')
	declination_2=Angle('-22 27 36.7 degrees')
	t_2=2459059.333333333
	
	ascension_3=Angle('19 40 31.38 hours')
	declination_3=Angle('-22 27 59.2 degrees')
	t_3=2459060.500000000
	'''
	
	# Venus
	'''
	ascension_1=Angle('05 20 48.73 hours')
	declination_1=Angle('+18 55 07.9 degrees')
	t_1=2459058.666666667
	
	ascension_2=Angle('05 23 03.88 hours')
	declination_2=Angle('+18 58 56.9 degrees')
	t_2=2459059.333333333
	
	ascension_3=Angle('05 27 03.93 hours')
	declination_3=Angle('+19 05 30.7 degrees')
	t_3=2459060.500000000
	'''
	
	coordinates=list([(ascension_1,declination_1),
				      (ascension_2,declination_2),
					  (ascension_3,declination_3)])
	t=[t_1,t_2,t_3]
	
	if type(t_1) == str:
		times = Time(t, format='iso')
	else:
		times = Time(t, format='jd')
	
	# Obtenemos la posición y velocidad del objeto
	r,v=Laplace(coordinates,times)
	
	# Pasamos las coordenadas de ICRS a eclíptica
	r=ICRS_to_ecliptic(r)
	v=ICRS_to_ecliptic(v)
	
	# Comprobamos el error
	print(getApproximationError(r,v,t_2,'Ceres'))
	
	
	
	# Obtenemos los elementos orbitales
	Object=getOrbitalElements(r,v,name='Approximate Ceres')
	print('Elementos orbitales obtenidos:')
	print(Object)
	print(const.Ceres)
	print('')
	
	plotOrbit(list([Object,const.Ceres,const.Mars,const.Earth]))
	
	
	
if __name__ == '__main__':
	main()
