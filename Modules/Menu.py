import re
import requests
import sys 

class Menu:
    
    strOptions = ''
    mnuOptions = {}

    def __init__(self):
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

    def start(self, default = None):  
        print (self.strOptions, '\n')
        try:
            res = int(input('Seleccione una opción: '))
        except:
            print('\nERROR: Debe introducir un número de opción!!')
            self.start()
        
        #Ejecutamos el método vinculado al índice del menú seleccionado
        return [res,self.mnuOptions[res]()]
        
    def addOption(self, index, description, action):
        self.mnuOptions[int(index)] = action
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