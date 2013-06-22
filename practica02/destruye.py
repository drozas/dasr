#!/usr/bin/python -tt
# -*- coding: utf-8 -*-

#DASR - Práctica 2.6
#Autor: David Rozas (drozas)

""" Script que permite la recuperación de ficheros de la papelera de reciclaje"""

import sys
import borra
import os
import os.path
import pickle
import shutil

def parse_params():
	""" Comprueba que hay al menos un argumento, y que todos ellos son enteros mayores que 1
	Devuelve una lista con los números parseados como enteros si todo fue correcto, None
	si hubo algún problema"""
	if (len(sys.argv)>1):
		#Comprobar que todos los argumentos existen
		i = 1
		numeros = []
		try:
			while (i<len(sys.argv)):
				n = int(sys.argv[i])
				if n>=1:
					numeros.append(n)
					i = i + 1
				else:
					raise ValueError

			return numeros

		except ValueError: 
			sys.stderr.write("Uso: Algunos de los argumentos no eran números positivos\n")
			return None
	else:
		sys.stderr.write("Uso: ./destruye.py <num_positivo>+\n")
		return None

def delete_files(numeros):
	"""
	Destruye en la papelera todos los ficheros cuyos números hayan sido recibidos como argumentos,
	previa confirmación. Si el número no corresponde a ningún fichero, se ignora
	"""
	path = os.path.join(borra.get_papelera_path(), ".persistencia")
	if os.path.exists(path):
		fich = open(path,"r")
		#fichero de persistencia temporal
		fich2 = open (os.path.join(borra.get_papelera_path(), ".persistencia.new"), "w")
		try:
			i = 1
			while True:
				fichero = pickle.load(fich)
				if i in numeros:
					try:
						src_path = os.path.join(borra.get_papelera_path(), fichero[1])
						answer= ""

						while (True):
							answer = raw_input("Se va a proceder a borrar definitivamente " + src_path + " ¿Confirma la acción? (S/N): ").upper()
							if (answer=="S" or answer =="N"):
								break
						if (answer=="S"):
							#Borrar fichero/directorio
							if (os.path.isdir(src_path)):
								shutil.rmtree(src_path)
							else:
								os.remove(src_path)
							print src_path + " ha sido borrado definitivamente"
						elif (answer=="N"):
							#Si la accion no se ha confirmado, guardar en persistencia.
							pickle.dump(fichero, fich2)
					
					except IOError,OSError:
						#Deshacer acción
						pickle.dump(fichero, fich2)
						msg="ERROR: No fue posible borrar " + src_path
						sys.stderr.write(msg + "\n")
				else:
					#Lo añadimos al temporal
					pickle.dump(fichero, fich2)
				i = i + 1
		except EOFError:
			fich.close()
			fich2.close()
			#Sobreescribimos el archivo original
			src = os.path.join(borra.get_papelera_path(), ".persistencia.new")
			dst = os.path.join(borra.get_papelera_path(), ".persistencia") 
			shutil.move(src, dst)
	else:
		print "Papelera vacía"

if __name__ == '__main__':
	numeros = parse_params()
	if numeros == None:
		sys.exit(-1)
	else:
		delete_files(numeros)
