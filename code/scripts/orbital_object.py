#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 21 11:36:56 2020

@author: simon
"""

import numpy as np
from astropy import units as u
from astropy.coordinates import Angle

class OrbitalObject:
	def __init__(self,name,a,e,i,Omega,omega,p,degree=False):
		angle_unit=u.radian
		if degree:
			angle_unit=u.deg
			
		self.name=name
		self.a=a
		self.e=e
		self.i=Angle(i, angle_unit).rad
		self.Omega=Angle(Omega, angle_unit).rad
		self.omega=Angle(omega, angle_unit).rad
		self.p=p

	def getDegAngles(self):
		conv=180/np.pi
		return list([self.i*conv, self.Omega*conv, self.omega*conv])
	
	def getName(self):
		return self.name
	
	def __str__(self):
		deg_angles=self.getDegAngles()
		return '(\''+str(self.name)+'\', '+str(self.a)+', '+str(self.e)+', '+str(deg_angles[0])+', '+str(deg_angles[1])+', '+str(deg_angles[2])+', '+str(self.p)+')'
