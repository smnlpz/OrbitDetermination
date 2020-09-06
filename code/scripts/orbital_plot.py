#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 21 11:01:34 2020

@author: simon
"""

import numpy as np
#from mpl_toolkits import mplot3d
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import seaborn as sns


def rotation_matrix(axis,ang):
	if axis=='x':
		return np.matrix([[1, 0,           0          ],
					      [0, np.cos(ang),-np.sin(ang)],
						  [0, np.sin(ang), np.cos(ang)]])
	if axis=='y':
		return np.matrix([[np.cos(ang), 0,-np.sin(ang)],
					      [0,           1, 0          ],
						  [np.sin(ang), 0, np.cos(ang)]])
	if axis=='z':
		return np.matrix([[np.cos(ang),np.sin(ang), 0],
					      [-np.sin(ang), np.cos(ang), 0],
						  [0,           0,           1]])
	return float('NaN')
		


def rotate(obj, omega, i, Omega):
	obj=np.transpose(obj)
	
	rot_matrix=np.dot(np.dot(rotation_matrix('z',omega),rotation_matrix('x',i)),rotation_matrix('z',Omega))
	
	for ind in range(len(obj)):
		obj[ind]=np.dot(rot_matrix,obj[ind])
	
	return np.transpose(obj)
	


def plotOrbit(orbitas,sun_center=True):
	# Creamos la figura
	fig = plt.figure(figsize=(8,5))
	ax = fig.add_subplot(111, projection='3d')
	
	# Dibujamos el Sol
	ax.scatter(0,0,0,color='yellow')
	
	if type(orbitas)!=list:
		orbitas=list([orbitas])
	
	# Inicializamos los colores a utilizar
	colors=sns.color_palette("bright", len(orbitas))
	color_i=0
	
	for orb in orbitas:
		# Semieje menor y distancia de los focos al centro de la elipse
		b=orb.a*np.sqrt((1-orb.e**2))
		center=orb.a*orb.e
		
		# Dibujamos la elipse
		u = np.linspace(0, 2*np.pi, 1000)
		ellipse=np.array([orb.a*np.cos(u)+center, b*np.sin(u), np.zeros(len(u))])
		
		# Dibujamos la línea de nodos de cada elipse
		line_of_nodes=np.array([np.zeros(2),
							    np.linspace(min(ellipse[1]),max(ellipse[1]),2),
								np.zeros(2)])
		
		# Rotaciones en el espacio
		ellipse=rotate(ellipse,orb.omega,orb.i,orb.Omega)
		line_of_nodes=rotate(line_of_nodes,orb.omega,orb.i,orb.Omega)
		
		# Añadimos las elipses junto al resto
		ax.plot3D(ellipse[0],ellipse[1],ellipse[2], color=colors[color_i],label=orb.name)
		color_i+=1
		ax.plot3D(line_of_nodes[0],line_of_nodes[1],line_of_nodes[2],linestyle=(0, (1,2)))
		
	
	# Establecemos los límites para los ejes
	Xlim=np.asarray(ax.get_xlim3d())
	Xlim_mid=np.asarray([-(Xlim[1]-Xlim[0])/2,(Xlim[1]-Xlim[0])/2])	
	if sun_center:
		ax.set_xlim3d(Xlim_mid)
	else:
		ax.set_xlim3d(Xlim)
	ax.set_ylim3d(Xlim_mid)
	ax.set_zlim3d(Xlim_mid * 3/4)
	try:
		ax.set_aspect('equal')
	except NotImplementedError:
		pass
	
	# Finalmente, añadimos la leyenda a la gráfica
	ax.legend(loc='upper right', frameon=False)
	
	plt.show()