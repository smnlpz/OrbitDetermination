import tkinter as tk
import tkinter.ttk as ttk

import numpy as np

from astropy.coordinates import Angle
from astropy.time import Time

# Para modificar en ejecución el directorio desde el que importar
import sys
sys.path.insert(1, './scripts')

from laplace_method import Laplace
from orbital_elements import getOrbitalElements
from orbital_plot import plotOrbit
from error_rate import getApproximationError
from orbital_object import OrbitalObject

sys.path.insert(1, './util')

import my_constants as const
from utilities import ICRS_to_ecliptic, getVectorsFromEphemeris

class OrbitTroya:
	
	coordinates=list()
	times=np.zeros(3)
	
	r=np.zeros(3)
	v=np.zeros(3)
	Object = OrbitalObject('',0,0,0,0,0,0)
	
	real_r=np.zeros(3)
	real_v=np.zeros(3)
	real_Object = OrbitalObject('',0,0,0,0,0,0)
	
	def __init__(self, master=None):
		# build ui
		mainwindow = ttk.Frame(master)
		
		name_label = ttk.Label(mainwindow, text='Nombre del Cuerpo: ')
		name_label.grid(column='0', padx='5', pady='15', row='0', columnspan='2')
		self.object_name = ttk.Entry(mainwindow,width='43')
		self.object_name.insert('end', 'Ceres')
		self.object_name.grid(column='2', columnspan='3', row='0', rowspan='1')
		
		asc_label = ttk.Label(mainwindow)
		asc_label.config(text='Ascensión recta (horas)')
		asc_label.grid(column='0', padx='5', pady='5', row='1',columnspan='2')
		self.asc1 = ttk.Entry(mainwindow)
		self.asc1.insert('end', '23 13 15.59')
		self.asc1.grid(column='0', pady='5', row='2',columnspan='2')
		self.asc2 = ttk.Entry(mainwindow)
		self.asc2.insert('end', '23 13 01.31')
		self.asc2.grid(column='0', pady='5', row='3',columnspan='2')
		self.asc3 = ttk.Entry(mainwindow)
		self.asc3.insert('end', '23 12 34.89')
		self.asc3.grid(column='0', pady='5', row='4',columnspan='2')
		
		dec_label = ttk.Label(mainwindow,text='Declinación (grados)')
		dec_label.grid(column='2', padx='5', pady='5', row='1',columnspan='2')
		self.dec1 = ttk.Entry(mainwindow)
		self.dec1.insert('end', '-20 17 00.5')
		self.dec1.grid(column='2', pady='5', row='2',columnspan='2')
		self.dec2 = ttk.Entry(mainwindow)
		self.dec2.insert('end','-20 21 27.5')
		self.dec2.grid(column='2', pady='5', row='3',columnspan='2')
		self.dec3 = ttk.Entry(mainwindow)
		self.dec3.insert('end', '-20 29 18.9')
		self.dec3.grid(column='2', pady='5', row='4',columnspan='2')
		
		t_label = ttk.Label(mainwindow)
		t_label.config(text='Fecha observación')
		t_label.grid(column='4', padx='5', pady='5', row='1')
		self.t1 = ttk.Entry(mainwindow)
		self.t1.insert('end', '2459058.666666667')
		self.t1.grid(column='4', pady='5', row='2')
		self.t2 = ttk.Entry(mainwindow)
		self.t2.insert('end', '2459059.333333333')
		self.t2.grid(column='4', pady='5', row='3')
		self.t3 = ttk.Entry(mainwindow)
		self.t3.insert('end', '2459060.500000000')
		self.t3.grid(column='4', pady='5', row='4')
		
		output_label = ttk.Label(mainwindow)
		output_label.config(font='{FreeMono} 12 {bold underline}', text='Salida:')
		output_label.grid(column='0', padx='5', pady=(20, 5), row='5', sticky='w',columnspan='2')
		self.textWindow = tk.Text(mainwindow)
		self.textWindow.config(font='{FreeMono} 11 {italic}', height='14', padx='5', pady='5')
		self.textWindow.config(width='64')
		self.textWindow.grid(columnspan='5', padx='5', pady='5', row='6', rowspan='10', sticky='w')
		
		check_0=tk.IntVar()
		check_1=tk.IntVar()
		check_2=tk.IntVar()
		check_3=tk.IntVar()
		check_4=tk.IntVar()
		check_5=tk.IntVar()
		check_6=tk.IntVar()
		check_7=tk.IntVar()
		check_8=tk.IntVar()
		check_9=tk.IntVar()
		check_10=tk.IntVar()
		
		plot_label = ttk.Label(mainwindow)
		plot_label.config(font='{FreeMono} 12 {bold underline}', text='Planetas a dibujar:')
		plot_label.grid(padx='5', pady=(20, 5),column='0', row='17', columnspan='2')
		checkbutton_0 = ttk.Checkbutton(mainwindow,variable=check_0,onvalue=1,offvalue=0)
		checkbutton_0.config(state='disabled', text='Órbita Aproximada')
		checkbutton_0.grid(padx='5', pady=(20, 5),column='2', row='17',sticky='w')
		checkbutton_1 = ttk.Checkbutton(mainwindow,variable=check_1,onvalue=1,offvalue=0)
		checkbutton_1.config(state='disabled', text='Vacío')
		checkbutton_1.grid(column='0', padx='5', row='18',sticky='w')
		checkbutton_2 = ttk.Checkbutton(mainwindow,variable=check_2,onvalue=1,offvalue=0)
		checkbutton_2.config(text='Mercurio')
		checkbutton_2.grid(column='1', padx='5', row='18',sticky='w')
		checkbutton_3 = ttk.Checkbutton(mainwindow,variable=check_3,onvalue=1,offvalue=0)
		checkbutton_3.config(text='Venus')
		checkbutton_3.grid(column='2', padx='5', row='18',sticky='w')
		checkbutton_4 = ttk.Checkbutton(mainwindow,variable=check_4,onvalue=1,offvalue=0)
		checkbutton_4.config(text='Tierra')
		checkbutton_4.grid(column='3', padx='5', row='18',sticky='w')
		checkbutton_5 = ttk.Checkbutton(mainwindow,variable=check_5,onvalue=1,offvalue=0)
		checkbutton_5.config(text='Marte')
		checkbutton_5.grid(column='4', padx='5', row='18',sticky='w')
		checkbutton_6 = ttk.Checkbutton(mainwindow,variable=check_6,onvalue=1,offvalue=0)
		checkbutton_6.config(text='Júpiter')
		checkbutton_6.grid(column='0', padx='5', row='19',sticky='w')
		checkbutton_7 = ttk.Checkbutton(mainwindow,variable=check_7,onvalue=1,offvalue=0)
		checkbutton_7.config(text='Saturno')
		checkbutton_7.grid(column='1', padx='5', row='19',sticky='w')
		checkbutton_8 = ttk.Checkbutton(mainwindow,variable=check_8,onvalue=1,offvalue=0)
		checkbutton_8.config(text='Urano')
		checkbutton_8.grid(column='2', padx='5', row='19',sticky='w')
		checkbutton_9 = ttk.Checkbutton(mainwindow,variable=check_9,onvalue=1,offvalue=0)
		checkbutton_9.config(text='Neptuno')
		checkbutton_9.grid(column='3', padx='5', row='19',sticky='w')
		checkbutton_10 = ttk.Checkbutton(mainwindow,variable=check_10,onvalue=1,offvalue=0)
		checkbutton_10.config(text='Plutón')
		checkbutton_10.grid(column='4', padx='5', row='19',sticky='w')
		
		checkbuttons=list([check_2,check_3,check_4,check_5,check_6,check_7,check_8,check_9,check_10])
		
		space_label = ttk.Label(mainwindow)
		space_label.grid(row='20',pady='5')
		
		
		button_search = ttk.Button(mainwindow,text='Buscar',command=lambda: self.searchObject(checkbutton_1,check_1))
		button_search.grid(column='5', padx=5, row='0')
		button_error = ttk.Button(mainwindow,text='Error',command=self.computeError,state='disable')
		button_error.grid(column='5', padx=5, row='7')
		button_laplace = ttk.Button(mainwindow,text='Laplace',command=lambda: self.computeLaplace(button_error,checkbutton_0,check_0))
		button_laplace.grid(column='5', padx=5, row='6')
		button_plot = ttk.Button(mainwindow,text='Dibujar',command=lambda: self.plot(check_0,check_1,checkbuttons))
		button_plot.grid(column='5', padx='5', row='18', rowspan='2')
		
		
		mainwindow.config(height='200', width='200')
		mainwindow.pack(side='top',padx=10,pady=10)

		# Main widget
		self.mainwindow = mainwindow
		
	def searchObject(self,check,check_value):
		self.real_r,self.real_v=getVectorsFromEphemeris(name=self.object_name.get(),epoch=float(self.t2.get()))
		self.real_Object=getOrbitalElements(self.real_r,self.real_v,name=self.object_name.get())
		
		check.config(text=self.object_name.get(),state='enable')
		
	def computeLaplace(self,b_error,check,check_value):
		coordinates=list([(Angle(self.asc1.get()+' hours'),Angle(self.dec1.get()+' degrees')),
						  (Angle(self.asc2.get()+' hours'),Angle(self.dec2.get()+' degrees')),
						  (Angle(self.asc3.get()+' hours'),Angle(self.dec3.get()+' degrees'))])
		
		t=[float(self.t1.get()),float(self.t2.get()),float(self.t3.get())]
		
		times = Time(t, format='jd')
		
		# Obtenemos la posición y velocidad del objeto
		self.r,self.v=Laplace(coordinates,times)
		
		# Pasamos las coordenadas de ICRS a eclíptica
		self.r=ICRS_to_ecliptic(self.r)
		self.v=ICRS_to_ecliptic(self.v)
		
		# Obtenemos los elementos orbitales
		self.Object=getOrbitalElements(self.r,self.v,name='Approximate ' + self.object_name.get())
		
		self.textWindow.delete('1.0','end')
		self.textWindow.insert('end','Posición calculada: '+str(self.r))
		self.textWindow.insert('end','\nVelocidad calculada: '+str(self.v))
		
		self.textWindow.insert('end','\n\nElementos orbitales obtenidos:\n')
		self.textWindow.insert('end',str(self.Object))
		
		b_error.config(state='enable')
		
		if self.Object.a<=0:
			self.textWindow.insert('end','\n\nSemieje mayor negativo, no se puede dibujar la órbita.')
			check_value.set(0)
			check.config(state='disabled')
		else:
			check.config(state='enable')
	
	
	def computeError(self):
		# Comprobamos el error
		self.textWindow.delete('1.0','end')
		self.textWindow.insert('end',getApproximationError(self.r,self.v,self.times[1],self.object_name.get()))

		
	def plot(self,check_0,check_1,checkbuttons):
		toPlot=list()
		if check_0.get():
			toPlot.append(self.Object)
		if check_1.get():
			toPlot.append(self.real_Object)
		
		for i in range(len(checkbuttons)):
			if checkbuttons[i].get():
				toPlot.append(const.SolarSystem[i])
		
		plotOrbit(toPlot)
	
			
		
	def run(self):
		self.mainwindow.mainloop()


