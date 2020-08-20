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


def isclose(a, b, rel_tol=1e-09, abs_tol=0.0):
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


def newton_method(f,x_0,max_iters,tol):
	f_prime=f.diff(x)
	
	iters=0
	for iters in range(max_iters):
		x_1=x_0-f.subs(x,x_0)/f_prime.subs(x,x_0)
		if(np.abs(x_1-x_0)<tol):
			return float(x_1),iters+1	
		x_0=float(x_1)
		
	return x_0,iters+1



def approximate_phi(M,m,plot=False):
	max_iters=10000
	tol=0.000000001
	max_tries=16
	
	f = sin(x)**4-M*sin(x+m)
	phi_values=list()
	
	for i in range(max_tries):
		x_0=i*2*np.pi/max_tries
		phi,n_iters=newton_method(f=f,x_0=x_0,max_iters=max_iters,tol=tol)
		
		# Si llegamos al número máximo de iteraciones probablemente el valor
		# aproximado no sea correcto, por lo que devolvemos NaN
		if n_iters==max_iters:
			phi=float('nan')
		
		# Por la periodicidad de la función, podemos trasladar a (0,2pi)
		while phi<0 or phi>2*np.pi:
			if phi<0:
				phi+=2*np.pi
			else:
				phi-=2*np.pi
		
		# Comprobamos que el valor calculado no sea similar a otro
		# calculado previamente
		add=True
		for s in phi_values:
			if isclose(phi,s,rel_tol=10000*tol):
				add=False
				break
		
		if add:
			phi_values.append(phi)
		
	phi_values = [s for s in phi_values if s<np.pi]
	phi_values.sort()
	
	if plot:
		t=np.arange(0.,np.pi,np.pi/64)
		plt.clf()
		plt.plot(t,np.sin(t)**4, color='blue')
		plt.plot(t,M*np.sin(t+m),color='green')
		plt.plot(phi_values,np.sin(phi_values)**4,'ro')
	
	return phi_values

	
def main():
	# Cálculo de sqrt(3) mediante el método de Newton
	f=x**2-3
	raiz_3,n_iters=newton_method(f=f,x_0=2,max_iters=1000,tol=0.000001)
	print('sqrt(3) = '+ str(raiz_3) +';\t n_iters = ' + str(n_iters))
	
	
	M=0.3695715755580589
	m=-0.034911329608047485
	
	lista=approximate_phi(M,m,plot=True)
	
	print(lista)
	
	
	

if __name__ == '__main__':
	main()


