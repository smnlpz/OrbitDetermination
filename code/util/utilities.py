#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 21 11:42:17 2020

@author: simon
"""

import numpy as np

import requests
from requests.exceptions import HTTPError

import csv

import sys

import my_constants as const

def isclose(a, b, rel_tol=1e-06, abs_tol=0.0):
	'''
	rel_tol is a relative tolerance, it is multiplied by
	the greater of the magnitudes of the two arguments;
	as the values get larger, so does the allowed difference
	between them while still considering them equal.
	
	abs_tol is an absolute tolerance that is applied as-is in 
	all cases. If the difference is less than either of 
	those tolerances, the values are considered equal.
	'''
	return abs(a-b) <= max(rel_tol * max(abs(a), abs(b)), abs_tol)

def reduce_to_0_2pi(x):
	'''
	Parameters
	----------
	x : float
		Ángulo en radianes en \mathbb{R}

	Returns
	-------
	x : float
		Ángulo en radianes en [0,2\pi]
	'''
	
	while x<0 or x>2*np.pi:
		if x<0:
			x+=2*np.pi
		else:
			x-=2*np.pi
	return x

def ICRS_to_ecliptic(pos):
	'''
	Parameters
	----------
	pos : np.array
	      Vector (x,y,z) en el sistema de coordenadas ICRF

	Returns
	-------
	tmp : np.array
	      Vector (x,y,z) en el sistema de coordenadas de la eclítpica
	'''
	x=pos[0]
	y=pos[1]*np.cos(const.mean_obliquity)+pos[2]*np.sin(const.mean_obliquity)
	z=-pos[1]*np.sin(const.mean_obliquity)+pos[2]*np.cos(const.mean_obliquity)
	return np.array([x,y,z])
	

def getVectorsFromEphemeris(name, epoch, center='Sun', ref_plane='ECLIPTIC'):
	'''
	Parameters
	----------
	name : 	 	str
				Nombre del cuerpo a buscar en la efemérides
	epoch : 	float
				Dia juliano en el que buscar en la efemérides
	center : 	str
				Nombre desde donde se ve el objeto
	ref_plane : str
				Plano de referencia para tomar los valores
	
	Returns
	-------
	(pos, vel, R) : (np.array, np.array, float)
					Posición, velocidad y distancia del cuerpo
	'''
	
	if center=='Sun':
		center='500@10'
	elif center=='Earth':
		center='500@399'
	
	URL="https://ssd.jpl.nasa.gov/horizons_batch.cgi?batch=1&"
	URL+="COMMAND='"+name+"'&"
	URL+="CENTER='"+center+"'&"
	URL+="TLIST='"+str(epoch)+"'&"
	URL+="REF_PLANE='"+ref_plane+"'&"
	URL+="MAKE_EPHEM='YES'&TABLE_TYPE='VECTORS'&OUT_UNITS='AU-D'&REF_SYSTEM='J2000'&VECT_CORR='NONE'&VEC_LABELS='YES'&VEC_DELTA_T='NO'&CSV_FORMAT='YES'&OBJ_DATA='NO'&VEC_TABLE='3'"
	
	try:
		page = requests.get(URL)
		# If the response was successful, no Exception will be raised
		#page.raise_for_status()
	except HTTPError as http_err:
		print('HTTP error\n')
		print(http_err)
		sys.exit(0)
	except Exception as err:
		print('No es posible obtener los valores del vector\n')
		print(err)
		sys.exit(0)
	
	data = page.text[page.text.find('$$SOE\n')+len('$$SOE\n'):page.text.find('$$EOE')]
	
	lines = data.splitlines()
	reader = csv.reader(lines)
	row = list(reader)[0]
	
	pos=np.array([float(row[2]),float(row[3]),float(row[4])])
	vel=np.array([float(row[5]),float(row[6]),float(row[7])])
	
	return pos, vel
