#!/usr/bin/python -tt
# -*- coding: utf-8 -*-

#DASR - Práctica 2.5
#Autor: David Rozas (drozas)

""" Script que simula una cola de compradores, que se modifica con la 
recepción de señales SIGUSR1 y SIGUSR2 """

import os.path
import sys
import signal

#Listas globales, que mantienen la lista de clientes del fichero /etc/passwd y la cola actual
customers = []
queue = []

def load_customers():
	""" Carga la lista de compradores del fichero /etc/passwd"""
	global customers
	if (os.path.exists("/etc/passwd") and os.path.isfile("/etc/passwd")):
		file = open("/etc/passwd", "r")

		for l in file.readlines():
			u = l.split(":")
			customers.append(u[0])

		file.close()
		return 0
	else:
		sys.stderr.write("Error: Imposible leer clientes de /etc/passwd")
		return -1

def llega_cliente(nombre_comprador):
	"""Añade un cliente a la cola global. Detiene la ejecución si el nombre de
	comprador no es un string"""
	if (isinstance(nombre_comprador,str)):
		global queue
		queue.append(nombre_comprador)
	else:
		sys.stderr.write(str(nombre_comprador) +  " no es un string. Fin de ejecución.\n")
		raise SystemExit

def cliente_pagando():
	"""Extrae un cliente de la cola"""
	global queue
	if (len(queue)>0):
		print (queue.pop(0) + " sale de la cola.")
	else:
		print ("No hay clientes que eliminar")

def imprime_cola():
	"""Muestra el contenido de la cola por stdout"""
	global queue
	print ("Cola del super")
	if (len(queue)>0):
		print ("Total : " + str(len(queue)) + " clientes")
		for c in queue:
			print c
	else:
		print ("Vacía")

def signal_handler_sigusr1(signum, frame):
	"""Agrega un cliente a la cola y la imprime. 
		
	Además lo elimina de customers, que es donde llevamos la cuenta de los que quedan
	(produce fin de ejecución en main)
	"""
	llega_cliente(customers.pop(0))
	imprime_cola()

def signal_handler_sigusr2(signum, frame):
	"""Elimina un cliente de la cola, y la imprime"""
	cliente_pagando()
	imprime_cola()	

if __name__ == '__main__':
	state = load_customers()
	if (state==0):
		print ("Arrancado con pid = " + str(os.getpid()))

		#Mientras haya customers, atender señales
		signal.signal(signal.SIGUSR1, signal_handler_sigusr1)
		signal.signal(signal.SIGUSR2, signal_handler_sigusr2)
		while (len(customers)>0):
			None
		print ("Ya no hay más clientes en /etc/passwd. Fin de ejecución.")

	sys.exit(state)
