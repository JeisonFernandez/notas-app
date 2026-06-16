from models.estudiante_model import EstudianteModel

class EstudianteController:
    """
    Controlador para manejar operaciones con estudiantes.
    Conecta la vista con el modelo EstudianteModel.
    """
    
    def __init__(self):
        self.modelo = EstudianteModel()
    
    def listar_todos(self):
        return self.modelo.listar_todos()
    
    def buscar(self, texto):
        if not texto or texto.strip() == "":
            return self.modelo.listar_todos()
        return self.modelo.buscar(texto)
    
    def crear(self, cedula, nombres, apellidos, pnf, trayecto, seccion):
        # Validar campos vacíos
        if not cedula or not nombres or not apellidos or not pnf or not trayecto or not seccion:
            return {'success': False, 'message': 'Todos los campos son obligatorios', 'id': None}
        
        # Validar cédula
        if len(cedula) < 6:
            return {'success': False, 'message': 'Cédula muy corta', 'id': None}
        
        # Validar trayecto (1-4)
        try:
            trayecto = int(trayecto)
            if trayecto < 1 or trayecto > 4:
                return {'success': False, 'message': 'Trayecto debe ser 1, 2, 3 o 4', 'id': None}
        except ValueError:
            return {'success': False, 'message': 'Trayecto debe ser un número', 'id': None}
        
        # Verificar si la cédula ya existe
        existente = self.modelo.obtener_por_cedula(cedula)
        if existente:
            return {'success': False, 'message': f'Ya existe un estudiante con cédula {cedula}', 'id': None}
        
        # Crear estudiante
        nuevo_id = self.modelo.crear(cedula, nombres, apellidos, pnf, trayecto, seccion)
        
        if nuevo_id:
            return {'success': True, 'message': 'Estudiante creado exitosamente', 'id': nuevo_id}
        else:
            return {'success': False, 'message': 'Error al crear el estudiante', 'id': None}
    
    def obtener_por_id(self, estudiante_id):
        return self.modelo.obtener_por_id(estudiante_id)
    
    def obtener_por_cedula(self, cedula):
        return self.modelo.obtener_por_cedula(cedula)