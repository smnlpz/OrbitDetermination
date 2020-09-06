#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep  1 17:05:45 2020

@author: simon
"""

import numpy as np

# Para modificar en ejecución el directorio desde el que importar
import sys
sys.path.insert(1, '../util')

from utilities import getVectorsFromEphemeris

def getApproximationError(pos,vel,epoch,object_name):
	# Buscamos el cuerpo en la efemérides
	real_pos,real_vel,result=getVectorsFromEphemeris(name=object_name,epoch=epoch)
	
	real_dist=np.linalg.norm(real_pos)
	dist=np.linalg.norm(pos)
	
	# Comparamos y guardamos resultados
	output=''
	output+='Posición real: ' +str(real_pos)
	output+='\nPosición calculada: ' +str(pos)
	output+='\nError = '+str(real_pos-pos)+'\n|Error| = '+str(np.linalg.norm(real_pos-pos))
	output+='\n\nVelocidad real: ' +str(real_vel)
	output+='\nVelocidad calculada: ' +str(vel)
	output+='\nError = '+str(real_vel-vel)+'\n|Error| = '+str(np.linalg.norm(real_vel-vel))
	output+='\n\nDistancia real: ' +str(real_dist)
	output+='\nDistancia aproximada: ' +str(dist)

	return output


	