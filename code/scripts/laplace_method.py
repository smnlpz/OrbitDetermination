#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug  9 12:43:52 2020

@author: simon
"""

import numpy as np
from scipy.interpolate import lagrange

import requests
from requests.exceptions import HTTPError

import csv

from newton import approximate_phi

# Para modificar en ejecución el directorio desde el que importar
import sys
sys.path.insert(1, '../util')

import my_constants as const
from utilities import isclose



def toJulian(times):
	return times.jd

def toRadian(ang):
	return ang.radian

def toCartesian(ascension,declination):
	return np.array([np.cos(declination)*np.cos(ascension),
				     np.cos(declination)*np.sin(ascension),
					 np.sin(declination)])

def get_EC(coordinates,times):
	# Pasamos de coordenadas ecuatoriales a cartesianas
	# Almacenamos los vectores lambda_i,mu_i,nu_i en una lista 
	position=list()
	for coord in coordinates:
		position.append(toCartesian(toRadian(coord[0]),toRadian(coord[1])))
	position=np.array(position)

	velocity=np.zeros(3)
	second_deriv=np.zeros(3)
	
	for i in range(3):
		# Dado que no sabemos si los intervalos son
		# equiespaciados, utilizamos la derivada del
		# polinomio de Lagrange
		
		#velocity[i]=(2*times[1]-(times[1]+times[2]))/((times[0]-times[1])*(times[0]-times[2]))*position[0][i]+(2*times[1]-(times[2]+times[0]))/((times[1]-times[2])*(times[1]-times[0]))*position[1][i]+(2*times[1]-(times[0]+times[1]))/((times[2]-times[0])*(times[2]-times[1]))*position[2][i]
		#second_deriv[i]=2/((times[0]-times[1])*(times[0]-times[2]))*position[0][i]+2/((times[1]-times[2])*(times[1]-times[0]))*position[1][i]+2/((times[2]-times[0])*(times[2]-times[1]))*position[2][i]
		
		poly=lagrange(times, position[:,i])
		velocity[i]=poly.deriv(m=1)(times[1])
		second_deriv[i]=poly.deriv(m=2)(times[1])

	
	# Solo nos interesa la posición en t_2, que es donde hemos
	# aproximado las derivadas
	return position[1],velocity,second_deriv




def get_SE(epoch):
	URL="https://ssd.jpl.nasa.gov/horizons_batch.cgi?batch=1&COMMAND='10'&CENTER='500@399'&MAKE_EPHEM='YES'&TABLE_TYPE='VECTORS'&TLIST='"+str(epoch)+"'&OUT_UNITS='AU-D'&REF_PLANE='FRAME'&REF_SYSTEM='J2000'&VECT_CORR='NONE'&VEC_LABELS='YES'&VEC_DELTA_T='NO'&CSV_FORMAT='YES'&OBJ_DATA='NO'&VEC_TABLE='3'"
	
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
	
	second_deriv=-const.mu*position/R**3
	
	return position,velocity,second_deriv,R
	

def discuss_phi(phi_values,psi):
	index=-1
	print('\nPosibles phi = ' +str(phi_values))
	print(np.array(phi_values)*180/np.pi)
	print('psi = ' +str(psi)+' ('+str(psi*180/np.pi)+')')
	print('pi-psi = ' +str(np.pi-psi))
	print('')
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
	# En esta matriz introducimos los vectores por filas. Realmente
	# Deberían de ir por columnas, pero como vamos a calcular el
	# determinante no es necesario transponer
	D_matrix=np.matrix([pos,vel,second_deriv])
	D=2*np.linalg.det(D_matrix)
	
	D1_matrix=np.matrix([pos,vel,pos_sun])
	D1=-2*const.mu*np.linalg.det(D1_matrix)
	
	'''
	def hg(yz):
		y=yz[0]
		z=yz[1]
		
		h = y - D1/D * (1/R**3 - 1/z**3)
		g = z**2 - y**2 - R**2 - 2*y*R*cos_psi
		
		return np.array([h,g])
	
	from scipy.optimize import fsolve
	yz0 = np.array([20,1])
	yz = fsolve(hg,yz0)
	rho=yz[0]
	r=yz[1]
	print(rho)
	print(r)
	'''
	
	psi=np.arccos(np.dot(pos_sun,pos)/R)

	polares=np.array([R*np.cos(psi)-D1/(D*R**3),R*np.sin(psi)])
	N=np.linalg.norm(polares)
	
	if (D1/D>0 and N>0) or (D1/D<0 and N<0):
		N=-N
	
	print('\nD1 =' +str(D1)+' ; D = ' +str(D))
	M=(-N*D*R**3*np.sin(psi)**3)/D1
	print('M = ' +str(M))
	m=np.arcsin(R*np.sin(psi)/N)
	#m=np.arccos((R*np.cos(psi)-D1/(D*R**3))/N)
	print('m = ' +str(m))
	print('N = ' +str(N))
	print('')
	
	
	phi_values=approximate_phi(M,m,plot=True)
	phi=discuss_phi(phi_values,psi)	
	
	rho=R*np.sin(psi+phi)/np.sin(phi)	
	r=R*np.sin(psi)/np.sin(phi)
	
	print('Distancia al Sol = ' + str(r))
	print('Distancia a la Tierra = ' + str(rho))
	
	return rho,r

def getPosVel(pos,vel,second_deriv,rho,pos_sun,vel_sun,R,r):
	D_matrix=np.matrix([pos,vel,second_deriv])
	D=2*np.linalg.det(D_matrix)
	
	D2_matrix=np.matrix([pos,pos_sun,second_deriv])
	D2=-const.mu*np.linalg.det(D2_matrix)
	
	rho_deriv=D2/D*(1/R**3-1/r**3)
	#rho_deriv=-1.188525987011635E-02
	
	#print(rho*pos-pos_sun)
	#print(rho_deriv*pos+rho*vel-vel_sun)
	
	return rho*pos-pos_sun,rho_deriv*pos+rho*vel-vel_sun

def Laplace(coordinates, times):
	# Transformamos a días Julianos
	times=toJulian(times)
	
	# Pasamos de ascensión recta y declinación a cartesianas
	# Calculamos las derivadas (aproximadas)
	E_C,E_C_deriv,E_C_deriv_2=get_EC(coordinates,times)
	
	# Tomamos de la web de JPL el vector Sol-Tierra
	S_E,S_E_deriv,S_E_deriv_2,R=get_SE(times[1])	
	
	# Calculamos las distancias $\rho$ y $r$
	rho,r=get_rho_r(E_C,E_C_deriv,E_C_deriv_2,S_E,R)
	
	pos,vel=getPosVel(E_C,E_C_deriv,E_C_deriv_2,rho,S_E,S_E_deriv,R,r)
	
	
	#vel=np.array([5.865829038500923E-04,3.104449796577703E-03,-7.769220675952629E-05])
	
	return pos,vel
	

