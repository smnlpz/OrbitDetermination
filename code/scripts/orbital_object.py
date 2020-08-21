#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 21 11:36:56 2020

@author: simon
"""

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
		
	def toRad(self):
		self.i=self.i.rad
		self.Omega=self.Omega.rad
		self.omega=self.omega.rad
		
	def toDeg(self):
		self.i=self.i.deg
		self.Omega=self.Omega.deg
		self.omega=self.omega.deg	
		
	def getName(self):
		return self.name
	
	def __str__(self):
		return '(\''+str(self.name)+'\', '+str(self.a)+', '+str(self.e)+', '+str(self.i)+', '+str(self.Omega)+', '+str(self.omega)+', '+str(self.p)+')'
