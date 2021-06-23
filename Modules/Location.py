import requests
import re
import json 
import geocoder

from Modules.Conn import Conn
from progress.bar import Bar
from Modules.helpers import My
from Modules.Direccion import Direccion 
 
class Location:

    def __init__(self, country = 'España'):
        """
        Class search and check locations from Spain
        """    
        self._MARGIN = 100
        self._reset()
        # Conexion data base
        self._conn = Conn('./db/postal.db')
        self._country = country
        
    def set_country():
        pass 
    
    def _reset(self):
        """
        Reset private variables
        """
        self._data = []
        self._data_postal = [] 
        self._main_target= ''
        self._targets = []
        self._data_prov = []
        self._data_muni = []
        self._data_sniper = []
        self._data_directs = []
   
    def build_dirs(self):
        ok1 = []
        # Cargamos los objetivos y buscamos los que tengan el disparador con el patrón correcto
        for target in self._targets:
            try:
                direc = Direccion(self._country)
                direc.context = target  
                # Buscamos el tipo de via 
                direc.tipo = self.find_tipo(target)

                # Buscamos calle Y/o localizaciones
                direc.calle = self.find_direct(target, direc.tipo)           

                # Numero de portal
                direc.num = self.find_num(target, direc.calle)
                                                
                # Buscamos numeros de telefono
                direc.tels = self.find_all_tels()
                
                # Eliminamos las partes de direcciones del target para evitar confusiones
                target = target.replace(direc.num, '')
                target = target.replace(direc.calle, '')
                target = target.replace(direc.tipo, '')
                                
                # Buscamos los codigos postales 
                direc.cp = self.find_postal(target) 

                # Buscamos municipio 
                direc.muni = self.find_muni(target)
                target = target.replace(direc.muni, '')
                        
                # Buscamos provincias 
                direc.prov = self.find_prov(target, direc.cp)

                if direc.setcor(): 
                    self._data_directs.append(direc)
            except: 
                pass
        return self._data_directs
    
    def find_prov(self, target, cp=False):
        data = ''
        if self._data_prov == []: self.find_all_prov()
            
        for prov in self._data_prov: 

            if cp:
                c = self._conn 
                c.table('prov')
                i = cp[0:2]
                arr_prov = c.getById(i)
                data = arr_prov[0][1]
            else: 
                regex = f"\\b{prov}\\b"""
                m = re.findall(regex, target)
                if m: data = m[0]
                
        return data
                    
    def find_muni(self, target):
        data = ''
        if self._data_muni == []: self.find_all_muni()
        r = '|'.join(self._data_muni) 
        regex = f"\\b{r}\\b"
        for m in re.finditer(regex, target):
            if m!=[]: 
                data = m[0]
        return data
            
    def find_direct(self, target, tipo): 
        data = ''
        pattern = str(tipo)+'(\s)?([A-z]|\s){1,100}'
        
        for m in re.finditer(pattern, target):
            calle = m.group(0)
            calle = calle.replace(tipo,'',1)
            data = calle.strip()
            
        return data
        
    def find_tipo(self, target): 
        data = ''
        for match in self._data_sniper:
                t = match.group()
                data = t.strip()
                data = re.sub('\(|\)|\\\/', '', data)
        return data  
        
    def find_num(self, target, str_switch = False):
        data = ''
        if str_switch:
            pattern = str_switch + "[\s|Nn|\W]((\d){1,3})[\W|\s]"
            for match in re.finditer(pattern, target):
                data = match.group(1)
                
        return data
    
    def find_targets(self):
        """
        Search localitations streets, ...
        """
        data = {}
        sngt = []
        str_values = ''
        c = 0

        # shortest 
        arr2 = self._DataToArray('abre')
        str2 = '|'.join(arr2)
        str2 = My.normalize(str2, special=False)
        patt2 = f'\\b({str2})[\/|\.]'

        arr1 = self._DataToArray('vias')
        str1 = '|'.join(arr1)
        str1 = My.normalize(str1, special=False)
        patt1 = f'\\b({str1})\\b'

        pattern = f'({patt1})|({patt2})'

        for match in re.finditer(pattern, self._main_target):
            self._data_sniper.append(match)
            pos_start = match.start()
            pos_end = match.end() 
            
            pos_ini = pos_start - self._MARGIN
            if pos_ini < 0 : pos_ini = 0 
            pos_finish = pos_end + self._MARGIN
            content = self._main_target[pos_ini:pos_finish]
            content = My.strip_tags(content, incom=True)
            
            self._targets.append(content)

        return self._targets
    
    def find_all_tels(self):
        tels = []
        target = self._main_target
        target = target.replace(' ','')
        pres = self._DataToArray('pretels')
        repres = '|'.join(pres)
        pattern = f'\D(\+\d\d)?((6|7|{repres})(\d{{6,8}}))\D'
        
        for match in re.findall(pattern, target): 
            tel = match[1]
            # validando telefonos fijos
            if len(tel) >= 9 and not tel in tels :
                tels.append(tel)

        return tels
                

    def find_tels(self, target):
        pattern = '[\+]?\d[\W\d\s]{9,10}'
        data = []
        target = target.replace(' ','')
        for match in re.finditer(pattern, target):
            if match != []:
                f = match.group()
                f = f.replace(' ', '')
                data.append(f)
                  
        return data
        
    def find_postal(self, target):
        data = ''
        str_values = '|'.join(self._DataToArray('cp'))
        pattern = f'\\b({str_values})\\b'
        m = re.findall(pattern, target)
        if m:
            data = m[0]
        return data

    def find_all_prov(self):
        self._data_prov = self._find_loc('prov')
        return self._data_prov
    
    def find_all_muni(self):
        self._data_muni = self._find_loc('muni')
        return self._data_muni
        
    def _find_loc(self, table):
        """
        Search from data base
        """
        if self._main_target == '' : 
            print('No se ha asignado objetivo!!')
            exit()
        else: 
            matches = {}
            arr_matches = []
            provs = self._DataToArray(table)
            regex = '|'.join(provs)
            regex = regex.replace('/', '|')
            regex = My.normalize(regex)

            pattern = f'\W({regex})\W'
            string = self._main_target
            
            for match in re.findall(pattern, string):
                if isinstance(match, list) or isinstance(match, tuple): 
                    match =  match[0]
                # Load data
                if not match in self._data: 
                    self._data.append(match) 

                # Return for view
                if match in arr_matches:
                    matches[match] += 1
                else: 
                    arr_matches.append(match)
                    matches[match] = 1
                           
            return matches
        
    def _DataToArray(self, table, column = 'value'):
        # Obtain cities in array from data base
        self._conn.table(table)
        self._conn.getall(column)
        return self._conn.toArray()
    
            
    def _loopFor(self, func, arrdata):
        # Auxiliar function
        bar = Bar('Processing', max=len(arrdata))
        for a in arrdata:
            bar.next()
            func(a)
        bar.finish()
    
    # using property decorator
    # a getter function
    @property
    def target(self):
        return self._main_target       
    # a setter function
    @target.setter
    def target(self, a):
        self._main_target= My.normalize(a, special=False)