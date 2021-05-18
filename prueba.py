#!/usr/bin/python3

import requests
import re

class p:
    def __init__(self):
        

    def searchRAE(self, work) -> str:
        url = 'https://apirae.herokuapp.com/buscar/{}'
        json = requests.get( url.format(work))
        r = re.findall(r'<div id=[\"|\']resultados[\"|\']>(.*?)<\/div>', html)[0]
        
        return r

    def searchNames(self):
        try:
            target = self.dataTarget
            # Obtenemos nombres compuestos
            regex = r'([A-Z+].*?\s[A-Z+].*?)[\s|$]'
            names = re.findall(regex, target)
            target = re.sub(regex, '', target)  
            print(names)
            regex = r'([A-Z+].*?)+[\s|$]'
            names.append(re.findall(regex,target))
            target = re.sub(regex, '', target)
            # Obtenemos los nombres simpes
            return names

        except Exception as e:
            print('ERROR searchNames:', e)
