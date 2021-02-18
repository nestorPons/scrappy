import re
import requests

class Menu:
    def __init__(self, object):
        pass
    
    def requestTarget(self, default = ''):
        self.res = input('Introduzca un objetivo url [{}]: '.format(default))
        if self.res == '':
            self.res = default
            
        self.res = self.isURL(self.res)
        return self.res
    
    def mainMenu(self):   
        res = input('''
              Seleccione una opción:
              1 Obtener las imagenes\n
              2 Obtener las urls\n
              3 Obtener los emails\n
              4 Crear informe\n
              ''')
        if res == 1:
            res = input('Seleccione objetivo [Todo]')
            if re == '': 
                
    
    def isURL(self, url):
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
    def getRes(self):
        return self.res