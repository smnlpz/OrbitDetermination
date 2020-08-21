#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 10 18:41:32 2020

@author: simon
"""

import requests
import csv
import numpy as np

t_1=2459058.5 # 28 de julio 00:00
t_2=2459059.5 # 29 de julio 00:00
t_3=2459060.5 # 30 de julio 00:00
times=list([t_1,t_2,t_3])

#URL="https://ssd.jpl.nasa.gov/horizons_batch.cgi?batch=1&COMMAND='399'&CENTER='500@10'&MAKE_EPHEM='YES'&TABLE_TYPE='VECTORS'&TLIST='"+str(times[0])+"''"+str(times[1])+"''"+str(times[2])+"'&OUT_UNITS='AU-D'&REF_PLANE='ECLIPTIC'&REF_SYSTEM='J2000'&VECT_CORR='NONE'&VEC_LABELS='YES'&VEC_DELTA_T='NO'&CSV_FORMAT='YES'&OBJ_DATA='NO'&VEC_TABLE='2'"

#page = requests.get(URL)

#print(page.content)

#data = page.text[page.text.find('$$SOE')+len('$$SOE'):page.text.find('$$EOE')]
data = '2459060.500000000, A.D. 2020-Jul-30 00:00:00.0000,  6.112946346574949E-01, -8.105349306345847E-01,  3.514551484244886E-05,  1.344930366791684E-02,  1.029741112207862E-02,  1.047363067791113E-07,\n'

lines = data.splitlines()
print(lines)
reader = csv.reader(lines)
parsed_csv = list(reader)


for row in parsed_csv:
	position=np.array([float(row[2]),float(row[3]),float(row[4])])
	velocity=np.array([float(row[5]),float(row[6]),float(row[7])])

print(position)
