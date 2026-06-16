from models.db_manager import DatabaseManager

class NotaModel:
    """
    Modelo para manejar operaciones con la tabla 'notas'.
    También maneja la tabla 'inscripciones' para relacionar estudiantes con materias.
    """
    
    def __init__(self):
        self.db = DatabaseManager()
    

    # MÉTODOS PARA INSCRIPCIONES
    def obtener_o_crear_inscripcion(self, estudiante_id, materia_id, periodo="2026-1"):
        """
        Busca una inscripción existente. Si no existe, la crea.
        
        Args:
            estudiante_id (int): ID del estudiante
            materia_id (int): ID de la materia
            periodo (str): Periodo académico (ej: "2026-1")
            
        Returns:
            int: ID de la inscripción (existente o nueva)
        """


        self.db.conectar()
        
        # Buscar si ya existe inscripción
        sql_buscar = """
            SELECT id FROM inscripciones 
            WHERE estudiante_id = ? AND materia_id = ? AND periodo = ?
        """
        inscripcion = self.db.consultar_uno(sql_buscar, (estudiante_id, materia_id, periodo))
        
        if inscripcion:
            inscripcion_id = inscripcion[0]
        else:
            sql_crear = """
                INSERT INTO inscripciones (estudiante_id, materia_id, periodo)
                VALUES (?, ?, ?)
            """
            inscripcion_id = self.db.ejecutar(sql_crear, (estudiante_id, materia_id, periodo))
        
        self.db.cerrar()
        return inscripcion_id
    

    # MÉTODOS PARA NOTAS
    def guardar_notas(self, inscripcion_id, nota1, nota2, nota3, nota4, nota5):
        """
        Guarda 5 notas para una inscripción. Calcula promedio y estado automáticamente.
        Notas en sistema venezolano: 0-20, aprueba con 12 o más.
        
        Args:
            inscripcion_id (int): ID de la inscripción
            nota1-5 (float): Notas (0-20)
            
        Returns:
            int: ID de la nota guardada, o None si falla
        """


        # Validar: notas entre 0 y 20
        notas = [nota1, nota2, nota3, nota4, nota5]
        for nota in notas:
            if nota < 0 or nota > 20:
                print(f"Error: Nota {nota} fuera de rango (0-20)")
                return None
        
        # Calcular promedio
        promedio = sum(notas) / 5
        
        # Determinar estado 
        estado = "APRUEBA" if promedio >= 12.0 else "DESAPRUEBA"
        
        self.db.conectar()
        sql = """
            INSERT INTO notas (
                inscripcion_id, nota1, nota2, nota3, nota4, nota5, promedio, estado
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """
        nota_id = self.db.ejecutar(sql, (
            inscripcion_id, nota1, nota2, nota3, nota4, nota5, promedio, estado
        ))
        self.db.cerrar()
        return nota_id
    
    def obtener_historial_por_estudiante(self, estudiante_id, limite=10):
        """
        Obtiene el historial de notas de un estudiante (todas las materias).
        
        Args:
            estudiante_id (int): ID del estudiante
            limite (int): Máximo de registros a retornar
            
        Returns:
            list: Lista de tuplas (materia, nota1-5, promedio, estado, fecha)
        """


        self.db.conectar()
        sql = """
            SELECT 
                m.nombre AS materia,
                n.nota1, n.nota2, n.nota3, n.nota4, n.nota5,
                n.promedio, n.estado, n.fecha_registro
            FROM notas n
            JOIN inscripciones i ON n.inscripcion_id = i.id
            JOIN materias m ON i.materia_id = m.id
            WHERE i.estudiante_id = ?
            ORDER BY n.fecha_registro DESC
            LIMIT ?
        """
        historial = self.db.consultar(sql, (estudiante_id, limite))
        self.db.cerrar()
        return historial
    
    def obtener_historial_por_estudiante_materia(self, estudiante_id, materia_id, limite=10):
        """
        Obtiene el historial de notas de un estudiante en una materia específica.
        
        Args:
            estudiante_id (int): ID del estudiante
            materia_id (int): ID de la materia
            limite (int): Máximo de registros a retornar
            
        Returns:
            list: Lista de tuplas (nota1-5, promedio, estado, fecha)
        """

        
        self.db.conectar()
        sql = """
            SELECT 
                n.nota1, n.nota2, n.nota3, n.nota4, n.nota5,
                n.promedio, n.estado, n.fecha_registro
            FROM notas n
            JOIN inscripciones i ON n.inscripcion_id = i.id
            WHERE i.estudiante_id = ? AND i.materia_id = ?
            ORDER BY n.fecha_registro DESC
            LIMIT ?
        """
        historial = self.db.consultar(sql, (estudiante_id, materia_id, limite))
        self.db.cerrar()
        return historial
    
    def obtener_ultimas_notas(self, profesor_id, limite=10):
        """
        Obtiene las últimas notas guardadas por un profesor.
        
        Args:
            profesor_id (int): ID del profesor
            limite (int): Máximo de registros
            
        Returns:
            list: Lista de tuplas (estudiante, materia, promedio, estado, fecha)
        """

        
        self.db.conectar()
        sql = """
            SELECT 
                e.nombres || ' ' || e.apellidos AS estudiante,
                m.nombre AS materia,
                n.promedio, n.estado, n.fecha_registro
            FROM notas n
            JOIN inscripciones i ON n.inscripcion_id = i.id
            JOIN estudiantes e ON i.estudiante_id = e.id
            JOIN materias m ON i.materia_id = m.id
            WHERE m.profesor_id = ?
            ORDER BY n.fecha_registro DESC
            LIMIT ?
        """
        notas = self.db.consultar(sql, (profesor_id, limite))
        self.db.cerrar()
        return notas