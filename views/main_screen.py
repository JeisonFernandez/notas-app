import os
from kivy.lang import Builder
from kivymd.uix.screen import MDScreen
from kivymd.app import MDApp
from kivy.properties import ObjectProperty

from views.notas_tab import NotasTab
from views.estudiantes_tab import EstudiantesTab
from views.materias_tab import MateriasTab

kv_path = os.path.join(os.path.dirname(__file__), 'main_screen.kv')
Builder.load_file(kv_path)

class MainScreen(MDScreen):
    profesor_actual = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
    def on_switch_tabs(self, bar, item, item_icon, item_label):
        """Maneja el evento cuando se toca un item en el MDNavigationBar."""
        
        # CORRECCIÓN: En KivyMD 2.0, item_label ya es el string directo.
        pantalla = item_label
        
        if pantalla == 'Notas':
            self.ids.tab_manager.current = 'nav_notas'
        elif pantalla == 'Estudiantes':
            self.ids.tab_manager.current = 'nav_estudiantes'
        elif pantalla == 'Materias':
            self.ids.tab_manager.current = 'nav_materias'
        elif pantalla == 'Perfil':
            self.ids.tab_manager.current = 'nav_perfil'

    def logout(self):
        """Cierra sesión y vuelve al login."""
        app = MDApp.get_running_app()
        if hasattr(app, 'profesor_actual'):
            app.profesor_actual = None
            
        self.manager.current = 'login'