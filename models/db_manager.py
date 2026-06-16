from kivy.uix.recyclegridlayout import defaultdict
import sqlite3
import os

class DatabaseManager:
    def __init__(self, db_path='database.db'):
        self.db_path = db_path
        self.connection = None
        self.cursor = None

    def conectar(self):
        try:
            self.connection = sqlite3.connect(self.db_path)
            self.cursor = self.connection.cursor()
            self.cursor.execute("PRAGMA foreing_keys = ON;")
            return True
        except Exception as e:
            print(f"Error de conexión: {e}")
            return False
        
    def cerrar(self):
        if self.connection:
            self.connection.close()

    def ejecutar(self, sql, params=None):
        try:
            if params:
                self.cursor.execute(sql, params)
            else:
                self.cursor.execute(sql)
            
            self.connection.commit()
            return self.cursor.lastrowid
        except:
            return None
        
    def consultar(self, sql, params=None):
        try:
            if params:
                self.cursor.execute(sql, params)
            else:
                self.cursor.execute(sql)

            self.connection.commit()
            return self.cursor.fetchall()
        except:
            return None
    
    def consultar_uno(self, sql, params=None):
        resultados = self.consultar(sql, params)
        return resultados[0] if resultados else None
