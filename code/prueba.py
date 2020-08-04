#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 30 12:08:44 2020

@author: simon
"""


import time
import numpy as np

G=6.67384*10**(-11)
M=1.98847*10**(30)



def orbital_elements(x,vx):
	x_norm=np.linalg.norm(x)
	vx_norm=np.linalg.norm(vx)
	
	# El valor de mu está en m^3*s^-2, mientras que x y vx están en
	# au y au/day respectivamente. Hacemos la conversión:
	mu=G*M
	mu=86400.0**2*mu/149597870700.0**3	
	
	# Calculamos la energía, y con ella el semieje mayor
	h=(vx_norm*vx_norm)/2 - mu/x_norm
	a=-mu/(2*h)
	
	# Calculamos el momento angular y el vector de excentricidad, cuya
	# norma nos proporciona la excentricidad de la órbita
	c=np.cross(x,vx)
	e_vec=-x/x_norm-1/mu*(np.cross(c,vx))
	e=np.linalg.norm(e_vec)
	
	# Obtenemos el período orbital
	p=2*np.pi/np.sqrt(mu)*a**(3/2)
	
	# Calculamos la inclinación, el nodo ascendente y el argumento
	# del perihelio
	nodo_asc=np.cross([0,0,1],c)
	i=np.arccos(np.dot(np.array([0,0,1]),c)/np.linalg.norm(c))
	Omega=np.arccos(np.dot(np.array([1,0,0]),nodo_asc)/np.linalg.norm(nodo_asc))
	omega=np.arccos(np.dot(e_vec,nodo_asc)/np.linalg.norm(nodo_asc)*e)
	
	'''
	if c[1]<0:
		Omega = 2*np.pi-Omega
	if e_vec[2]<0:
		omega = 2*np.pi-omega
	'''
	
	# Factor de conversión para pasar de radianes a grados
	conversion=360/(2*np.pi)
	#conversion=1
	
	return(a,e,i*conversion, Omega*conversion, omega*conversion, p)





def main():
	'''
	# Marte
	# 2020-Jul-28 00:00:00.0000
	# Coordinate Origin [change] : 	Sun (body center) [500@10]
	X = 1.220019371704684E+00
	Y =-6.470577187040094E-01
	Z =-4.348794194489423E-02
	VX= 7.090666373969929E-03
	VY= 1.355900871701440E-02
	VZ= 1.101801802943566E-04
	'''
	
	'''
	# Urano
	# 2020-Jul-28 00:00:00.0000
	# Coordinate Origin [change] : 	Sun (body center) [500@10]
	X = 1.573553246967107E+01
	Y = 1.200453525995092E+01
	Z =-1.592451238694909E-01
	VX=-2.407903101224412E-03
	VY= 2.946972796014599E-03
	VZ= 4.194955948634716E-05
	'''
	
	# C/2020 F3 (Neowise)
	# 2020-Jul-28 00:00:00.0000
	# Coordinate Origin [change] : 	Sun (body center) [500@10]
	X =-4.313004534071243E-03
	Y =-6.365798630096369E-01
	Z = 3.771839684898292E-01
	VX=-1.320373168048227E-02
	VY=-2.498337721153771E-02
	VZ= 6.922421576828086E-04
	
	
	r=np.array([X,Y,Z])
	v=np.array([VX,VY,VZ])
	
	orbit_elem=orbital_elements(r,v)
	print(orbit_elem)



if __name__ == '__main__':
	main()

