#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 21 11:42:17 2020

@author: simon
"""

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

