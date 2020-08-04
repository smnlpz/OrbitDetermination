#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug  3 18:10:42 2020

@author: simon
"""

from sympy import *
import numpy as np

x = Symbol('x')


def newton_method(f,x_0,max_iters,tol):
	f_prime=f.diff(x)
	
	iters=0
	for iters in range(max_iters):
		x_1=x_0-f.subs(x,x_0)/f_prime.subs(x,x_0)
		if(np.abs(x_1-x_0)<tol):
			return float(x_1),iters+1	
		x_0=float(x_1)
		
	return x_0,iters+1



def approximate_phi(M,m,x_0):
	max_iters=10000
	f = sin(x)**4-M*sin(x+m)
	phi,n_iters=newton_method(f=f,x_0=x_0,max_iters=max_iters,tol=0.000000001)
	
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
	
	return phi,n_iters

	
def main():
	# Cálculo de sqrt(3) mediante el método de Newton
	f=x**2-3
	raiz_3,n_iters=newton_method(f=f,x_0=2,max_iters=1000,tol=0.000001)
	print('sqrt(3) = '+ str(raiz_3) +';\t n_iters = ' + str(n_iters))
	
	
	M=0.6
	m=6.09
	phi_values=list()
	
	
	for i in range(8):
		x_0=i*2*np.pi/8
		phi,n_iters=approximate_phi(M,m,x_0)
		print('\nx_0 = '+ str(x_0))
		print('phi = '+ str(phi) +';\t n_iters = ' + str(n_iters))
		
		if not phi in phi_values:
			phi_values.append(phi)
			
	phi_values = [s for s in phi_values if s<np.pi]
	
	

if __name__ == '__main__':
	main()


