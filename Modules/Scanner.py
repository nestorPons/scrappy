import mechanize
import re
from progress.bar import Bar, ChargingBar

class Scanner:
        
    def __init__(self):
        self._scope = 0
        self.links = []
        self.target = ''
        self.actualTarget = ''
        self.actualStrKey = ''
        self.data = {}

        self.noLoads = []
        self.urls = []
        self.urlNoLoad = []

        self.browser = mechanize.Browser()
        self.browser.set_handle_robots(False)
        self.browser. set_handle_robots(False)
        self.browser.addheaders = [("User-agent","Mozilla/5.0")]
    
    # Establecemos el objetivo del escaneo
    def iniTarget(self, url):
        try:
            # Se carga la info de la url pasada por el usuario
            self.links.append(url)
            self.loadTarget(url)
            self.loadData(url)
            self.target = url
            if len(self.urlNoLoad) != 0: raise ValueError

        except ValueError as e:
            print ('No se ha podido cargar la pagina:', url)
            print(e)
            
        except Exception as e:
            print(e)
            self.__init__()

        return self
    
    def loadTarget(self, link):
        try:
            # Abrimos la pagina objetivo
            self.browser.open(link)
            # Cargamos en el target el texto de la url
            self.actualTarget = self.browser.response().read().decode("utf-8") 
        except:
            self.urlNoLoad.append(link) 
            
        return self   
    
    def scanLinks(self):
        try:
            _links = re.findall(r'<a.*?href=.?["|\'](.*?)["|\'?]', self.actualTarget)
            
            #iniciamos el contador
            bar = Bar('Obteniendo datos:', max= len(_links) )

            # Añade todos los links 
            for link in _links:
                bar.next()    
                #Filtrado por el nivel de alcance 
                if self.filterScope(link):
                    # y filtra que no se repitan
                    if link  not in self.links:
                        #Filtramos y ponemos el dominio si no lo tuviera     
                        if not re.search('^(https|http)+://', link):
                            link = self.target + '/' + link
                    
                        self.links.append(link)

                    # Extraemos la informacion de las paginas encontradas
                    self.loadData(link)
            
            bar.finish()
            
            return self
        except Exception as e:
            print(e)

    # Filtra el nivel de scope 
    def filterScope(self, url) -> bool:
        # Solo escanea la pagina principal
        if self._scope == 0:
            return url == self.target
        # Escanea los links dentro del dominio
        elif self._scope == 1:
                return re.search('.*?'+self.target+'.*?', url)
        elif self._scope == 2:
            pass
        elif self._scope == 3:
            pass
        else:
            pass

    def loadData(self, url):
        try:
            url = url.replace('/imgres?imgurl=','')
            # Cargamos en el array de paginas scaneadas
            self.urls.append(url)
            # Abrimos y cargamos la pagina en variable de trabajo
            self.loadTarget(url)
            # buscamos en los datos 
            # Cargamos los datos en data
            dic = {}
            #buscar telefonos  
            dic['tels'] = re.findall( r'[69][\d]{8}', self.actualTarget.replace(' ', ''))
            #buscar emails  
            dic['emails'] = re.findall(r'[\w\.-]+@[\w\.-]+', self.actualTarget)
            #buscar imagenes 
            dic['img'] = re.findall(r'<\s*img.*?src\s*=\s*["|\'](.*?\.jpg|png|jpeg|gif?)["|\'?]', self.actualTarget)

            # Cargamos variable data
            self.data[url] = dic

        except:
            # Guardamos array con las dir que no han cargado
            self.noLoads.append(url)      
    
    def getLinks(self):
        return self.links
       
    def getEmails(self, key):
        key = self.checkey(key)
        return self.data[key]['emails']
    
    def getImages(self, key):
        key = self.checkey(key)
        return self.data[key]['img']

    def checkey(self, key):
        if isinstance(key, (int) ):   
            self.actualStrKey = self.links[key]  
        else:
            self.actualStrKey = key
        return self.actualStrKey
    # Vistas
    
    def viewNoLoad(self):
        print('No se han podido cargar:')
        for url in self.urlNoLoad:
            print(url)
    
    def viewUrls(self):
        print('URLS encontradas:')
        for url in self.urls:
            print(url)

    def viewData(self):
        print('Información encontrada:')
        for url,data in self.data.items():
            print(url)
            print(data)
            
    def report(self):
        self.printUrls()
        print('\n')
        self.printData()
        print('\n')
        self.printNoLoad()
        
    def getTels(self):
        tels = {}
        response = []
        count = {}
        # Si no se pasa llave se listan todos los diccionarios
        for url in self.data.keys():       
            count = 0
            for t in self.data[url]['tels']:
                count += 1
                tels[t] = count 
       
            response.append([url,tels])

        return response[0]
            
    def viewEmails(self, key):
        # Si no se pasa llave se listan todos los diccionarios
        if key==None:
            for k in self.data.keys():
                for t in self.data[k]['emails']:
                    print(t)
        else:
            for t in self.getEmails(key):
                print(t)
        
    def viewImages(self, key):
        for t in self.getImages(key):
            if not re.search('^(https|http)+://', t):
                if self.actualStrKey[len(self.actualStrKey)-1] != '/':
                    
                    print('{}/{}'.format(self.actualStrKey, t))
                else:
                    print(self.actualStrKey + t)
            else:
                print(t)

    #getter and setter
    def scope(self, val=None):
        try:
            if val != None:
                if int(val) > 3:
                    print('Valores permitidos:')
                    print('0 -> Escanea la pagina actual. [Por defecto]')
                    print('1 -> Escanea opcion 0 y los vínculos de su dominio')
                    print('2 -> Escanea opcion 1 y vinculos relacionados')
                    print('3 -> Escanea opcion 2 y los dominios de los vínculos relacionados')
                    print('Seleccione una nueva opción')
                    self.scope()
                else:
                    self._scope = val
            return self._scope
        except ValueError:
            print('Ingrese un numero de opción')
            self.scope()