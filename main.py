#!/usr/bin/python3

from Modules.Scanner import Scanner
from Modules.Menu import Menu
import functionsMain as main
from Modules.Config import Config


menu = Menu('Menú Principal')
menuOp = Menu('Menú de opciones')
menuData = Menu('Menú de datos')
menuLinks = Menu('Links escaneados')

config = Config('config.json')
scann = Scanner(cache=True, default=config.data())

menu.addOption('0', 'Menu opciones', menuOp.start)
menu.addOption('1', 'Obtener los telefonos', [scann.getData,'tels'], [main.showData, ['ID', 'TELÉFONO', 'COINCIDENCIAS']])
menu.addOption('2', 'Obtener los emails', [scann.getData, 'emails'], main.showData)
menu.addOption('3', 'Obtener las imagenes', scann.getImg, main.showImages)
menu.addOption('8', 'Menú datos sin procesar', menuData.start)
menu.addOption('9', 'Salir',  menu.exit)

menuData.addOption('1', 'Ver urls escaneadas', scann.getLinks,main.showLinks)
menuData.addOption('9', 'Ver los datos', menuData.exit) 

menuOp.addOption('1', 'Seleccion de alcance', scann.scope, [main.inputScope, [scann, menuOp, config]] )
menuOp.addOption('9', 'Salir al menú principal', menuOp.exit )

#Solicitamos el objetivo
t = menu.requestTarget(config.data('target'))
# Se guarda el nuevo objetivo si ha cambiado
if t != config.data('target') : config.data('target', t)
scann.iniTarget(t)

# Se inicia el scaneo 
scann.scanLinks()


# Se inicia el menu Principal
menu.start()