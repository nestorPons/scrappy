import sqlite3

class Conn:

    def __init__(self, db_path, table = ''):
        self._path = db_path 
        self._data = False
        self._table = table
        self._sql_connection()


    def _sql_connection(self):
        try:
            con = sqlite3.connect(self._path)
            self._conn = con
            return con

        except Error:

            print(Error)

    def getById(self, key, column='*'):
        if self._table != '':
            cur = self._conn.cursor()
            str1 = f'SELECT {column} FROM {self._table} WHERE id={key}'
            cur.execute(str1)

            self._data = cur.fetchall()
            return self._data
        else: 
            raise Exception('No hay tabla seleccionada!!')    
        
    def getall(self, column='*'):
        if self._table != '':
            cur = self._conn.cursor()
            cur.execute(f'SELECT {column} FROM {self._table}')

            self._data = cur.fetchall()
            return self._data
        else: 
            raise Exception('No hay tabla seleccionada!!')
    
    def toArray(self):
        arr = []
        data = self._data 
        for d in data:
            arr.append(d[0])
        return arr

    #getter and setter
    def table(self, t = ''):
        if not t == '': 
            self._table = t

        return self._table