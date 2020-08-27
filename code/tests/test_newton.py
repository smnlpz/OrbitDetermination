#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 21 11:39:07 2020

@author: simon
"""

from sympy import *
x = Symbol('x')

# Para modificar en ejecución el directorio desde el que importar
import sys
sys.path.insert(1, '../scripts')

import newton


def main():
	# Cálculo de sqrt(3) mediante el método de Newton
	f=x**2-3
	raiz_3,n_iters=newton.newton_method(f=f,x_0=2,max_iters=1000,tol=0.000001)
	print('sqrt(3) = '+ str(raiz_3) +';\t n_iters = ' + str(n_iters))
	
	
	# El método de Newton no converge con
	# m=3.600653945648716 y x_0=1.5707963267948966
	M=0.6
	m=6
	
	lista=newton.approximate_phi(M,m,plot=True)
	
	print(lista)
	

if __name__ == '__main__':
	main()