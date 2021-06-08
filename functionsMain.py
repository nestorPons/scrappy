from tabulate import tabulate
import os 
import re
from Modules.Menu import Menu
from Modules.Img import Img
import wget
import exiftool

def endOption():
    
    input("\nPresione cualquier tecla para continuar...")
    os.system('clear')

def setTarget(tpl):
    (menu, config, scann) = tpl
    #Solicitamos el objetivo
    t = menu.requestTarget(config.data('target'))
    # Se guarda el nuevo objetivo si ha cambiado
    if t != config.data('target') : config.data('target', t)
    scann.reset()
    scann.iniTarget(t)
    # Se inicia el scaneo 
    scann.scanLinks()

    #whois del objetivo 
        
        

def printResponse(response, header=[], showindex=True):
    data = response[1]
    
    for k, v in data.items():
        print(k, '->', v)
    endOption()

def showImage(response):
    print('SHOW IMAGE')
    print(response)

# Muestra los datos del scaner
# [index, {url : [datos]}]
def showDataMenu (response, tpl=()):
    inFunc=None
    outFunc=None
    headers=[]
    
    if len(tpl) >= 1: inFunc = tpl[0]
    if len(tpl) >= 2: outFunc = tpl[1]
    if len(tpl) == 3: headers = tpl[2]
    try:
        mnu = Menu('Seleccione id para ampliar la información:')
        res = response[1]
        count = 1
        
        # Establecemos cabecera del menú
        if headers:
            mnu.setHeader(headers)

        # Opciopn salir
        mnu.addOption([0, 'Volver'], mnu.exit)
        for lbl, data in res[1].items():

            if inFunc: 
                if outFunc:
                    # Tiene funcion de entrada y de salida
                    mnu.addOption(data=[count, lbl, data], inOp=[inFunc, lbl], outOp=outFunc)      
                else:
                    # Tiene funcion de entrada
                    mnu.addOption(data=[count, lbl, data], inOp=[inFunc, lbl])
            else: 
                if outFunc:
                    # Tiene funcion de salida
                    mnu.addOption(data=[count, lbl, data], inOp=None, outOp=outFunc)
                else:
                    # Sin funciones de retorno
                    mnu.addOption(data=[count, lbl, data])
            count += 1
       
        mnu.start()
        #endOption()
    except Exception as e:
        print('ErrorshowDataMenu:', e)
        exit()

def exitProgram(response):
    print('\nGracias por usar Scrappy')
    print('Hasta pronto!\n')
    exit()

# Menu para cambiar el alcance
# Recibe un array con un diccionario {url: estado}
def showLinks(response):
    data = response[1]
    for k in data:
        print(k)
    #endOption()

# Menu para cambiar el alcance
def inputScope(response, tpl):
    try:
        (scann, menuOp, config) = tpl
        actualScope = scann.scope()
        value = menuOp.input('Seleccione el alcance deseado de 0-3, actual = {}: '.format(actualScope), scann.scope)  
        # Se guarda el dato en el archivo de configuración
        config.data('scope', value)
        menuOp.exit()

        if actualScope != scann.scope():
            # Se reescanea para adaptarlo al nuevo scope
            scann.scanLinks()
    except Exception as e:
        print(e)

def showrawdata(response, scann):
    print(scann.data)

def getImage(response):
    try:
        urlimage = response
        filename = re.sub(r'(https|http)+://', '', urlimage).strip()
        ext = re.findall(r'(\.[^.]+$)', filename)[0]

        filename.replace(ext, '')
        namefile = re.sub(r'\W','',filename)
        pathimage = 'targets/' + namefile + ext
        wget.download(urlimage, pathimage)

        # obtenemos los metadata
        files = [pathimage]  
        with exiftool.ExifTool() as et:  
            metadata = et.get_metadata_batch(files)  

        for k, v in metadata[0].items():
            print(k, '=>' , v)
 
        endOption()
    except Exception as e:
        print('getImage', e)
        exit()