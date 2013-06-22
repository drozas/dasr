#!/usr/bin/python -tt
# -*- coding: utf-8 -*-

#DASR - Práctica 2.6
#Autor: David Rozas (drozas)

""" Script que realiza un borrado con papelera de reciclaje"""

import os.path
import os
import sys
import time
import re
import commands
import shutil
import pickle

global papelera_path

def get_papelera_path():
	"""Toma el valor del path de la papelera, creándolo si no 
	existe"""

	papelera = os.getenv("PAPELERA")
	if papelera == None:
		msg="ERROR: variable de entorno PAPELERA no definida"
		sys.stderr.write(msg + "\n")
		raise SystemExit
	else:
		if not(os.path.isdir(papelera)) or not(os.path.exists(papelera)):
			try:
				os.mkdir(papelera,0700)
				print "Creado directorio para papelera en " + papelera
			except OSError:
				msg="ERROR: No fue posible crear el directorio " + papelera
				sys.stderr.write(msg + "\n")
				raise SystemExit
		return papelera


def check_params():
	""" Comprueba que hay al menos un argumento, y que todos ellos existen
	Devuelve 0 en ese caso, -1 en cualquier otro."""
	if (len(sys.argv)>1):
		#Comprobar que todos los argumentos existen
		i = 1
		while (i<len(sys.argv)):
			if (not(os.path.exists(sys.argv[i]))):
				sys.stderr.write("ERROR: El fichero o directorio " + sys.argv[i] + " no existe\n")
				return -1
			i = i + 1

		return 0
	else:
		sys.stderr.write("Uso: ./borra.py <directorio|fichero>+\n")
		return -1

def store_data(file, new_name):
	"""
	Guarda la meta información de borrado en un fichero.
	Se guardará una lista con id+path_absoluto+fecha_modificacion+fecha_borrado (en formato humano)
	""" 
	pers_file = open(os.path.join(papelera_path, ".persistencia"), "a")
	data = [file, new_name, os.path.abspath(file), time.ctime(os.path.getmtime(file)), time.ctime(time.time())]
	pickle.dump(data, pers_file)
	pers_file.close()

def get_systemfile(file):
	""" Devuelve el sistema de ficheros al que pertenece ese fichero (o directorio) """

	p = commands.getstatusoutput('df ' + file)
	if (p[0]==0):
		#Cortar por retorno de carro para obtener lineas
		lineas = p[1].split('\n')
		#Cortamos la primera linea por espacios, y devolvemos el valor del primer campo
		datos = re.split(" +", lineas[1])
		return datos[0]
	else:
		msg="ERROR: No fue posible averiguar el sistema de ficheros de " + file
		sys.stderr.write(msg + "\n")
		raise SystemExit


def same_systemfile(file):
	""" Comprueba si el fichero está en el mismo sistema de ficheros que la papelera, 
	intentando realizar un enlace duro (que después será borrado) 
	
	Problema: Esto es válido para ficheros, pero no para directorios (que no permiten enlaces duros)
	Solución: Mirarlo a traveś de df"""
	return get_systemfile(papelera_path) == get_systemfile(file)

#	try:
#		os.link(file,os.path.join(papelera_path, "link"))
#		os.remove(os.path.join(papelera_path, "link"))
#		return True
#	except OSError:
#		print "salta exception"
#		return False



def get_directory_size(directory):
	"""Calcula el tamaño de todos los ficheros de un directorio (recursivamente) """
	dir_size = 0
	for (path, dirs, files) in os.walk(directory):
		for file in files:
			filename = os.path.join(path, file)
			dir_size += os.path.getsize(filename)

	return dir_size

def get_new_name(file):
	"""
	Devuelve un nombre nuevo, formado por un identificador único con:
	nombre-fichero/dir + fecha_última_modificación + fecha_borrado
	(ambas en formato segundos since epoch)
	"""
	return os.path.basename(os.path.abspath(file)) + "_" + str(time.time()) + "_" + str(os.path.getmtime(file))

def is_bigger_than(file, percentage):
	"""
	Devuelve true, si el fichero o directorio es mayor que el porcentaje recibido del home
	"""

	home_path = os.getenv("HOME")
	if home_path == None:
		msg="ERROR: variable de entorno HOME no definida"
		sys.stderr.write(msg + "\n")
		raise SystemExit
	else:
		threshold = get_directory_size(home_path) * percentage
		size = 0.0
		if os.path.isdir(file):
			size = get_directory_size(file)
		else:
			size = os.path.getsize(file)

		#print "homesize=" + str(threshold) + " file=" + str(size)
		return size>threshold

def copy_same_filesystem(file):
	"""
	Si es un fichero, realiza un enlace duro en la papelera, y lo borra.
	Si es un directorio, lo mueve a la papelera.

	Además se almacenarán persistentemente los datos.
	"""

	try: 
		new_name = get_new_name(file)
		store_data(file, new_name)		
		if(os.path.isdir(file)):
			shutil.move(file, os.path.join(papelera_path, new_name))
			print file + " ha sido envidado a la papelera de reciclaje (move)"
		else:
			os.link(file,os.path.join(papelera_path, new_name))
			os.remove(file)
			print file + " ha sido enviado a la papelera de reciclaje (enlace duro)"

	except OSError:
		#Esto no debería pasar porque fue previamente controlado, pero por si acaso
		sys.stderr.write("ERROR: Durante el envío a la papelera de " + file + "\n")

def copy_different_filesystem(file):
	"""
	Realiza una copia ordinaria del fichero/directorio en la papelera
	
	Si el tamaño es muy grande, pregunta para hacer borrado definitivo (ficheros)
	En el caso de los directorios, se pregunta siempre

	El nombre del enlace estará formado por un identificador único con:
	nombre-fichero + fecha_última_modificación + fecha_borrado
	(ambas en formato segundos since epoch)

	Además, se almacenarán persistentemente todos los datos
	"""

	try:		
		if is_bigger_than(file, 0.05):
			answer = ""
			while (True):
				answer = raw_input("¿Deseas borrarlo definitivamente? (S/N): ").upper()
				if (answer=="S" or answer =="N"):
					break
			if (answer=="S"):
				#Borrado definitivo, dependiendo de si es directorio o fichero
				if os.path.isdir(file):
					shutil.rmtree(file)
					print file + " ha sido borrado definitivamente (rmtree-dFS)"
				else:
					os.remove(file)
					print file + " ha sido borrado definitivamente (remove-dFS)"
			elif (answer=="N"):
				new_name = get_new_name(file)
				store_data(file, new_name)
				shutil.move(file, os.path.join(papelera_path, new_name))
				print file + " ha sido envidado a la papelera de reciclaje (move-dFS)"
		
		else:
			new_name = get_new_name(file)
			store_data(file, new_name)
			shutil.move(file, os.path.join(papelera_path, new_name))
			print file + " ha sido envidado a la papelera de reciclaje (move-dFS)"

	except OSError:
		sys.stderr.write("ERROR: No fue posible borrar " + file + "\n")
	

if __name__ == '__main__':
	global papelera_path
	papelera_path = get_papelera_path()
	state = check_params()
	if state==0:
		#Para cada uno de los argumentos, realizar el tipo de copia correspondiente
		i = 1
		while (i<len(sys.argv)):
			if same_systemfile(sys.argv[i]):
				copy_same_filesystem(sys.argv[i])
			else:
				copy_different_filesystem(sys.argv[i])

			i = i + 1
	
	sys.exit(state)
