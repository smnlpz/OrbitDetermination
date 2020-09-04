#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep  2 18:03:53 2020

@author: simon
"""

import tkinter as tk

# Para modificar en ejecución el directorio desde el que importar
import sys
sys.path.insert(1, './gui')
from orbit_gui import OrbitTroya

def main():
	root = tk.Tk()
	root.title('Orbit Troya')
	troya = OrbitTroya(root)
	troya.run()

if __name__ == '__main__':
	main()
