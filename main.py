from kivymd.app import MDApp
from kivymd.uix.screenmanager import MDScreenManager

from views.login_screen import LoginScreen
from views.main_screen import MainScreen
from models.db_manager import DatabaseManager


class ControlNotasApp(MDApp):
    """
    Aplicación principal.
    Maneja la navegación entre pantallas y la sesión del profesor.
    """
    
    def build(self):
        """Construye la aplicación"""
        
        # ============================================
        # 1. INICIALIZAR BASE DE DATOS
        # ============================================
        
        db = DatabaseManager()
        db.conectar()
        db.crear_tablas()
        db.cerrar()
        
        # ============================================
        # 2. CONFIGURAR TEMA
        # ============================================
        
        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.theme_style = "Dark"
        
        # ============================================
        # 3. CREAR MANEJADOR DE PANTALLAS
        # ============================================
        
        self.screen_manager = MDScreenManager()
        
        # ============================================
        # 4. CREAR PANTALLAS
        # ============================================
        
        # Pantalla de login
        self.login_screen = LoginScreen(name='login')
        self.screen_manager.add_widget(self.login_screen)
        
        # Pantalla principal (sin profesor aún)
        self.main_screen = None
        
        # ============================================
        # 5. CONECTAR EL LOGIN CON LA APP
        # ============================================
        
        # Sobrescribir el método de login de la vista
        self.login_screen.on_login_real = self.procesar_login
        
        return self.screen_manager
    
    # ============================================================
    # 6. PROCESAR LOGIN
    # ============================================================
    
    def procesar_login(self, usuario, password):
        """
        Procesa el login desde la pantalla de login.
        Si es exitoso, muestra la pantalla principal.
        
        Args:
            usuario (str): Nombre de usuario
            password (str): Contraseña
            
        Returns:
            bool: True si login exitoso, False si falla
        """
        from controllers.auth_controller import AuthController
        
        auth = AuthController()
        
        if auth.login(usuario, password):
            # Obtener profesor logueado
            profesor = auth.obtener_usuario_actual()
            
            # Crear pantalla principal con el profesor
            self.main_screen = MainScreen(
                profesor_actual=profesor,
                name='main'
            )
            
            # Conectar el logout de la pantalla principal
            self.main_screen.cerrar_sesion_real = self.cerrar_sesion
            
            # Agregar y cambiar a la pantalla principal
            self.screen_manager.add_widget(self.main_screen)
            self.screen_manager.current = 'main'
            
            return True
        else:
            return False
    
    # ============================================================
    # 7. CERRAR SESIÓN
    # ============================================================
    
    def cerrar_sesion(self):
        """Cierra sesión y vuelve a la pantalla de login"""
        # Remover pantalla principal
        if self.main_screen:
            self.screen_manager.remove_widget(self.main_screen)
            self.main_screen = None
        
        # Ir a la pantalla de login
        self.screen_manager.current = 'login'
        
        # Limpiar campos de login
        self.login_screen.limpiar_campos()


if __name__ == '__main__':
    ControlNotasApp().run()