import geocoder
import json

class Direccion:
    
    def __init__(self, pais = ''):
        self._status = False
        self._prediction = 0
        self._com = ''
        self._tipo = ''
        self._calle = ''
        self._num = ''
        self._prov = ''
        self._muni = ''
        self._cp = ''
        self._tels = []
        self._planta =''
        self._aux =''
        self._long = 0
        self._lat = 0
        self._context = ''
        self._pais = pais

    def checkgeo(self):
        
        self._status = False
        str1 = self.toString()
        g = geocoder.osm(str1)

        if g.ok:   
            try:        
                self._status = True
                self._prediction = g.importance 
            except Exception as e: 
                print(e)
                
        else:
            print('No se ha podido encontrar nada')
            print(g)
        
        return self._status
      
    def setcor(self):
        str1 = self.toString()
        g = geocoder.osm(str1)
        if g.ok: 
            self._prediction = g.importance
            self._calle = g.road            
            self._long = g.lng
            self._lat = g.lat
            self._aux = g.address
            self._prov = g.county
            self._muni = g.town or g.city
            self._com = g.state
            self._cp = g.postal
            self.check_status()
            
        return self._status
    
    def check_status(self):
        self._status = False
        if self._calle : self._status = True
        elif self._prov : self._status = True
        elif self._muni : self._status = True
        elif self._cp : self._status = True
        return self._status
    
    @property
    def prediccion(self):
        return self._prediction * 100       

    @prediccion.setter
    def prediccion(self, a):
        self._prediction= a
        
    @property
    def tels(self):
        return self._tel       

    @tels.setter
    def tels(self, a):
        self._tels= a
        
    @property
    def context(self):
        return self._context       

    @context.setter
    def context(self, a):
        self._context= a
        
    @property
    def tipo(self):
        return self._tipo       

    @tipo.setter
    def tipo(self, a):
        self._tipo= a
        
    @property
    def muni(self):
        return self._muni       
    @tipo.setter
    def tipo(self, a):
        self._tipo= a
        
    @property
    def muni(self):
        return self._muni  
    @muni.setter
    def muni(self, a):
        self._muni= a
        
    @property
    def calle(self):
        return self._calle       

    @calle.setter
    def calle(self, a):
        self._calle= a
    
    @property   
    def status(self):
        return self._status       

    @status.setter
    def status(self, a):
        self._status= a
    
    @property
    def num(self):
        return self._num       

    @num.setter
    def num(self, a):
        self._num= a
    
    @property
    def prov(self):
        return self._prov       

    @prov.setter
    def prov(self, a):
        self._prov= a
        
    @property
    def cp(self):
        return self._cp       

    @cp.setter
    def cp(self, a):
        self._cp= a
            
    def toString(self):
        nombre = ('',self._calle + ',')[self._calle!='']
        muni = ('',self._muni + ',')[self._muni!='']
        prov = ('',self._prov + ',')[self._prov!='']
        com =('',self._com + ',')[self._com!='']
        cp = ('',self._cp + ',')[self._cp!='']
        pais = self._pais or ''
        
        return nombre + muni + prov + com + cp + pais
        
    def string(self):
        status = ('False', 'OK')[self._status]
        tipo =  self._tipo or ''
        calle = self._calle or ''
        num = str(self._num) or ''
        prov = self._prov or ''
        cp = self._cp or ''
        muni = str(self._muni) or ''
        pais = self._pais or ''
        planta = self._planta or ''
        aux = self._aux or ''
        lon = str(self._long) or ''
        lat = str(self._lat) or ''
        tels = ','.join(self._tels)  or ''
        com = self._com or ''
        print(
            'Fiabilidad:' + str(self.prediccion) + '%\n',
            'Estado:' + status + '\n',    
            'Tipo: ' + tipo + '\n',
            'Vía: ' + calle + '\n', 
            'Numero: ' + num + '\n',
            'Provincia: ' + prov + '\n',
            'Codigo Postal: ' + cp + '\n',
            'Municipio: ' + muni + '\n',
            'Comunidad: ' + com + '\n',
            'Pais: ' + pais + '\n',
            'Planta: ' + planta + '\n',
            'Dirección: ' + aux + '\n',
            'Longitud: ' +  lon + '\n', 
            'Latitud: ' + lat + '\n',
            'Telefonos: ' + tels 
            ) 