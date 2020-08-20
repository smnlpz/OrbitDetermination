#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug  9 12:43:52 2020

@author: simon
"""

import numpy as np
from sympy import *
from astropy.coordinates import Angle
from astropy.time import Time
import astropy.units as u

import requests
from requests.exceptions import HTTPError

import csv

import sys

from newton import approximate_phi, isclose

from prueba import orbital_elements, plotOrbit


# Cte gravitación universal
G=6.67384*10**(-11)
# Masa solar
M=1.98847*10**(30)

mu=86400.0**2*G*M/149597870700.0**3

def toJulian(times):
	return times.jd

def toRadian(ang):
	return ang.radian

def toCartesian(ascension,declination):
	return np.array([np.cos(declination)*np.cos(ascension),
				     np.cos(declination)*np.sin(ascension),
					 np.sin(declination)])

def getE_C(coordinates,times):
	# Pasamos de coordenadas ecuatoriales a cartesianas
	# Almacenamos los vectores lambda_i,mu_i,nu_i en una lista 
	position=list()
	for coord in coordinates:
		position.append(toCartesian(toRadian(coord[0]),toRadian(coord[1])))
	
	velocity=np.zeros(3)
	second_deriv=np.zeros(3)
	for i in range(3):	
		# Dado que no sabemos si los intervalos son
		# equiespaciados, utilizamos la derivada del
		# polinomio de Lagrange
		velocity[i]=(2*times[1]-(times[1]+times[2]))/((times[0]-times[1])*(times[0]-times[2]))*position[0][i]+(2*times[1]-(times[2]+times[0]))/((times[1]-times[2])*(times[1]-times[0]))*position[1][i]+(2*times[1]-(times[0]+times[1]))/((times[2]-times[0])*(times[2]-times[1]))*position[2][i]
		second_deriv[i]=2/((times[0]-times[1])*(times[0]-times[2]))*position[0][i]+2/((times[1]-times[2])*(times[1]-times[0]))*position[1][i]+2/((times[2]-times[0])*(times[2]-times[1]))*position[2][i]
	
	# Solo nos interesa la posición en t_2, que es donde hemos
	# aproximado las derivadas
	return position[1],velocity,second_deriv




def getS_E(epoch):
	URL="https://ssd.jpl.nasa.gov/horizons_batch.cgi?batch=1&COMMAND='399'&CENTER='500@10'&MAKE_EPHEM='YES'&TABLE_TYPE='VECTORS'&TLIST='"+str(epoch)+"'&OUT_UNITS='AU-D'&REF_PLANE='ECLIPTIC'&REF_SYSTEM='J2000'&VECT_CORR='NONE'&VEC_LABELS='YES'&VEC_DELTA_T='NO'&CSV_FORMAT='YES'&OBJ_DATA='NO'&VEC_TABLE='3'"
	
	try:
		page = requests.get(URL)
		# If the response was successful, no Exception will be raised
		#page.raise_for_status()
	except HTTPError as http_err:
		print('HTTP error\n')
		print(http_err)
		sys.exit(0)
	except Exception as err:
		print('No es posible obtener los valores del vector SE (Sol-Tierra)\n')
		print(err)
		sys.exit(0)
	
	data = page.text[page.text.find('$$SOE\n')+len('$$SOE\n'):page.text.find('$$EOE')]
	
	lines = data.splitlines()
	reader = csv.reader(lines)
	row = list(reader)[0]
	
	position=np.array([float(row[2]),float(row[3]),float(row[4])])
	velocity=np.array([float(row[5]),float(row[6]),float(row[7])])
	R=float(row[9])
	
	second_deriv=-mu*position/R**3
	
	return position,velocity,second_deriv,R
	

def discuss_phi(phi_values,psi):
	index=-1
	print(phi_values)
	print(np.pi-psi)
	for i in range(len(phi_values)):
		if isclose(np.pi-psi,phi_values[i]):
			index=i
			break
		
	if index==0:
		print('No hay solución')
		return float('nan')
	if index==1:
		print('Solución única '+str(phi_values[0]))
		return phi_values[0]
	if index==2:
		print('Solución doble '+str(phi_values[0])+', '+str(phi_values[1]))
		print('Elija una de las dos (0 o 1):')
		selected=input()
		return phi_values[int(selected)]
	else:
		print('Error')
		return float('nan')
	
	
def get_rho_r(pos,vel,second_deriv,pos_sun,R):
	D_matrix=np.matrix([pos,vel,second_deriv])
	D_matrix=np.transpose(D_matrix)
	D=2*np.linalg.det(D_matrix)
	
	D1_matrix=np.matrix([pos,vel,pos_sun])
	D1_matrix=np.transpose(D1_matrix)
	D1=-2*mu*np.linalg.det(D1_matrix)
	
	psi=np.arccos(np.dot(pos_sun,pos)/R)

	idk=np.array([R*np.cos(psi)-D1/(D*R**3),R*np.sin(psi)])
	N=np.linalg.norm(idk)
	
	if (D1/D>0 and N>0) or (D1/D<0 and N<0):
		N=-N
	
	M=(-N*D*R**3*np.sin(psi)**3)/D1
	m=np.arcsin(R*np.sin(psi)/N)
		
	#m=np.arctan(R*np.sin(psi)/(R*np.cos(psi)-D1/(D*R**3)))
	#N=(R*np.sin(psi))/np.sin(m)
	phi_values=approximate_phi(M,m,plot=True)
	phi=discuss_phi(phi_values,psi)
	
	rho=R*np.sin(psi+phi)/np.sin(phi)
	r=R*np.sin(psi)/np.sin(phi)
	
	return rho,r

def getPosVel(pos,vel,second_deriv,rho,pos_sun,vel_sun,R,r):
	D_matrix=np.matrix([pos,vel,second_deriv])
	D_matrix=np.transpose(D_matrix)
	D=2*np.linalg.det(D_matrix)
	
	D2_matrix=np.matrix([pos,pos_sun,second_deriv])
	D2_matrix=np.transpose(D2_matrix)
	D2=-2*mu*np.linalg.det(D2_matrix)
	
	rho_deriv=D2/D*(1/R**3-1/r**3)	
	
	return rho*pos-pos_sun,rho_deriv*pos+rho*vel-vel_sun

def Laplace(coordinates, times):
	# Transformamos a días Julianos
	times=toJulian(times)
	
	# Pasamos de ascensión recta y declinación a cartesianas
	# Calculamos las derivadas (aproximadas)
	E_C,E_C_deriv,E_C_deriv_2=getE_C(coordinates,times)
	
	# Tomamos de la web de JPL el vector Sol-Tierra
	S_E,S_E_deriv,S_E_deriv_2,R=getS_E(times[1])	
	
	# Calculamos las distancias $\rho$ y $r$
	rho,r=get_rho_r(E_C,E_C_deriv,E_C_deriv_2,S_E,R)
	
	pos,vel=getPosVel(E_C,E_C_deriv,E_C_deriv_2,rho,S_E,S_E_deriv,R,r)
	
	return pos,vel
	





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
	Object=orbital_elements(r,v,name='Pluto')
	print(Object)
	
	plotOrbit(Object,True)
	
	
	
if __name__ == '__main__':
	main()
