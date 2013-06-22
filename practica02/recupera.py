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
		sys.stderr.write("Uso: ./recupera.py <num_positivo>+\n")
		return None

def recover_files(numeros):
	"""
	Restaura desde la papelera todos los ficheros cuyos números hayan sido recibidos como argumentos.
	Si el número no corresponde a ningún fichero, se ignora
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
					#Mover el fichero a su destino original (o a este path si hubo problemas)
					try:
						dest_path = fichero[2]
						src_path = os.path.join(borra.get_papelera_path(), fichero[1])
						shutil.move(src_path, dest_path)
						print "Restaurado " + src_path + " a " + dest_path

					except IOError:
						#Ofrecer meterlo en el path actual
						answer= ""
						dest_path = os.path.join(os.getcwd(), os.path.basename(fichero[0]))

						while (True):
							answer = raw_input("No fue posible guardarlo la localización original. ¿Desea guardarlo en " + dest_path + " (S/N): ").upper()
							if (answer=="S" or answer =="N"):
								break
						if (answer=="S"):
							shutil.move(src_path, dest_path)
							print "Restaurando " + src_path + " a " + dest_path
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
		recover_files(numeros)
