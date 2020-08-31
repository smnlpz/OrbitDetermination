#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug 30 12:12:27 2020

@author: simon
"""

import numpy as np
from scipy.interpolate import lagrange

valor_real=np.array([2.877536329527219E+01, -4.896255154715386E+00, -5.593217457054652E-01])
valor_real/=2.919430917371045E+01

rho=2.919430917371045E+01
rho_prima=-1.167800417699119E-02

derivada=np.array([-1.303447187892505E-02,-6.963877053288004E-03,-7.773751777526004E-05])

valor_real_prima=(derivada-rho_prima*valor_real)/rho


#position=np.array([[ 0.98569822 ,-0.14599621, -0.08416723],[ 0.98564669 ,-0.14626914, -0.0842967 ],[ 0.98559377, -0.14654918, -0.08442906]])
position=np.array([[ -0.52821828, -0.78154679, -0.33191876],[ 0.98564669 ,-0.14626914, -0.0842967 ],[ 0.98559377, -0.14654918, -0.08442906]])
#times=np.array([2459058.5,2459059.5,2459060.5])
times=np.array([2458849.500000000,2459059.5,2459060.5])

velocity=np.zeros(3)
second_deriv=np.zeros(3)

for i in range(3):
	# Dado que no sabemos si los intervalos son
	# equiespaciados, utilizamos la derivada del
	# polinomio de Lagrange
	
	#velocity[i]=(2*times[1]-(times[1]+times[2]))/((times[0]-times[1])*(times[0]-times[2]))*position[0][i]+(2*times[1]-(times[2]+times[0]))/((times[1]-times[2])*(times[1]-times[0]))*position[1][i]+(2*times[1]-(times[0]+times[1]))/((times[2]-times[0])*(times[2]-times[1]))*position[2][i]
	#second_deriv[i]=2/((times[0]-times[1])*(times[0]-times[2]))*position[0][i]+2/((times[1]-times[2])*(times[1]-times[0]))*position[1][i]+2/((times[2]-times[0])*(times[2]-times[1]))*position[2][i]
	
	poly=lagrange(times, position[:,i])
	velocity[i]=poly.deriv(m=1)(times[1])
	second_deriv[i]=poly.deriv(m=2)(times[1])

print('Posición real:')
print(valor_real)

print('Posición pasada de asc. recta dec. a XYZ:')
print(position[1])


print('\nValor real:')
print(valor_real_prima)
print('Norma = ' + str(np.linalg.norm(valor_real_prima)))

print('Valor aproximado:')
print(velocity)
print('Norma = ' + str(np.linalg.norm(velocity)))

print('\nError:')
print(valor_real_prima-velocity)
print('Norma = ' + str(np.linalg.norm(valor_real_prima-velocity)))

'''
# Cte gravitación universal
G=6.67384*10**(-11)
# Masa solar
M=1.98847*10**(30)

# El valor de mu está en m^3*s^-2, mientras que x y vx están en
# au y au/day respectivamente. Hacemos la conversión:
mu_unchanged=G*M
mu=86400.0**2*mu_unchanged/149597870700.0**3

print(-mu*position[1]/np.linalg.norm(position[1]))
'''