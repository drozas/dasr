#!/usr/bin/python -tt
# -*- coding: utf-8 -*-

#DASR - Práctica 2.6
#Autor: David Rozas (drozas)

"""
Script que borra todos los ficheros mayores que el 0.1% del home.
"""

import borra
import os
import os.path
import pickle
import shutil

#Mantienen esta nomenclatura por el move: src el .new, dst el normal
src_persistence = os.path.join(borra.get_papelera_path(), ".persistencia.new")
dst_persistence = os.path.join(borra.get_papelera_path(), ".persistencia")

if os.path.exists(dst_persistence):
	fich = open(dst_persistence,"r")
	#fichero de persistencia temporal
	fich2 = open (src_persistence, "w")

	try:
		while True:
			fichero = pickle.load(fich)
			src_path = os.path.join(borra.get_papelera_path(), fichero[1])
			print "analizando " + src_path
			if borra.is_bigger_than(src_path, 0.001):
				if os.path.isdir(src_path):
					shutil.rmtree(src_path)
				else:
					os.remove(src_path)
				print "Eliminado: " + src_path 	
			else:
				#Lo añadimos al temporal
				pickle.dump(fichero, fich2)
	
	except EOFError:
		fich.close()
		fich2.close()
		shutil.move(src_persistence, dst_persistence)

else:
	print "Vacío"

