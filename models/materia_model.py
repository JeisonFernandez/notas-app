from models.db_manager import DatabaseManager

class MateriaModel:
    """
    Modelo para manejar operaciones con la tabla 'materias'.
    Cada materia pertenece a un profesor.
    """
    
    def __init__(self):
        self.db = DatabaseManager()
    
    def listar_por_profesor(self, profesor_id):
        self.db.conectar()
        sql = """
            SELECT id, nombre, fecha_creacion 
            FROM materias 
            WHERE profesor_id = ?
            ORDER BY nombre
        """
        materias = self.db.consultar(sql, (profesor_id,))
        self.db.cerrar()
        return materias
    
    def crear(self, nombre, profesor_id):
        self.db.conectar()
        sql = "INSERT INTO materias (nombre, profesor_id) VALUES (?, ?)"
        nuevo_id = self.db.ejecutar(sql, (nombre, profesor_id))
        self.db.cerrar()
        return nuevo_id
    
    def obtener_por_id(self, materia_id):
        self.db.conectar()
        sql = "SELECT id, nombre, profesor_id, fecha_creacion FROM materias WHERE id = ?"
        materia = self.db.consultar_uno(sql, (materia_id,))
        self.db.cerrar()
        return materia
    