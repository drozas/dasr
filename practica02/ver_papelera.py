#!/usr/bin/python -tt
# -*- coding: utf-8 -*-

#DASR - Práctica 2.6
#Autor: David Rozas (drozas)

""" Script que muestra un listado de los ficheros que hay en la papelera"""

import borra
import os
import os.path
import pickle

path = os.path.join(borra.get_papelera_path(), ".persistencia")
if os.path.exists(path):
	fich = open(path,"r")
	try:
		print "Número\t", "Nombre original\t", "Papelera-ID\t", "Path original\t", "Fecha modificación\t", "Fecha borrado"
		i = 0
		while True:
			fichero = pickle.load(fich)
			i  = i + 1
			print i,
			for data in fichero:
				print data,
			print "\n"
	
	except EOFError:
		fich.close()
else:
	print "Vacío"

