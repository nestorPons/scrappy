import os, sys
import argparse
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)
 
from Modules.Location import Location

l = Location()
p1 = "./caches/www_akkubatt_es_"
p2 = "./caches/www_lebouquet_es"
p3 = "./caches/kronox"
p4 = "./caches/multi"
p5 = "./caches/manu"
p6 = "./caches/simetria"
p7 = "./caches/lledo"
p = p1
if sys.argv[0]:
    if sys.argv[1] == 'p1': p = p1
    if sys.argv[1] == 'p2': p = p2
    if sys.argv[1] == 'p3': p = p3
    if sys.argv[1] == 'p4': p = p4
    if sys.argv[1] == 'p5': p = p5
    if sys.argv[1] == 'p6': p = p6
    if sys.argv[1] == 'p7': p = p7

with open(p, 'r') as filehtml:
    l.target = filehtml.read()
    l.find_targets()
    print('----------------')
    #print(l.find_prov())
    print('----------------')
    #print(l.find_muni())
    print('----------------')
    for d in l.build_dirs():
        print(d.print())
    # print(l._way_targets())
    # print(l.find_postal())
