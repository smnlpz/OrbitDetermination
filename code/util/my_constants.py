#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 21 11:20:14 2020

@author: simon
"""

import numpy as np
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

# Oblicuidad media, para el paso de ICRF a la eclíptica
mean_obliquity=2.343776036355538E+01*np.pi/180


# Todos los valores de las coordenadas astronómicas están
# tomadas a día 2020-Jul-28 20:00:00.0000 en la web de JPL.
# (2459059.333333333)

Mercury = OrbitalObject(name='Mercury',
					    a=3.870983668423151E-01,
					    e=2.056324574435540E-01,
					    i=7.003700031428785E+00,
					    Omega=4.830522172401749E+01,
					    omega=2.918622484111233E+01,
					    p=8.796915076159155E+01, degree=True)

Venus = OrbitalObject(name='Venus',
					  a=7.233285085724335E-01,
					  e=6.780656400927397E-03 ,
					  i=3.394552870751427E+00,
					  Omega=7.662327384352011E+01,
					  omega=5.514122646705786E+01,
					  p=2.246990668138898E+02, degree=True)


Earth = OrbitalObject(name='Earth',
					  a=9.997843564797363E-01,
					  e=1.707168344231522E-02,
					  i=1.982259124359018E-03,
					  Omega=2.194445465875467E+02,
					  omega=2.426369002793497E+02,
					  p=365.256363, degree=True)

Mars = OrbitalObject(name='Mars',
					 a=1.523729095669281E+00,
					 e=9.342196628978804E-02,
					 i=1.847891976835405E+00,
					 Omega=4.949621500821488E+01,
					 omega=2.866044343175786E+02,
					 p=686.971, degree=True)

Ceres = OrbitalObject(name='Ceres',
					  a=2.767120471001614E+00,
					  e=7.776375075625865E-02,
					  i=1.058814721891299E+01,
					  Omega=8.028170111757919E+01,
					  omega=7.371338812354641E+01,
					  p=1.681281862025212E+03, degree=True)

Jupiter = OrbitalObject(name='Jupiter',
						a=5.203735240082719E+00,
						e=4.873741903295260E-02,
						i=1.303536884947396E+00,
					    Omega=1.005162233205719E+02,
					    omega=2.734496717295364E+02,
						p=4332.59, degree=True)

Saturn = OrbitalObject(name='Saturn',
					   a=9.580378603925364E+00,
					   e=4.573830934737452E-02,
					   i=7.679928274896487E-01,
					   Omega=7.422636249705366E+01,
					   omega=9.800287460118255E+01,
					   p=3.071331260399070E+04, degree=True)

Uranus = OrbitalObject(name='Uranus',
					   a=1.919368996885909E+01,
					   e=5.144638213206364E-02,
					   i=2.488361866097358E+00,
					   Omega=1.135993676796563E+02,
					   omega=3.370164030770658E+02,
					   p=10759.22, degree=True)

Neptune = OrbitalObject(name='Neptune',
						a=3.023754274903354E+01,
						e=1.135551700010499E-02,
						i=1.773029846579799E+00,
						Omega=1.318449993586480E+02,
						omega=2.436715746298982E+02,
						p=6.073051814008412E+04, degree=True)

Pluto = OrbitalObject(name='Pluto',
					  a=3.943085597722086E+01,
					  e=2.486586629355636E-01,
					  i=1.701691381428098E+01,
					  Omega=1.102804444543798E+02,
					  omega=1.134201399602920E+02,
					  p=9.043837137342972E+04, degree=True)

SolarSystem = list([Mercury,Venus,Earth,Mars,Jupiter,Saturn,Uranus,Neptune,Pluto])


