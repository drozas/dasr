#!/usr/bin/python -tt
# -*- coding: utf-8 -*-

#Autor: David Rozas (drozas)

import commands
import re
import time,os,pickle

NOMBRE_FICHERO=os.path.join(os.getenv("HOME"),".mi_df.pick")


def lee_lista_de_diccionarios():
	"""Devuelve la lista de diccionarios almacenada, o None si no existía el fichero """

	if os.path.exists(NOMBRE_FICHERO):
		fich=open(NOMBRE_FICHERO,'r')
		lista_de_diccionarios=pickle.load(fich)
		fich.close()
		return lista_de_diccionarios
	else:
		print NOMBRE_FICHERO + " no existe"
		return None


def print_df():
	"""Muestra la ejecución de df -l, y devuelve el espacio total"""

	p = commands.getstatusoutput('df -l')
	if (p[0]==0):
		print p[1]
		lineas = p[1].split('\n')
		nSistemas = str(len(lineas[1:]))
		espacioTotal = 0
		espacioUsado = 0
		espacioDisponible = 0
		for l in lineas[1:]:
			#Cortar con expresion regular por 1 o mas espacios
			datos = re.split(" +", l)
			espacioTotal = espacioTotal + int(datos[1])
			espacioUsado = espacioUsado + int(datos[2])
			espacioDisponible = espacioDisponible + int(datos[3])

		print "\n\nNúmero total de sistemas de ficheros montados : " + str(nSistemas)
		print "Espacio Total:" + str(espacioTotal)
		print "Espacio Usado:" + str(espacioUsado)
		print "Espacio Disponible:" + str(espacioDisponible)

		return espacioTotal

def guardar_lista(listaDirs):
	"""Almacena persistentemente (sobreescribiendo si existía el fichero) la lista de diccionarios"""

	fich = open(NOMBRE_FICHERO,'w')
	pickle.dump(listaDirs,fich)
	fich.close()
	

if __name__ == '__main__':
	total = print_df()
	diccionarios = lee_lista_de_diccionarios()

	#El diccionario estará formado por:
	dic = {}
	dic["fecha"] = time.time()
	dic["total"] = total

	if (diccionarios != None):
		#Si ya hay lista de diccionarios, añadimos el nuestro a la lista
		diccionarios.append(dic)
		guardar_lista(diccionarios)
	else:
		#Si no, inicializamos la lista
		l = []
		l.append(dic)
		guardar_lista(l)
