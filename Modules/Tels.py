import requests
import re
from html.parser import HTMLParser


class WebParse(HTMLParser):

    def __init__(self, number):
        self.target = number

        url = 'https://www.numerosdetelefono.es/'+self.target
        self.htmlTxt = requests.get(url).text
        self.feed(self.htmlTxt)
        self.close()

    
    def getClasses(self, tag=False):
        css = re.findall(r'class\s?=\s?(["|\'])(.*?)\1', self.htmlTxt)
        print (css)


    def getByClassCSS(self):
        pass


parse = WebParse('660291797')