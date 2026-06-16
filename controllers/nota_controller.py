from models.nota_model import NotaModel

class NotaController:
    """
    Controlador para manejar operaciones con notas.
    Conecta la vista con el modelo NotaModel.
    """
    
    def __init__(self):
        self.modelo = NotaModel()
    
    def guardar_notas(self, estudiante_id, materia_id, nota1, nota2, nota3, nota4, nota5, periodo="2026-1"):
    
        # Validar que estudiante y materia estan seleccionados
        if not estudiante_id or not materia_id:
            return {
                'success': False,
                'message': 'Debe seleccionar un estudiante y una materia',
                'promedio': None,
                'estado': None,
                'id': None
            }
        
        # Validar que todas las notas sean números
        try:
            notas = [float(nota1), float(nota2), float(nota3), float(nota4), float(nota5)]
        except ValueError:
            return {
                'success': False,
                'message': 'Todas las notas deben ser números válidos',
                'promedio': None,
                'estado': None,
                'id': None
            }
        
        # Validar rango de notas (0-20)
        for nota in notas:
            if nota < 0 or nota > 20:
                return {
                    'success': False,
                    'message': f'Las notas deben estar entre 0 y 20 (nota inválida: {nota})',
                    'promedio': None,
                    'estado': None,
                    'id': None
                }
        
        # Obtener o crear inscripción
        inscripcion_id = self.modelo.obtener_o_crear_inscripcion(
            estudiante_id, materia_id, periodo
        )
        
        if not inscripcion_id:
            return {
                'success': False,
                'message': 'Error al crear la inscripción',
                'promedio': None,
                'estado': None,
                'id': None
            }
        
        # Guardar notas
        nota_id = self.modelo.guardar_notas(
            inscripcion_id, notas[0], notas[1], notas[2], notas[3], notas[4]
        )
        
        if nota_id:
            # Calcular promedio y estado para mostrar
            promedio = sum(notas) / 5
            estado = "APRUEBA" if promedio >= 12.0 else "DESAPRUEBA"
            
            return {
                'success': True,
                'message': 'Notas guardadas exitosamente',
                'promedio': promedio,
                'estado': estado,
                'id': nota_id
            }
        else:
            return {
                'success': False,
                'message': 'Error al guardar las notas',
                'promedio': None,
                'estado': None,
                'id': None
            }
    
    def obtener_historial_estudiante(self, estudiante_id, limite=10):
        return self.modelo.obtener_historial_por_estudiante(estudiante_id, limite)
    
    def obtener_historial_estudiante_materia(self, estudiante_id, materia_id, limite=10):
        return self.modelo.obtener_historial_por_estudiante_materia(estudiante_id, materia_id, limite)
    
    def obtener_ultimas_notas(self, profesor_id, limite=10):
        return self.modelo.obtener_ultimas_notas(profesor_id, limite)