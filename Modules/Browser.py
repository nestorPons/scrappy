import mechanize
import re
from progress.bar import Bar, ChargingBar

class Browser:
    
    links = []
    target = ''
    actualStrKey = ''
    data = {}
    
    noLoads = []
    urls = []
    urlNoLoad = []
    
    def __init__(self, url):
        
        
        self.browser = mechanize.Browser()
        self.browser.set_handle_robots(False)
        self.browser. set_handle_robots(False)
        self.browser.addheaders = [("User-agent","Mozilla/5.0")]
        
        # Se carga la info de la url pasada por el usuario
        self.links.append(url)
        self.loadTarget(url)
        self.loadData(url)
        
    def loadTarget(self, link):
        try:
            # Abrimos la pagina objetivo
            self.browser.open(link)
            # Cargamos en el target el texto de la url
            self.target = self.browser.response().read().decode("utf-8") 
        except:
            self.urlNoLoad.append(link) 
            
        return self   
    
    def searchRef(self):
        _links = re.findall(r'<a.*?href=.?["|\'](.*?)["|\'?]', self.target)
        
        #iniciamos el contador
        bar = Bar('Procesando:', max= len(_links) )
                
        # Añade todos los links 
        for link in _links:
            bar.next()    
            # y filtra que no se repitan
            if link  not in self.links:
                #Filtramos y ponemos el dominio si no lo tuviera     
                if not re.search('^(https|http)+://', link):
                    link = self.links[0] + '/' + link
                
                self.links.append(link)
                
            # Extraemos la informacion de las paginas encontradas
            
            self.loadData(link)
        
        bar.finish()
        
        return self
    
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
            dic['tels'] = re.findall( r'[69][\d]{8}', self.target.replace(' ', ''))
            #buscar emails  
            dic['emails'] = re.findall(r'[\w\.-]+@[\w\.-]+', self.target)
            #buscar imagenes 
            dic['img'] = re.findall(r'<\s*img.*?src\s*=\s*["|\'](.*?\.jpg|png|jpeg|gif?)["|\'?]', self.target)

            # Cargamos variable data
            self.data[url] = dic

        except:
            # Guardamos array con las dir que no han cargado
            self.noLoads.append(url)      
    
    def getLinks(self):
        return self.links
    
    def getTels(self, key):
        key = self.checkey(key)
        return self.data[key]['tels']
    
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
        
    def viewTels(self, key):
        for t in self.getTels(key):
            print(t)
            
    def viewEmails(self, key):
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