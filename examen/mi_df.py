#!/usr/bin/python -tt
# -*- coding: utf-8 -*-

#Autor: David Rozas (drozas)

import commands
import re

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
