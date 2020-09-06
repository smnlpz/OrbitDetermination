#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 30 12:08:44 2020

@author: simon
"""

import numpy as np
from orbital_object import OrbitalObject


# Para modificar en ejecución el directorio desde el que importar
import sys
sys.path.insert(1, '../util')

import my_constants as const



def getOrbitalElements(x,vx,name='NotAssigned'):
	x_norm=np.linalg.norm(x)
	vx_norm=np.linalg.norm(vx)
	
	# Calculamos la energía, y con ella el semieje mayor
	h=(vx_norm*vx_norm)/2 - const.mu/x_norm
	a=-const.mu/(2*h)
	
	# Calculamos el momento angular y el vector de excentricidad, cuya
	# norma nos proporciona la excentricidad de la órbita
	c=np.cross(x,vx)
	e_vec=-x/x_norm-1/const.mu*(np.cross(c,vx))
	e=np.linalg.norm(e_vec)
	
	# Obtenemos el período orbital
	p=2*np.pi/np.sqrt(const.mu)*a**(3/2)
	
	# Calculamos la inclinación, el nodo ascendente y el argumento
	# del periastro
	nodo_asc=np.cross([0,0,1],c)
	i=np.arccos(np.dot(np.array([0,0,1]),c)/(np.linalg.norm(c)))
	Omega=np.arccos(np.dot(np.array([1,0,0]),nodo_asc)/(np.linalg.norm(nodo_asc)))
	omega=np.arccos(np.dot(nodo_asc,e_vec)/(np.linalg.norm(nodo_asc)*e))
	
	# Corregimos el valor de omega
	if e_vec[2]<0:
		omega = 2*np.pi-omega
	
	
	orbital = OrbitalObject(name=name,a=a,e=e,i=i,Omega=Omega,omega=omega,p=p)
	
	return orbital

	