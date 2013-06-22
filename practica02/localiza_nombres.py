#!/usr/bin/python -tt
# -*- coding: utf-8 -*-

#DASR - Práctica 2.3
#Autor: David Rozas (drozas)

""" Recibe un nombre de fichero y un directorio, y busca todos los 
nombres (enlaces duros) de dicho fichero a partir de ese directorio 
recursivamente """

import os.path
import sys

def check_params():
	if (len(sys.argv)==3):
		#Comprobar que el fichero es un fichero, y que el directorio existe
		if (os.path.isfile(sys.argv[1]) and os.path.isdir(sys.argv[2])):
			return 0
		else:
			sys.stderr.write("Uso: El argumento <fichero> debe existir y ser un fichero, y el argumento <directorio> debe existir y ser un directorio\n")
			return -1
	else:
		sys.stderr.write("Uso: ./localiza_nombres.py <fichero> <directorio_busqueda>\n")
		return -1

def is_same_file (arg, dirname, names):
	"""Chequea para todos los ficheros de ese directorio, si es un nombre de arg, y lo muestra en ese caso """
	for name in names:
		try: 
			if (os.path.samefile(arg, os.path.join(dirname,name))):
				print (os.path.join(dirname,name))
		except OSError:
			None

if __name__ == '__main__':
	state = check_params()
	if (state == 0):
		os.path.walk(sys.argv[2], is_same_file, sys.argv[1])
	sys.exit(state)
