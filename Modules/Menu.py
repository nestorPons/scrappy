import re
import requests
import os
from tabulate import tabulate

class Menu:
    
    def __init__(self, menuName='', table=False):
        self.format = table
        self.end = False
        self.name = menuName
        self.strOptions = ''
        self.lstOptions = []
        self.mnuOptions = {}
        self.outOptions = {}
        self._headers = ['ID', 'DESCRIPCIÓN']
    
    def requestTarget(self, default = ''):
        try:
            self.res = input('Introduzca un objetivo url [{}]: '.format(default))
            if self.res == '':
                self.res = default
                
            self.res = self.isURL(self.res)
            print('Objetivo:', self.res)
            return self.res

        except ValueError:
            print('ERROR: url no válida!')
            self.requestTarget(default)

        except Exception as e:
            print(e)

    # Establece la cabecera de la tabla
    def setHeader(self, header=[]):
        self._headers = header
        
    # Atrapa la respuesta del menú
    # Mensage -> menssaje alternativo 
    def start(self, menssage='Seleccione una opción: '): 
        os.system("clear")
        try:
            while not self.end:
                result = None
                self.showData(self.lstOptions)    
                try: 
                    index = int(input(menssage))
                    if not index in self.mnuOptions: raise ValueError
                except:
                    print('\nERROR: Numero de opción incorrecto!')
                    self.start()
                
                inArgs = self.mnuOptions[index]

                #Ejecutamos el método vinculado al índice del menú seleccionado
                if inArgs:
                    #Ejecutamos el método vinculado al índice del menú seleccionado
                    if isinstance(inArgs, list):
                        if len(inArgs) > 1:
                            # Ejecución de función guardada y sus argumentos si los tiene
                            result = inArgs[0](inArgs[1])
                        else:
                            result = inArgs[0]()
                    else:
                        result = inArgs()

                    # Ejecutamos la accion programada
                    result = [index,result]
                else: 
                    result = [index, False]
   
                # salida
                outOp = self.outOptions[index]
 
                if outOp:
                    print('a')
                    # Si tiene funcion de respuesta se ejecuta
                    if isinstance(outOp, list): 
                        print('b')
                        if len(outOp) > 1:
                            # funcion (argumento de respuesta, argumentos vinculados, [funcion de respuesta])
                            print('c', result, outOp)
                            outOp[0](result, outOp[1])
                        else:
                            outOp[0](result)
                    else:
                        outOp(result)

            # Se reestablece para poder volver a abrir el menu
            self.end = False
            os.system("clear")
        except Exception as e:
            print('Opción no disponible...')
            print(e)
            exit()

    # Solicita un dato para añadirlo a una funcion 
    def input(self, menssage='Introduzca los datos: ', function=None, typedata=int):
        try:
            r = typedata(input(menssage))
            function(r)
            return r
            
        except ValueError:
            print('ERROR: Valor del dato incorrecto!!')
            self.input(menssage, function, typedata)

        except Exception as e:
            print(e)


    def addOption(self, data, inOp = [], outOp = []):
        '''
        inFuncscripción ,datos a incluir en la tabla/menu
        @param [action] = list: [nombre de funcion, argumentos]
        @param [response] = list: [nombre de funcion, argumentos]
        '''
        try:
            index = data[0]
            self.mnuOptions[int(index)] = inOp
            self.outOptions[int(index)] = outOp
            self.lstOptions.append(data)   
    
            return self
        except Exception as e:
            print('Menu.addOption:', e)
            exit()

    # Se comprueba que tiene la forma de una url 
    def isURL(self, url):
        if url == '' or re.search(r'(.*?)\.(.*?)\.(.*?)', url):
            if not re.search(r'^(https|http)+://', url):
                try:
                    u = 'https://{}'.format(url)
                    requests.get(u)                
                except:
                    u = 'http://{}'.format(url)
                    requests.get(u)
                return u
            else:
                return url
        else:
            raise ValueError
    
    def exit(self):
        self.end = True

    def showData(self, data):
        print(
            tabulate(data, headers=self._headers)
        )
