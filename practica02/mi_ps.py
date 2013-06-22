#!/usr/bin/python -tt
# -*- coding: utf-8 -*-

#DASR - Práctica 2.1
#Autor: David Rozas (drozas)

import commands
import re

p = commands.getstatusoutput('ps -ef')
if (p[0]==0):
    
    #Cortar por retorno de carro para obtener lineas (ignoraremos cabecera en el resto del programa)
    lineas = p[1].split('\n')
    nProcesos = str(len(lineas[1:]))

    #Crear un diccionario con usuarios como claves, y lista de sus procesos como valores
    usuarios = {}
    for l in lineas[1:]:
	#Cortar con expresion regular por 1 o mas espacios
        datos = re.split(" +", l)
        
        if not((datos[0] in usuarios)):
            #Si no tenemos ese usuario almacenado, creamos una nueva entrada y una nueva lista para él, agregando ese elemento
            procesos = []
            procesos.append(datos[7])
            usuarios[datos[0]] = procesos
        else:
            #Si ya lo tenemos almacenado, agregamos el proceso a su lista
            usuarios[datos[0]].append(datos[7])
            
    #Transformar el diccionario en una lista, para mostrarlos ordenadamente.
    lUsuarios = usuarios.items()
    #En lugar de crear funcion de comparación, creamos una funcion lambda
    lUsuarios.sort(lambda x,y:len(y[1]) - len(x[1]))

    #Mostrar informacion
    print ("Número de procesos que se estan ejecutando: " + str(nProcesos))
    print ("Número de usuarios: " + str(len(lUsuarios)))
    #En u tenemos tuplas de : username+listaProcesos
    for u in lUsuarios:
        print ("\nEl usuario "  + u[0] + " tiene " + str(len(u[1])) + " procesos ")
        for p in u[1]:
            print ("\t" + p.replace("[","").replace("]","").replace(":",""))
        
else:
    print ('Hubo problemas al ejecutar el comando ps -ef')
