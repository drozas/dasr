#!/usr/bin/python -tt
# -*- coding: utf-8 -*-

#DASR - Práctica 3.4
#Autor: David Rozas (drozas)

""" Recibe uno o más nombres de ficheros tgz y crea en el directorio actual un fichero con los 
mismos datos pero en formato .tar.bz2 (incluye empaquetado por si el fichero .tgz estaba 
compuesto de varios ficheros)"""

import os.path
import sys
import commands
import os

def check_params():
	if (len(sys.argv)>1):
		#Comprobar que todos los argumentos existen y son ficheros tgz
		i = 1
		while (i<len(sys.argv)):
			if (not(os.path.isfile(sys.argv[i])) or not(is_tgz(sys.argv[i]))):
				sys.stderr.write("Uso: Todos los argumentos deben ser ficheros tgz\n")
				return -1
			i = i + 1

		return 0
	else:
		sys.stderr.write("Uso: ./tgz-bz2.py [<fichero.tgz>]+\n")
		return -1

def is_tgz(file):
	""" 
	Devuelve true si el fichero es un fichero comprimido gzip, 
	false en caso contrario.
	"""
	
	command = "file " + file
	r = commands.getstatusoutput(command)
	if (r[0]==0):
		trozos = r[1].split(" ")
		return trozos[1]=="gzip"
	else:
		print "Error al ejecutar: " + command
		return False

def tgz2bz(file):
	"""Convierte el fichero tgz en un tar.bz2 con el mismo nombre"""
	
	#El nuevo nombre del fichero lo formaremos: separando nombre de fichero y path y quitando su extensión
	new_name = os.path.split(file)
	new_name = (new_name[1].split(".")[0])+".tar.bz2"
	
	command = "gunzip -c " + file + " | bzip2 > ./" + new_name
	print "Ejecutando " + command
	return commands.getstatusoutput(command)[0]



if __name__ == '__main__':
	state = check_params()
	if (state == 0):
		#Para cada uno de los argumentos, intentar hacer la conversión (seguir con el resto si alguno falla)
		i = 1
		while (i<len(sys.argv)):
			result = tgz2bz(sys.argv[i])
			if (result == 0):
				print(sys.argv[i] + " fue convertido correctamente.")
			else:
				print(sys.argv[i] + " hubo un error al intentar realizar la conversión.")

			i = i + 1
	sys.exit(state)
