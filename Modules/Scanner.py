import mechanize
import requests
import re
from progress.bar import Bar, ChargingBar

class Scanner:
        
    def __init__(self, cache=False, default = {}):
        self._scope = 0
        if default:
            self._scope = default['scope']
        self.cache = cache
        self.reset()

    def reset(self):
        self.links = []
        self.target = ''
        self.dataTarget = ''
        self.actualStrKey = ''
        self.data = {}

        self.noLoads = []
        self.urls = []
        self.urlNoLoad = []

        self.browser = mechanize.Browser()
        self.browser.set_handle_robots(False)
        self.browser.set_handle_robots(False)
        self.browser.addheaders = [("User-agent","Mozilla/5.0")]

    # Establecemos el objetivo del escaneo
    def iniTarget(self, url):
        try:
            # Se carga la info de la url pasada por el usuario
            self.links.append(url)
            self.loadTarget(url)
            self._loadData(url)
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

        def get(link, nameFile):
            # Abrimos la pagina objetivo
            self.browser.open(link)
            # Cargamos en el target el texto de la url
            self.dataTarget = self.browser.response().read().decode("utf-8") 
            try:
                # Guarda el get en la carpeta caches
                cache = open('caches/'+nameFile,'+w')
                cache.write(self.dataTarget)
            except: 
                print('Error al cachear el archivo!')

        # Se crea nombre del archivo cache
        nameFile = re.sub(r'(https|http)+://', '', link).strip()
        nameFile = re.sub(r'\W','_',nameFile)
        try:
            if self.cache:
                try:
                    f = open('caches/'+nameFile, 'r')
                    self.dataTarget = f.read()
                except:
                    get(link, nameFile)
            else:
                get(link, nameFile)
        except:
            # Guarda las urls que no se han podido acceder
            self.urlNoLoad.append(link) 
            
        return self   
    
    # Obtiene los enlaces del objetivo
    def scanLinks(self):
        try:
            _links = re.findall(r'<a.*?href=.?["|\'](.*?)["|\'?]', self.dataTarget)
            
            #iniciamos el contador
            bar = Bar('Obteniendo datos:', max= len(_links) )

            # Añade todos los links 
            for link in _links:
                # Construimos la url si el link la tiene dinámica
                if not re.search(r'^(https|http)+://', link):
                    link = self.target + '/' + link

                bar.next()   
                #Filtrado por el nivel de alcance 
                if self.filterScope(link):
                    # y filtra que no se repitan
                    if link  not in self.links:
                        # se añade al array de links a scanear
                        self.links.append(link)
                        # Extraemos la informacion de las paginas encontradas
                        self._loadData(link)
            
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
            match = re.search(r'.*?'+self.target+r'.*?', url) 
            return match != None
        elif self._scope == 2:
            match = re.search(r'(.*?)\.(.*?)\.(.*?)', url) 
            return match != None
        elif self._scope == 3:
            pass

    def _loadData(self, url):
        try:
            url = url.replace(r'/imgres?imgurl=','')
            # Cargamos en el array de paginas scaneadas
            self.urls.append(url)
            # Abrimos y cargamos la pagina en variable de trabajo
            self.loadTarget(url)
            # buscamos en los datos 
            # Cargamos los datos en data
            dic = {}
            #buscar telefonos  
            dic['tels'] = re.findall( r'[69][\d]{8}', self.dataTarget.replace(' ', ''))
            #buscar emails  
            dic['emails'] = re.findall(r'[\w\.-]+@[\w]+\.?[a-zA-Z]{2,5}', self.dataTarget)
            #buscar imagenes 
            dic['img'] = re.findall(r'<\s*img.*?src\s*=\s*["|\'](.*?\.jpg|png|jpeg|gif?)["|\'?]', self.dataTarget)
            #buscar nombres 
            dic['names'] = self.searchNames()
            print(dic['names'])
            # Guardamos los datos
            self.data[url] = dic
            # print(self.data)
        except:
            # Guardamos array con las dir que no han cargado
            self.noLoads.append(url) 
            
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
            print(names)
            return names

        except Exception as e:
            print('ERROR searchNames:', e)

    def getLinks(self):
        return self.links

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
        for value in self.data.values():
            print(value) 

    def getData(self, key):
        response = []
        data = {}
        # Se listan todos los datos de determinada llave
        for url in self.data.keys():       
            count = 0
            for t in self.data[url][key]:
                count += 1
                data[t] = count 
       
            response.append([url,data])

        return response[0]

    def getImg(self):
        try:
            dic = {}
            # Componemos la url de las imagenes para poder linkear
            for k, v in self.getData('img')[1].items():
                nk = k
                if not re.search(r'^(https|http)+://', nk):
                    nk = re.sub(r'\.\/','',nk)
                    nk = self.target +'/'+ k
                dic[nk] = v


            return [self.target, dic]
            
        except Exception as e:
            print('getImage:', e)

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
            print('Error: Valor incorreto!')
            self.scope()