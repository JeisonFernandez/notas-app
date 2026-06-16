from models.materia_model import MateriaModel

class MateriaController:
    """
    Controlador para manejar operaciones con materias.
    Conecta la vista con el modelo MateriaModel.
    """
    
    def __init__(self):
        self.modelo = MateriaModel()
    
    def listar_por_profesor(self, profesor_id):
        if not profesor_id:
            return []
        return self.modelo.listar_por_profesor(profesor_id)
    
    def crear(self, nombre, profesor_id):

        # Validar nombre
        if not nombre or nombre.strip() == "":
            return {'success': False, 'message': 'El nombre de la materia es obligatorio', 'id': None}
        
        if len(nombre.strip()) < 3:
            return {'success': False, 'message': 'El nombre debe tener al menos 3 caracteres', 'id': None}
        
        # Crear materia
        nuevo_id = self.modelo.crear(nombre.strip(), profesor_id)
        
        if nuevo_id:
            return {'success': True, 'message': 'Materia creada exitosamente', 'id': nuevo_id}
        else:
            return {'success': False, 'message': 'Error al crear la materia', 'id': None}
    
    def obtener_por_id(self, materia_id):
        return self.modelo.obtener_por_id(materia_id)