from models.db_manager import DatabaseManager

class ProfesorModel:
  
    def __init__(self):
        self.db = DatabaseManager()

    def verificar_login(self, usuario, password):
        """
        Verifica credenciales de login.
        Retorna (id, usuario, nombre) si existe, None si no.
        """
        self.db.conectar()
        sql = "SELECT id, usuario, nombre FROM profesores WHERE usuario = ? AND password = ?"
        profesor = self.db.consultar_uno(sql, (usuario, password))
        self.db.cerrar()
        return profesor
    
    def obtener_todos(self):
        """ 
        Obtener lista de todos los profesores
        """
        self.db.conectar()
        sql = "SELECT * FROM profesores ORDER BY nombre"
        profesores = self.db.consultar(sql)
        self.db.cerrar()
        return profesores
    
    def obtener_por_id(self, profesor_id):
        """
        Obtener profesor por id
        """
        self.db.conectar()
        sql = "SELECT * FROM profesores WHERE id = ?"
        profesor = self.db.consultar_uno(sql, (profesor_id,))
        self.db.cerrar()
        return profesor
    
    def crear(self, usuario, password, nombre):
        """
        Crear un profesor
        """
        self.db.conectar()
        sql = "INSERT INTO profesores (usuario, password, nombre) VALUES (?,?,?)"
        nuevo_id = self.db.ejecutar(sql, (usuario, password, nombre))
        self.db.cerrar()
        return nuevo_id
    
    def actualizar_password(self, profesor_id, nueva_password):
        """
        Actualizar la contraseña del profesor
        """
        self.db.conectar()
        sql = "UPDATE profesores SET password = ? WHERE id = ?"
        resultado = self.db.ejecutar(sql, (nueva_password, profesor_id))
        self.db.cerrar()
        return resultado
    
    def eliminar(self, profesor_id):
        """
        Elimina un profesor por su ID
        """
        self.db.conectar()
        sql = "DELETE FROM profesores WHERE id = ?"
        resultado = self.db.ejecutar(sql, (profesor_id,))
        self.db.cerrar()
        return resultado is not None

