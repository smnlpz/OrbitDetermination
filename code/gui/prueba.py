#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep  1 18:00:31 2020

@author: simon
"""


import tkinter as tk
from tkinter.font import Font

# Para modificar en ejecución el directorio desde el que importar
import sys
sys.path.insert(1, '../scripts')

from orbital_plot import plotOrbit

sys.path.insert(1, '../util')

import my_constants as const


root=tk.Tk()
root.title('ORBITAL TROYA')

def onClick(i):
	print('Hola caracola ' +i)
	
def popup():
	tk.messagebox.showinfo('Hey','Wassup!')
	
def otra_ventana(phi_1,phi_2):
	phi = -1
	top = tk.Toplevel()
	top.title('Ángulo')
	top.geometry('200x200')
	radio1 = tk.Radiobutton(top, text=phi_1, variable=phi, value=0).pack()
	radio2 = tk.Radiobutton(top, text=phi_2, variable=phi, value=1).pack()
	button1 = tk.Button(top, text='pintar', command=lambda:plotOrbit(const.Ceres)).pack()
	button2 = tk.Button(top, text='Cerrar', command=top.destroy).pack()
	

# Creamos los elementos que se mostrarán
label1 = tk.Label(root, text='ORBITAL TROYA')
label2 = tk.Label(root, text='Probando tkinter')
label3 = tk.Label(root, text='Wey k pasa')
text1 = tk.Entry(root)
myButton = tk.Button(root, text='Orbita', command=lambda: onClick(text1.get()))
button1 =tk.Button(root, text='popup', command=lambda: otra_ventana('10','20'), pady=10)
exit_button = tk.Button(root, text='Salir', command=root.quit)

myFont = Font(family="Times New Roman", size=12)
label1.configure(font=myFont)

# Posicionamos los elementos
label1.grid(row=0,column=10,padx=10,pady=10)
label2.grid(row=0,column=0)
label3.grid(row=10,column=3)
myButton.grid(row=5,column=7)
text1.grid(row=0,column=4)
exit_button.grid(row=10,column=10)
button1.grid(row=0,column=5)

root.mainloop()