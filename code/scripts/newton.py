#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug  3 18:10:42 2020

@author: simon
"""

from sympy import *
import numpy as np
import matplotlib.pyplot as plt

x = Symbol('x')


def newton_method(f,x_0,max_iters,tol):
	f_prime=f.diff(x)
	
	iters=0
	#print(x_0)
	for iters in range(max_iters):
		x_1=x_0-f.subs(x,x_0)/f_prime.subs(x,x_0)
		#print(str(float(x_1)) + ' \t ' + str(x_1-x_0))
		if(np.abs(x_1-x_0)<tol):
			return float(x_1),iters+1
		x_0=float(x_1)
		
	return x_0,iters+1



def approximate_phi(M,m,tol=0.000000001,max_tries=64,plot=False):
	max_iters=10000
	
	f = sin(x)**4-M*sin(x+m)
	phi_values=list()
	
	for i in range(max_tries):
		alpha_i=i*np.pi/max_tries
		alpha_i_plus_1=(i+1)*np.pi/max_tries
		#print(str(f.subs(x,alpha_i)) + ' ' + str(f.subs(x,alpha_i_plus_1)))
		
		if np.sign(f.subs(x,alpha_i))!=np.sign(f.subs(x,alpha_i_plus_1)):
			x_0=(alpha_i+alpha_i_plus_1)/2
			#print('\nx_0 = ' +str(x_0))
			phi,n_iters=newton_method(f=f,x_0=x_0,max_iters=max_iters,tol=tol)
		
			# Si llegamos al número máximo de iteraciones probablemente el
			# valor aproximado no sea correcto, por lo que devolvemos NaN
			# (es poco probable que pase, ya que hemos elegido un valor
			# inicial cercano a la solución)
			if n_iters==max_iters:
				phi=float('nan')
		
			phi_values.append(phi)
		
	
	if plot:
		t=np.arange(0.,np.pi,np.pi/64)
		plt.clf()
		plt.plot(t,np.sin(t)**4, color='blue')
		plt.plot(t,M*np.sin(t+m),color='green')
		plt.plot(phi_values,np.sin(phi_values)**4,'ro')
	
	return phi_values
