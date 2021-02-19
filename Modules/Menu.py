import re
import requests
import sys 

class Menu:
    
    name = ''
    strOptions = ''
    mnuOptions = {}
    resOptions = {}
    result = None

    def __init__(self, menuName=''):
        self.name = menuName
        "clear" if sys.platform.startswith("linux") else "cls"
    
    def requestTarget(self, default = ''):
        try:
            self.res = input('Introduzca un objetivo url [{}]: '.format(default))
            if self.res == '':
                self.res = default
                
            self.res = self.isURL(self.res)
            print('Objetivo:', self.res)
            return self.res

        except ValueError as v:
            print('ERROR: url no válida!')
            self.requestTarget(default)

        except Exception as e:
            print(e)

    # Atrapa la respuesta del menú
    # Mensage -> menssaje alternativo 
    def start(self, menssage='Seleccione una opción: '):  
        print('\n'+self.name)
        print (self.strOptions, '\n')
        try: 
            index = int(input(menssage))
        except:
            print('\nERROR: Debe introducir un número de opción!!')
            self.start()
        #Ejecutamos el método vinculado al índice del menú seleccionado
        if self.mnuOptions[index] != None:
            result = self.mnuOptions[index]() or False
            # Ejecutamos la accion programada
            self.result = [index,result]
            # y ejecutamos la función de espuesta 
            try:
                if self.resOptions[index] != None:
                    self.resOptions[index](result)

            except Exception as e:
                print(e)
        else: 
            self.result = [res, False]

        return self.result

    # Solicita un dato para añadirlo a una funcion 
    def input(self, menssage='Introduzca los datos: ', function=None, typedata=int):
        try:
            r = typedata(input(menssage))
            return function(r)
            
        except ValueError:
            print('ERROR: Valor del dato incorrecto!!')
            self.input(menssage, function, typedata)
        except Exception as e:
            print(e)

    # Añade opciones al menu
    # indice, descripcion, función a ejecutar, función respuesta
    def addOption(self, index, description, action = None, response = None):
        self.mnuOptions[int(index)] = action
        self.resOptions[int(index)] = response
        self.strOptions = '{}\n{} {}'.format(self.strOptions, index, description) 

    def isURL(self, url):
        if url == '' or re.search('(.*?)\.(.*?)\.(.*?)', url):
            if not re.search('^(https|http)+://', url):
                try:
                    u = 'https://{}'.format(url)
                    requests.get(u)                
                except:
                    u = 'http://{}'.format(url)
                    requests.get(u)
                return u
            else:
                return url
        else:
            raise ValueError
    
    def getRes(self):
        return self.res

    def getResult(self):
        return self.result