from tabulate import tabulate
import os 
import webbrowser
import re

def endOption():
    input("Presione cualquier tecla para continuar...")
    #os.system('clear')

# Muestra los datos del scaner
# [index, {url : [datos]}]
def showData(response, headers=[]):
    res = response[1]
    print(tabulate(res[1].items(), headers=headers, showindex=True))
    #endOption()


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
def inputScope(response, args):
    scann = args[0]
    menuOp = args[1]
    config = args[2]

    actualScope = scann.scope()
    value = menuOp.input('Seleccione el alcance deseado de 0-3, actual = {}: '.format(actualScope), scann.scope)  
    # Se guarda el dato en el archivo de configuración
    config.data('scope', value)
    menuOp.exit()

    if actualScope != scann.scope():
        # Se reescanea para adaptarlo al nuevo scope
        scann.scanLinks()
        
def showrawdata(response, args):
    scann = args[0] 
    print(scann.data)

def showImages(response):
    res = response[1]
    path = 'files/template.html'
    pathCache = 'files/cache_index.html';
    _file = open(path,'r')
    html = _file.read()
    _file.close()
    txt = ''
    for r in res:
        txt += '<img src="{}"/>'.format(r)
    htmlContent= re.sub(r'\$1', txt, html)
    _file = open(pathCache,'+w')
    _file.write(htmlContent)
    _file.close()
    webbrowser.open(pathCache)
    ##os.remove(pathCache)
