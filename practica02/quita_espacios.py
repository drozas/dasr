#!/usr/bin/python -tt
# -*- coding: utf-8 -*-

#DASR - Práctica 2.4
#Autor: David Rozas (drozas)

""" Script que recibe como argumento uno o más directorios y 
reemplaza los espacios por barras bajas en todos los ficheros y 
subdirectorios de los directorios indicados"""

import os.path
import sys
import fileinput
import shutil

def check_params():
	""" Comprueba que hay al menos un argumento, y que todos ellos con directorios.
	Devuelve 0 en ese caso, -1 en cualquier otro."""
	if (len(sys.argv)>1):
		#Comprobar que todos los argumentos son directorios
		i = 1
		while (i<len(sys.argv)):
			if (not(os.path.isdir(sys.argv[i]))):
				sys.stderr.write("El argumento " + sys.argv[i] + " no es un directorio válido\n")
				return -1
			i = i + 1

		return 0
	else:
		sys.stderr.write("Uso: ./quita_espacios.py <directorio>+\n")
		return -1

def remove_spaces(dir):
	""" Sustituye los espacios por cadenas bajas en los nombres de todos los ficheros 
	del directorio dado"""
	print "Analizando directorio " + dir 
	try:
		for x in os.listdir(dir):
			#Renombrar si es un fichero o directorio con espacios
			if (os.path.isfile(x)):
				if (x.find(" ")!=-1):
					src = os.path.join(dir, x)
					dst = os.path.join(dir, x.replace(" ", "_"))
					os.rename(src, dst)
					print src + " renombrado a " + dst + " (fichero)"
			else:
				if (x.find(" ")!=-1):
					src = os.path.join(dir, x)
					dst = os.path.join(dir, x.replace(" ", "_"))
					shutil.move(src, dst)
					print src + " renombrado a " + dst + " (directorio)"

	except OSError:
		print "No tienes permisos suficientes en " + dir


if __name__ == '__main__':
	state = check_params()
	if (state == 0):
		#Para cada directorio, cambiar todos los espacios por barras bajas en todos los
		#nombres de sus ficheros
		i = 1
		while (i<len(sys.argv)):
			remove_spaces(sys.argv[i])
			i = i + 1
	sys.exit(state)
