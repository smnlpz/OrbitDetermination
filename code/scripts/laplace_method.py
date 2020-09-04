#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug  9 12:43:52 2020

@author: simon
"""

import numpy as np
from scipy.interpolate import lagrange

from newton import approximate_phi

# Para modificar en ejecución el directorio desde el que importar
import sys
sys.path.insert(1, './util')

import my_constants as const
from utilities import isclose, getVectorsFromEphemeris


def toRadian(ang):
	# Pasamos una lista de coordenadas ecuatoriales en horas y grados
	# y la devuelve en radianes
	rad=list()
	for a in ang:
		rad.append((a[0].radian,a[1].radian))
		
	return rad

def toCartesian(coordinates):
	# Pasamos de coordenadas ecuatoriales a cartesianas
	# Almacenamos los vectores lambda_i,mu_i,nu_i en una lista 
	position=list()
	for coord in coordinates:
		tmp = np.array([np.cos(coord[1])*np.cos(coord[0]),
				        np.cos(coord[1])*np.sin(coord[0]),
						np.sin(coord[1])])
		position.append(tmp)
	
	# Devolvemos el resultado como un np.array
	return np.array(position)

def toJulian(times):
	return times.jd


def approximateDeriv(position,times):
	velocity=np.zeros(3)
	second_deriv=np.zeros(3)
	
	for i in range(3):
		# Dado que no sabemos si los intervalos son
		# equiespaciados, utilizamos la derivada del
		# polinomio de Lagrange
		
		poly=lagrange(times, position[:,i])
		velocity[i]=poly.deriv(m=1)(times[1])
		second_deriv[i]=poly.deriv(m=2)(times[1])

	
	# Solo nos interesa la posición en t_2, que es donde hemos
	# aproximado las derivadas
	return position[1],velocity,second_deriv



def vectorSE(epoch):
	position,velocity,result=getVectorsFromEphemeris(name='Sun',center='Earth',epoch=epoch,ref_plane='FRAME')
	
	R=np.linalg.norm(position)
	second_deriv=-const.mu*position/R**3
	
	return position,velocity,second_deriv,R
	

def discuss_phi(phi_values,psi):
	index=-1
	print('\nPosibles φ:\n' +str(phi_values))
	print('En grados:\n' +str(np.array(phi_values)*180/np.pi))
	print('\nψ = ' +str(psi)+' ('+str(psi*180/np.pi)+')')
	print('π-ψ = ' +str(np.pi-psi)+' ('+str((np.pi-psi)*180/np.pi)+')')
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
	
	psi=np.arccos(np.dot(pos_sun,pos)/R)

	polares=np.array([R*np.cos(psi)-D1/(D*R**3),R*np.sin(psi)])
	N=np.linalg.norm(polares)
	
	if (D1/D>0 and N>0) or (D1/D<0 and N<0):
		N=-N
	
	M=(-N*D*R**3*np.sin(psi)**3)/D1
	m=np.arcsin(R*np.sin(psi)/N)
	
	'''
	print('\nD1 =' +str(D1)+' ; D = ' +str(D))
	print('M = ' +str(M))
	print('m = ' +str(m))
	print('N = ' +str(N))
	print('')
	'''
	
	phi_values=approximate_phi(M,m,plot=False)
	phi=discuss_phi(phi_values,psi)	
	
	rho=R*np.sin(psi+phi)/np.sin(phi)	
	r=R*np.sin(psi)/np.sin(phi)
	
	'''
	print('Distancia al Sol = ' + str(r))
	print('Distancia a la Tierra = ' + str(rho))
	'''
	
	return rho,r

def getPosVel(pos,vel,second_deriv,pos_sun,vel_sun,R,r,rho):
	D_matrix=np.matrix([pos,vel,second_deriv])
	D=2*np.linalg.det(D_matrix)
	
	D2_matrix=np.matrix([pos,pos_sun,second_deriv])
	D2=-const.mu*np.linalg.det(D2_matrix)
	
	rho_deriv=D2/D*(1/R**3-1/r**3)
		
	return rho*pos-pos_sun,rho_deriv*pos+rho*vel-vel_sun

def Laplace(coordinates, times):	
	# Transformamos a cartesianas los ángulos en radianes
	position=toCartesian(toRadian(coordinates))
	
	# Transformamos a días Julianos
	times=toJulian(times)
	
	# Pasamos de ascensión recta y declinación a cartesianas
	# Calculamos las derivadas (aproximadas)
	E_C,E_C_deriv,E_C_deriv_2=approximateDeriv(position,times)
	
	# Tomamos de la web de JPL el vector Tierra-Sol
	S_E,S_E_deriv,S_E_deriv_2,R=vectorSE(times[1])	
	
	# Calculamos las distancias $\rho$ y $r$
	rho,r=get_rho_r(E_C,E_C_deriv,E_C_deriv_2,S_E,R)
	
	# Obtenemos los vectores de posición y velocidad
	pos,vel=getPosVel(E_C,E_C_deriv,E_C_deriv_2,S_E,S_E_deriv,R,r,rho)
	
	return pos,vel
	

