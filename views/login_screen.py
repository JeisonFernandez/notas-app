from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDButton, MDButtonText
from kivymd.uix.textfield import MDTextField, MDTextFieldLeadingIcon, MDTextFieldHintText
from kivymd.uix.label import MDLabel
from kivymd.uix.card import MDCard
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.metrics import dp

from controllers.auth_controller import AuthController


class LoginScreen(MDScreen):
    """
    Pantalla de inicio de sesión.
    Hereda de MDScreen.
    """
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.auth_controller = AuthController()
        self.build_ui()
    
    def build_ui(self):
        # Layout principal responsivo
        layout_principal = MDBoxLayout(
            orientation='vertical',
            spacing=dp(20),
            padding=dp(30),
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            size_hint=(0.9, None),      # 90% del ancho en móviles
            size_hint_max_x=dp(400),    # En PC nunca pasará de 400px de ancho
            adaptive_height=True        # La altura se ajusta sola
        )
        
        # Tarjeta contenedora
        tarjeta = MDCard(
            orientation='vertical',
            padding=dp(30),
            spacing=dp(20),
            elevation=4,
            radius=[10, 10, 10, 10],
            adaptive_height=True        # Crece según el contenido
        )
        
        # Título
        titulo = MDLabel(
            text='Control de Notas',
            halign='center',
            font_style='Headline',
            role='small',
            adaptive_height=True
        )
        
        # Campo usuario
        self.campo_usuario = MDTextField(
            MDTextFieldLeadingIcon(icon='account'),
            MDTextFieldHintText(text='Usuario'),
            mode='outlined',
        )
        
        # Campo contraseña
        self.campo_password = MDTextField(
            MDTextFieldLeadingIcon(icon='lock'),
            MDTextFieldHintText(text='Contraseña'),
            mode='outlined',
            password=True,
        )
        
        # Botón login (Actualizado para KivyMD 2.0)
        self.boton_login = MDButton(
            MDButtonText(text='Iniciar Sesión'),
            style="elevated",
            theme_bg_color="Custom",
            md_bg_color=(0.1, 0.5, 0.8, 1)
        )
        self.boton_login.bind(on_release=self.on_login)
        
        # Mensaje de estado
        self.mensaje = MDLabel(
            text='',
            halign='center',
            theme_text_color='Error',
            size_hint_y=0.1
        )
        
        # Agregar todo a la tarjeta
        tarjeta.add_widget(titulo)
        tarjeta.add_widget(self.mensaje)
        tarjeta.add_widget(self.campo_usuario)
        tarjeta.add_widget(self.campo_password)
        tarjeta.add_widget(self.boton_login)
        
        # Agregar tarjeta al layout principal
        layout_principal.add_widget(tarjeta)
        
        # Agregar layout a la pantalla
        self.add_widget(layout_principal)
    
    def on_login(self, instance):
        """Maneja el evento de login"""
        usuario = self.campo_usuario.text
        password = self.campo_password.text
        
        if not usuario or not password:
            self.mensaje.text = "Ingresa usuario y/o contraseña"
            self.mensaje.theme_text_color = 'Error'
            return
        
        if self.auth_controller.login(usuario, password):
            usuario_actual = self.auth_controller.obtener_usuario_actual()
            self.mensaje.text = f"Bienvenido, {usuario_actual['nombre']}"
            self.mensaje.theme_text_color = 'Primary'
            
            # CÓDIGO DE NAVEGACIÓN
            # Obtenemos la app principal en ejecución
            from kivymd.app import MDApp
            app = MDApp.get_running_app()
            
            # Llamamos a una función de la app para cambiar de pantalla
            if hasattr(app, 'cambiar_a_main'):
                app.cambiar_a_main(usuario_actual)
        else:
            self.mensaje.text = "Usuario o contraseña incorrectos"
            self.mensaje.theme_text_color = 'Error'

    def limpiar_campos(self):
        """
        Limpia los campos de texto
        """
        self.campo_usuario.text = ''
        self.campo_password.text = '' # BUG CRÍTICO SOLUCIONADO
        self.mensaje.text = ''