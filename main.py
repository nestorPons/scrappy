#!/usr/bin/python3

from Modules.Scanner import Scanner
from Modules.Menu import Menu
from tabulate import tabulate

menu = Menu()
scann = Scanner()

menu.addOption('1', 'Obtener los telefonos', scann.getTels)
menu.addOption('2', 'Obtener los emails', scann.viewEmails)


t = menu.requestTarget('www.lebouquet.es')
scann.setTarget(t)
# Se inicia el scaneo de todas las páginas vinculadas
scann.scanLinks()

# Se muestra el menú y esperamos la respuesta 
response = menu.start()
if response[0] == 1:
    print(response[1][0])
    print(tabulate(response[1][1].items(), showindex=True))

elif response[0] == 2:
    pass