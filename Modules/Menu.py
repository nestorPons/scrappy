import re
import requests
import os


class Menu:
    
    def __init__(self, menuName=''):
        self.end = False
        self.name = menuName
        self.strOptions = ''
        self.mnuOptions = {}
        self.resOptions = {}
        os.system("clear")
    
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

    # Atrapa la respuesta del menú
    # Mensage -> menssaje alternativo 
    def start(self, menssage='Seleccione una opción: '):  
        while not self.end:
            result = None
            self.end = False

            print('\n'+self.name)
            print('--------------')
            print (self.strOptions, '\n')
            try: 
                index = int(input(menssage))
                if not index in self.mnuOptions: raise
            except:
                print('\nERROR: Numero de opción incorrecto!')
                self.start()
            
            funaction = self.mnuOptions[index]

            #Ejecutamos el método vinculado al índice del menú seleccionado
            if funaction != None:
                #Ejecutamos el método vinculado al índice del menú seleccionado
                if isinstance(funaction, list):
                    # Ejecución de función guardada y sus argumentos si los tiene
                    result = funaction[0](funaction[1])
                else:
                    result = funaction() or False

                # Ejecutamos la accion programada
                result = [index,result]
            else: 
                result = [index, False]

            funres = self.resOptions[index]
            if funres != None:
                try:
                    # y ejecutamos la función de espuesta 
                    if isinstance(funres, list):
                        # funcion (argumento de respuesta, argumentos vinculados)
                        funres[0](result, funres[1])
                    else:
                        if result:
                            funres(result)
                        else:
                            funres()

                except Exception as e:
                    print(e)

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

    # Añade opciones al menu
    # indice, descripcion, función a ejecutar, función respuesta
    # action = [nombre de funcion, argumentos]
    # response = [nombre de funcion, argumentos]
    def addOption(self, index, description, action = None, response = None):
        # se añade el parametro 0 para evitar futuros errores
        self.mnuOptions[int(index)] = action
        self.resOptions[int(index)] = response
        self.strOptions = '{}\n{} {}'.format(self.strOptions, index, description) 

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