#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 21 11:42:17 2020

@author: simon
"""

import numpy as np

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
	
