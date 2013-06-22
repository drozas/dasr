#!/usr/bin/python -tt
# -*- coding: utf-8 -*-

#DASR - Práctica 3.5
#Autor: David Rozas (drozas)

""" Recodifica todos los ficheros (o ficheros contenidos en un directorio) a la codificación
estándar del sistema (si es un fichero de texto plano).
"""

import os.path
import sys
import commands
import os
import shutil

def check_params(files2convert):
	if (len(sys.argv)>1):
		#Comprobar que los argumentos existen y son texto plano, y preparar el diccionario en el 
		#que guardaremos los paths y codificación de cada uno de ellos

		i = 1
		while (i<len(sys.argv)):
			if (os.path.exists(sys.argv[i])):
				if ((os.path.isdir(sys.argv[i]))):
					for root, dirs, files in os.walk(sys.argv[i]):
						for f in files:
							if is_plain_text(os.path.join(root,f)):
								addFile(os.path.join(root,f), files2convert)
							else:
								print os.path.join(root,f) + " no es un fichero de texto. Se ignora.\n"

				elif((os.path.isfile(sys.argv[i]))):
					if is_plain_text(sys.argv[i]):
						addFile(sys.argv[i], files2convert)
					else:
						print sys.argv[i] + " no es un fichero de texto. Se ignora.\n"

			else:
				print sys.argv[i] + " no existe. Se ignora.\n"
			i = i + 1 

		return 0
	else:
		sys.stderr.write("Uso: ./mi_recode.py [fichero|dir]+\n")
		return -1

def is_plain_text(file):
	""" 
	Devuelve true si el fichero es un fichero de texto plano,
	false en cualquier otro caso
	"""
	
	command = "file --mime " + file
	r = commands.getstatusoutput(command)
	if (r[0]==0):
		trozos = r[1].split(" ")
		return trozos[1]=="text/plain;"
	else:
		print"Error al ejecutar: " + command
		return False

def get_charset(file):
	"""
	Devuelve true si el fichero es un fichero de texto plano,
	false en cualquier otro caso
	"""

	command = "file --mime " + file
	r = commands.getstatusoutput(command)
	if (r[0]==0):
		#Recortamos el campo charset, y de ahí su valor
		trozos = r[1].split(" ")
		return trozos[2].split('=')[1]
	else:
		print "Error al ejecutar: " + command
		return None

def addFile(file, d):
	"""
	Añade el fichero al diccionario para procesarlo, asociándole su codificación actual. 
	Además si el fichero original no tiene extensión, se la añadirá (.txt)
	"""

	#Tomamos su nombre, y vemos si tiene extensión txt
	filename = os.path.split(file)[1]
	if (len(filename.split("."))<=1):
		try: 
			new_path = file + ".txt"
			shutil.move(file, new_path)
			print file + " no tenía extensión. Ha sido renombrado como " + new_path + "\n"
			d[new_path] = get_charset(new_path)
		except (IOError):
			print "No fue posible renombrar " + file + ".No tienes permisos.\n"
	else:
		d[file] = get_charset(file)



def get_default_charset():
	""" 
	Devuelve la codificación por defecto del sistema, basándose en
	la variable de entorno LANG (preguntar si es la mejor forma)
	"""

	return (os.getenv("LANG").split('.')[1]).lower()



def addSufix(files):
	"""
	Comprueba si los ficheros tienen sufijo, y se lo añade si no lo tienen.
	Utiliza la estructura de ficheros temporal, pero debido a que no se permite
	modificar el diccionario en el bucle, lo que haremos es devolver uno nuevo actualizado
	"""
	new_dictionary = {}
	
	for f in files : 
		print f + " es un fichero en " + files[f]
		filename = os.path.split(f)[1]
		if (len(filename.split("."))<=2):
			try:
				#El nuevo path será: path de file + filename + nueva extensión
				new_path = os.path.join(os.path.split(f)[0], (filename.split(".")[0] + "." + files[f] + ".txt") )
				print "Renombrando " + f + " a " + new_path + "\n"
				shutil.move(f, new_path)

				#Agregamos la nueva entrada al diccionario auxiliar
				new_dictionary[new_path] = files[f]
			except (IOError):
				print "No fue posible renombrar " + f + ". No tienes permisos suficientes\n"
		else:
			print "No es necesario renombrar\n"

			#Agregamos la vieja entrada al diccionario auxiliar
			new_dictionary[f] = files[f]

	return new_dictionary


def copyDefaultCharset(files, default_charset):
	"""
	Realiza una copia del fichero en el formato estándar del sistema, recodificando
	si fuera necesario.
	"""
	for f in files:
		new_path = os.path.join(os.path.split(f)[0] ,(os.path.split(f)[1].split(".")[0] + ".txt"))
		print f
		#Copiamos el fichero en cualquier caso, y recodificamos si fuera necesario (recode no copia)
		try:
			shutil.copy(f, new_path)
			if (files[f]==default_charset):
				print "No es necesario recodificar. Copiado en " + new_path + "\n"
			else:
				command = "recode " + files[f] + ".." + default_charset + " " + new_path
				print "Recodificando a " + default_charset + " en " + new_path + " (" + command + ")\n"
				r = commands.getstatusoutput(command)
				if (r[0]!=0):
					print "Error al ejecutar " + command
		except (IOError):
			print "No tienes permisos suficientes en el fichero " + f + ". Se omitirá su copia\n"



if __name__ == '__main__':
	
	
	#Diccionario cuyas claves serán los paths de los ficheros a convertir, y cuyos valores su codificación
	files2convert = {}

	default_charset = get_default_charset()

	print "\n\tAnálisis de parámetros\n\t=======================\n"
	state = check_params(files2convert)
	
	if (state == 0 and len(files2convert)>0):

		#En este punto, en nuestro diccionario, todas las claves tendrán el formato:
		#fichero.txt o fichero.[cod].txt. A continuación, vemos si es necesario añadirles sufijo
		
		print "\n\tAdición de sufijos\n\t==================\n"
		files2convert = addSufix(files2convert)

		#En este punto, en nuestro diccionario todas las claves son del estilo file.[cod].txt
		#Por último, habrá que hacer una copia en el formato actual (recodificando si es necesario)
		
		print "\n\tCopiando a formato estándar\n\t===========================\n"
		print "Codificación por defecto: " + default_charset + "\n"
		copyDefaultCharset(files2convert, default_charset)
			
	sys.exit(state)
