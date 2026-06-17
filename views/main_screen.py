from kivymd.uix.screen import MDScreen
from kivymd.app import MDApp
from views.notas_screen import NotasScreen
from views.estudiantes_screen import EstudiantesScreen
from views.materias_screen import MateriasScreen

class MainScreen(MDScreen):
    def __init__(self, profesor_actual, **kwargs):
        super().__init__(**kwargs)
        self.profesor_actual = profesor_actual
        self.build_ui()

    def build_ui(self):
        # Crear las pantallas de cada pestaña
        self.tab_notas = NotasScreen(name="Notas")
        self.tab_estudiantes = EstudiantesScreen(name="Estudiantes")
        self.tab_materias = MateriasScreen(name="Materias")

        # Agregar al ScreenManager
        sm = self.ids.sm_contenido
        sm.add_widget(self.tab_notas)
        sm.add_widget(self.tab_estudiantes)
        sm.add_widget(self.tab_materias)

    def cambiar_pestana(self, nombre):
        self.ids.sm_contenido.current = nombre

    def cerrar_sesion(self):
        # Mostrar diálogo y luego notificar a la app
        app = MDApp.get_running_app()
        if hasattr(app, 'cerrar_sesion'):
            app.cerrar_sesion()