import os, sys
import argparse
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)
 
from Modules.Conn import Conn

l = Conn('db/postal.db', 'cp')
print(l.getData('cp'))