import re
import requests

class Menu:
    def __init__(self):
        self.res = input('Introduzca una url:')
        self.res = self.isURL(self.res)
        
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