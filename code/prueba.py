#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 30 12:08:44 2020

@author: simon
"""


import numpy as np
#from mpl_toolkits import mplot3d
import matplotlib.pyplot as plt
#from mpl_toolkits.mplot3d import Axes3D
import seaborn as sns

class OrbitalObject:
	def __init__(self,name,a,e,i,Omega,omega,p):
		self.name=name
		self.a=a
		self.e=e
		self.i=i
		self.Omega=Omega
		self.omega=omega
		self.p=p
		
	def toRad(self):
		conv=(2*np.pi)/360
		self.i*=conv
		self.Omega*=conv
		self.omega+=conv
		
	def toDeg(self):
		conv=360/(2*np.pi)
		self.i*=conv
		self.Omega*=conv
		self.omega*=conv
		
		
	def getName(self):
		return self.name
	
	def __str__(self):
		return '(\''+str(self.name)+'\', '+str(self.a)+', '+str(self.e)+', '+str(self.i)+', '+str(self.Omega)+', '+str(self.omega)+', '+str(self.p)+')'


Earth = OrbitalObject(name='Earth',
					  a=1.00000261,
					  e=0.01671123,
					  i=0,
					  Omega=0,
					  omega=0,
					  p=365.256363)

Saturn = OrbitalObject(name='Saturn',
					   a=9.5820172,
					   e=0.05648,
					   i=2.48446,
					   Omega=113.642811,
					   omega=336.013862,
					   p=10759.22)

Jupiter = OrbitalObject(name='Jupiter',
						a=5.2044,
						e=0.0489,
						i=1.303,
						Omega=100.464,
						omega=273.867,
						p=4332.59)






G=6.67384*10**(-11)
M=1.98847*10**(30)
def orbital_elements(x,vx,name='NotAssigned'):
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
	conv=360/(2*np.pi)
	#conv=1
	
	orbital = OrbitalObject(name=name,a=a,e=e,i=i*conv,Omega=Omega*conv,omega=omega*conv,p=p)
	
	return orbital


def rotate(obj, x_ang, y_ang, z_ang):
	rot_x = np.matrix([[1, 0,             0            ],
				       [0, np.cos(x_ang),-np.sin(x_ang)],
					   [0, np.sin(x_ang), np.cos(x_ang)]])
	
	rot_y = np.matrix([[np.cos(y_ang), 0,-np.sin(y_ang)],
				       [0,             1, 0            ],
					   [np.sin(y_ang), 0, np.cos(y_ang)]])
	
	rot_z = np.matrix([[np.cos(z_ang),-np.sin(z_ang), 0],
					   [np.sin(z_ang), np.cos(z_ang), 0],
					   [0,             0,             1]])
	
	obj=np.transpose(obj)
	
	for i in range(len(obj)):
		obj[i]=np.dot(rot_y,obj[i])
		obj[i]=np.dot(rot_x,obj[i])
		obj[i]=np.dot(rot_z,obj[i])
	
	return np.transpose(obj)
	

def plotOrbit(orbita,earthOrbit=False):
	# Creamos la figura
	fig = plt.figure(figsize=(10, 10))
	ax = fig.add_subplot(111, projection='3d')
	
	# Dibujamos el Sol
	ax.scatter(0,0,0,color='yellow')
	
	if type(orbita)!=list:
		orbita=list([orbita])
	
	colors=sns.color_palette("bright", len(orbita))
	color_i=0
	
	for orb in orbita:
		# Semieje menor y distancia de los focos al centro de la elipse
		b=orb.a*np.sqrt((1-orb.e**2))
		center=orb.a*orb.e
		
		# Pasamos los ángulos (por defecto en grados) a radianes para
		# trabajar con las funciones trigonométricas
		orb.toRad()
		
		# Dibujamos las elipses y las rotamos
		u = np.linspace(0, 2*np.pi, 1000)
		ellipse=np.array([orb.a*np.cos(u)+center, b*np.sin(u), np.zeros(len(u))])
		ellipse=rotate(ellipse,0,orb.i,orb.Omega)
		
		ax.plot3D(ellipse[0],ellipse[1],ellipse[2], color=colors[color_i])
		color_i+=1
		
		#line_of_nodes=np.array([np.zeros(2),
		#					    np.linspace(min(ellipse[1]),max(ellipse[1]),2),
		#						np.zeros(2)])
		#line_of_nodes=rotate(line_of_nodes,0,np.pi/5,Omega)
		#ax.plot3D(line_of_nodes[0],line_of_nodes[1],line_of_nodes[2],linestyle=':')
	
	if earthOrbit:
		b=Earth.a*np.sqrt((1-Earth.e**2))
		center=Earth.a*Earth.e
		ax.plot3D(Earth.a*np.cos(u)+center, b*np.sin(u), 0, 'red')

	# Establecemos los límites para los ejes
	Xlim=np.asarray(ax.get_xlim3d())
	Xlim_mid=np.asarray([-(Xlim[1]-Xlim[0])/2,(Xlim[1]-Xlim[0])/2])	
	ax.set_xlim3d(Xlim)
	ax.set_ylim3d(Xlim_mid)
	ax.set_zlim3d(Xlim_mid * 3/4)
	try:
		ax.set_aspect('equal')
	except NotImplementedError:
		pass
	

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
	'''
	X = 1.359741522403668E+01
	Y =-3.125322406604633E+01
	Z =-5.881149104622369E-01
	VX= 2.950200674787515E-03
	VY= 5.745585982807115E-04
	VZ=-9.180472035906128E-04
	
	
	r=np.array([X,Y,Z])
	v=np.array([VX,VY,VZ])
	
	orb=orbital_elements(r,v)
	
	orbits=list([orb,Saturn,Jupiter])
	
	plotOrbit(orbits,True)
	
if __name__ == '__main__':
	main()

