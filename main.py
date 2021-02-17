#!/usr/bin/python3

from Modules.Browser import Browser
from Modules.Menu import Menu

menu = Menu()

target = Browser(menu.getRes())
# Buscamos todas las referencias
target.searchRef()
target.viewImages(0)
