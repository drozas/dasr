#!/usr/bin/python -tt
# -*- coding: utf-8 -*-

import time,os, pickle

NOMBRE_FICHERO=os.path.join(os.getenv("HOME"),".mi_df.pick")

def lee_lista_de_diccionarios():
    global lista_de_diccionarios
    if os.path.exists(NOMBRE_FICHERO):
        fich=open(NOMBRE_FICHERO,'r')
        lista_de_diccionarios=pickle.load(fich)
        fich.close()
        return 1
    else:
        print NOMBRE_FICHERO + " no existe"
        return 0

def imprime():
    for x in lista_de_diccionarios:
        fecha_bruto=x['fecha']  # segundos desde 1/1/1970, como devuelve time.time()
        print time.ctime(fecha_bruto),   # convierte fecha en cadena legible
        print x['total']

def main():
    if lee_lista_de_diccionarios():
        imprime()


main()

