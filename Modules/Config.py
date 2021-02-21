import json

class Config():

    def __init__(self, pathfile):
        self.file = pathfile
        j = open(self.file, 'r')
        self._data = json.loads(j.read())
        j.close()
        
    #getter & setter
    def data(self, key=None, value=None):
        if key:
            if value:
                self._data[key]=value
                # Guarda el cambio en el archivo
                f = open(self.file,'w')
                f.write(json.dumps(self._data))
                f.close()
            return self._data[key]
        return self._data