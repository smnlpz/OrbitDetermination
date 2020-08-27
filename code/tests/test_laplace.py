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
	
	coordinates=list([(ascension_1,declination_1),(ascension_2,declination_2),(ascension_3,declination_3)])
	t=[t_1,t_2,t_3]
	times = Time(t, format='jd')
	
	r,v=Laplace(coordinates,times)
	Object=getOrbitalElements(r,v,name='Pluto')
	print('Elementos orbitales obtenidos:')
	print(Object)
	print('')
	
	plotOrbit(Object)
	
	
	
if __name__ == '__main__':
	main()
