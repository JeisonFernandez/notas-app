from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager
from views.login_screen import LoginScreen
from views.main_screen import MainScreen
from models.db_manager import DatabaseManager

class ControlNotasApp(MDApp):
    def build(self):
        db = DatabaseManager()
        db.conectar()
        db.crear_tablas()
        db.cerrar()

        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Blue"
        
        # El ScreenManager administra las pantallas
        self.sm = ScreenManager()
        
        # Creamos y agregamos solo la pantalla de Login por ahora
        self.login_screen = LoginScreen(name='login')
        self.sm.add_widget(self.login_screen)
        
        return self.sm

    def cambiar_a_main(self, profesor_actual):
        """
        Esta función se llama desde LoginScreen cuando el login es exitoso.
        """
        # 1. Creamos la pantalla principal pasándole los datos del profesor
        self.main_screen = MainScreen(name='main', profesor_actual=profesor_actual)
        
        # 2. Le conectamos la función de cerrar sesión real
        self.main_screen.cerrar_sesion_real = self.cerrar_sesion
        
        # 3. Agregamos la pantalla al manager y cambiamos a ella
        self.sm.add_widget(self.main_screen)
        self.sm.current = 'main'

    def cerrar_sesion(self):
        """
        Esta función se llama desde MainScreen cuando se confirma el logout.
        """
        # 1. Volvemos a la pantalla de login
        self.sm.current = 'login'
        
        # 2. Limpiamos los campos del login
        self.login_screen.limpiar_campos()
        
        # 3. Borramos la pantalla principal para liberar memoria y obligar 
        # a que se recargue si entra otro profesor.
        self.sm.remove_widget(self.main_screen)
        self.main_screen = None

if __name__ == '__main__':
    ControlNotasApp().run()