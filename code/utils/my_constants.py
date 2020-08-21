#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 21 11:20:14 2020

@author: simon
"""

import sys
sys.path.insert(1, '../scripts')

from orbital_object import OrbitalObject

# Cte gravitación universal
G=6.67384*10**(-11)
# Masa solar
M=1.98847*10**(30)

# El valor de mu está en m^3*s^-2, mientras que x y vx están en
# au y au/day respectivamente. Hacemos la conversión:
mu_unchanged=G*M
mu=86400.0**2*mu_unchanged/149597870700.0**3

Earth = OrbitalObject(name='Earth',
					  a=1.00000261,
					  e=0.01671123,
					  i=0,
					  Omega=0,
					  omega=101.22,
					  p=365.256363, degree=True)
	
Saturn = OrbitalObject(name='Saturn',
					   a=9.5820172,
					   e=0.05648,
					   i=2.48446,
					   Omega=113.642811,
					   omega=336.013862,
					   p=10759.22, degree=True)

Jupiter = OrbitalObject(name='Jupiter',
						a=5.2044,
						e=0.0489,
						i=1.303,
						Omega=100.464,
						omega=273.867,
						p=4332.59, degree=True)
