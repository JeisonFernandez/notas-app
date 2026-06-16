from models.db_manager import DatabaseManager

class EstudianteModel:
    
    """
    Modelo para estudiantes, listar, buscar, crear y obtener estudiantes.
    """

    def __init__(self):
        self.db = DatabaseManager()
    
    def listar_todos(self):
        self.db.conectar()
        sql = """
          SELECT id, cedula, nombres, apellidos, pnf, trayecto, seccion 
          FROM estudiantes
          ORDER BY apellidos, nombres
        """
        estudiantes = self.db.consultar(sql)
        self.db.cerrar()
        return estudiantes
    
    def buscar(self, texto):
        self.db.conectar()
        like = f"%{texto}%"
        sql = """
            SELECT id, cedula, nombres, apellidos, pnf, trayecto, seccion 
            FROM estudiantes
            WHERE cedula LIKE ? OR nombres LIKE ? OR apellidos LIKE ?
            ORDER BY apellidos, nombres
        """
        estudiantes = self.db.consultar(sql, (like, like, like))
        self.db.cerrar()
        return estudiantes
    
    def crear(self, cedula, nombres, apellidos, pnf, trayecto, seccion):
        self.db.conectar()
        sql = """
            INSERT INTO estudiantes (cedula, nombres, apellidos, pnf, trayecto, seccion)
            VALUES (?, ?, ?, ?, ?, ?)
        """
        nuevo_id = self.db.ejecutar(sql, (cedula, nombres, apellidos, pnf, trayecto, seccion))
        self.db.cerrar()
        return nuevo_id
    
    def obtener_por_id(self, estudiante_id):
        
        self.db.conectar()
        sql = """
            SELECT id, cedula, nombres, apellidos, pnf, trayecto, seccion
            FROM estudiantes
            WHERE id = ?
        """
        estudiante = self.db.consultar_uno(sql, (estudiante_id,))
        self.db.cerrar()
        return estudiante
    
    def obtener_por_cedula(self, cedula):
        
        self.db.conectar()
        sql = """
            SELECT id, cedula, nombres, apellidos, pnf, trayecto, seccion 
            FROM estudiantes 
            WHERE cedula = ?
        """
        estudiante = self.db.consultar_uno(sql, (cedula,))
        self.db.cerrar()
        return estudiante

