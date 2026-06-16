from models.profesor_model import ProfesorModel

class AuthController:

    def __init__(self):
        self.profesor_model = ProfesorModel()
        self.profesor_actual = None

    def login(self, usuario, password):
        profesor = self.profesor_model.verificar_login(usuario, password)

        if profesor:
            self.profesor_actual = {
                'id': profesor[0],
                'usuario': profesor[1],
                'nombre': profesor[2]
            }
            return True
        return False
    
    def logout(self):
        self.profesor_actual = None

    def obtener_usuario_actual(self):
        return self.profesor_actual
    
    def esta_logueado(self):
        return self.profesor_actual is not None
    
    def registrar_profesores(self, usuario, password, nombre):
        return self.profesor_model.crear(usuario, password, nombre)