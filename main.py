#!/usr/bin/python3

from Modules.Browser import Browser
from Modules.Menu import Menu

target = Browser()
menu = Menu(target)
res = menu.requestTarget('www.lebouquet.es')

# Buscamos todas las referencias
target.searchRef()
target.viewImages(0)
