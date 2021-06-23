#!venv/bin/python

import functionsMain as main
from Modules.Scanner import Scanner
from Modules.Menu import Menu
from Modules.Config import Config
from Modules.Tel import Tel
from Modules.Img import Img

try:
    # Menus del inicio
    menu = Menu('Menú Principal')
    menuOp = Menu('Menú de opciones')
    menuData = Menu('Menú de datos')
    menuLinks = Menu('Links escaneados')

    config = Config('config.json')
    scann = Scanner(cache=True, default=config.data())

    menu.addOption(['1', 'Establecer objetivo'], [main.setTarget, (menu, config, scann)])
    menu.addOption(['2', 'Obtener los telefonos'], [scann.getData,('tels')], [main.showDataMenu, (Tel.ntInfo, main.printResponse, ['ID', 'TELÉFONO', 'COINCIDENCIAS'])])
    menu.addOption(['3', 'Obtener los emails'], [scann.getData, ('emails')], main.showDataMenu)
    menu.addOption(['4', 'Obtener las imagenes'], scann.getImg, [main.showDataMenu,(main.getImage, None, None)])
    menu.addOption(['5', 'Buscar nombres'], scann.searchNames, [main.showDataMenu])
    menu.addOption(['6', 'Buscar direcciones'], scann.searchDirs, [main.printObjects])
    menu.addOption(['8', 'Opciones'], menuOp.start)
    menu.addOption(['9', 'Menú datos sin procesar'], menuData.start)
    menu.addOption(['0', 'Salir'],  menu.exit)

    menuData.addOption(['0', 'Salir al menú principal'], menuData.exit )
    menuData.addOption(['1', 'Ver urls escaneadas'], scann.getLinks, main.showLinks)
    menuData.addOption(['9', 'Ver los datos'], menuData.exit) 

    menuOp.addOption(['1', 'Seleccion de alcance'], scann.scope, [main.inputScope, (scann, menuOp, config)] )
    menuOp.addOption(['0', 'Salir al menú principal'], menuOp.exit )

    # Se inicia el menu Principal
    menu.start()
except Exception as e:
    print('Main:' , e)