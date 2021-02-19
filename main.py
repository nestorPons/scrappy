#!/usr/bin/python3

from Modules.Scanner import Scanner
from Modules.Menu import Menu
from tabulate import tabulate

menu = Menu('Menú Principal')
menuOp = Menu('Menú opciones')
scann = Scanner()

def showTels(response):
    print(response[0])
    print(tabulate(response[1].items(), showindex=True))

def exitProgram():
    print('\nGracias por usar Scrappy')
    print('Hasta pronto!\n')

# Menu para cambiar el alcance
def inputScope(response):
    print('INPUTSCOPE')
    actualScope = scann.scope()
    menuOp.input('Seleccione el alcance deseado de 0-3, actual = {}: '.format(actualScope), scann.scope)

    if actualScope != scann.scope():
        # Se reescanea para adaptarlo al nuevo scope
        scann.scanLinks()

menu.addOption('0', 'Opciones', menuOp.start)
menu.addOption('1', 'Obtener los telefonos', scann.getTels, showTels)
menu.addOption('2', 'Obtener los emails', scann.viewEmails)
menu.addOption('5', 'Salir', None, exitProgram)

menuOp.addOption('1', 'Seleccion de alcance', scann.scope, inputScope )
menuOp.addOption('2', 'Otra opcion menu', scann.scope )

#Solicitamos el objetivo
t = menu.requestTarget('www.lebouquet.es')
scann.iniTarget(t)

# Se inicia el scaneo 
scann.scanLinks()

while True:
    # Se muestra el menú y esperamos la respuesta 
    response = menu.start()
    if response[0] == 5: break