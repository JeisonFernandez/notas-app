import sqlite3

class DatabaseManager:
    # Constructor
    def __init__(self, db_path="database.db"):
        self.db_path = db_path
        self.connection = None
        self.cursor = None
    
    def conectar(self):
        try:
            self.connection = sqlite3.connect(self.db_path)
            self.cursor = self.connection.cursor()
            self.cursor.execute("PRAGMA foreign_keys = ON;")
            return True
        except Exception as e:
            print(f"Error conexión: {e}")
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
        except Exception as e:
            print(f"Error ejecutar: {e}")
            return None
    
    def consultar(self, sql, params=None):
        try:
            if params:
                self.cursor.execute(sql, params)
            else:
                self.cursor.execute(sql)
            return self.cursor.fetchall()
        except Exception as e:
            print(f"Error consultar: {e}")
            return []
    
    def consultar_uno(self, sql, params=None):
        resultados = self.consultar(sql, params)
        return resultados[0] if resultados else None
    
    def crear_tablas(self):
        # Crea todas las tablas necesarias para la app

        sql_profesores = '''
        CREATE TABLE IF NOT EXISTS profesores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            nombre TEXT NOT NULL,
            fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        '''
        
        sql_estudiantes = '''
        CREATE TABLE IF NOT EXISTS estudiantes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cedula TEXT UNIQUE NOT NULL,
            nombres TEXT NOT NULL,
            apellidos TEXT NOT NULL,
            pnf TEXT NOT NULL,
            trayecto INTEGER NOT NULL,
            seccion TEXT NOT NULL,
            fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        '''
        
        sql_materias = '''
        CREATE TABLE IF NOT EXISTS materias (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            profesor_id INTEGER NOT NULL,
            fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (profesor_id) REFERENCES profesores(id) ON DELETE CASCADE
        )
        '''
        
        sql_inscripciones = '''
        CREATE TABLE IF NOT EXISTS inscripciones (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            estudiante_id INTEGER NOT NULL,
            materia_id INTEGER NOT NULL,
            periodo TEXT NOT NULL,
            fecha_inscripcion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (estudiante_id) REFERENCES estudiantes(id) ON DELETE CASCADE,
            FOREIGN KEY (materia_id) REFERENCES materias(id) ON DELETE CASCADE,
            UNIQUE(estudiante_id, materia_id, periodo)
        )
        '''
        
        sql_notas = '''
        CREATE TABLE IF NOT EXISTS notas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            inscripcion_id INTEGER NOT NULL,
            nota1 REAL,
            nota2 REAL,
            nota3 REAL,
            nota4 REAL,
            nota5 REAL,
            promedio REAL,
            estado TEXT,
            fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (inscripcion_id) REFERENCES inscripciones(id) ON DELETE CASCADE
        )
        '''
        
        tablas = [sql_profesores, sql_estudiantes, sql_materias, sql_inscripciones, sql_notas]
        
        for sql in tablas:
            self.ejecutar(sql)
        
        # Insertar profesor de prueba (si no existe)
        self.ejecutar("""
            INSERT OR IGNORE INTO profesores (usuario, password, nombre) 
            VALUES ('admin', 'admin', 'Profesor Admin')
        """)