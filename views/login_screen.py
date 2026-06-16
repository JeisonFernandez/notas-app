from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.label import MDLabel
from kivymd.uix.card import MDCard
from kivymd.uix.boxlayout import MDBoxLayout

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
        """Construye la interfaz de login"""
        
        # Layout principal (vertical)
        layout_principal = MDBoxLayout(
            orientation='vertical',
            spacing=20,
            padding=30,
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            size_hint=(0.8, 0.7)
        )
        
        # Tarjeta contenedora
        tarjeta = MDCard(
            orientation='vertical',
            padding=20,
            spacing=15,
            size_hint=(1, 1),
            elevation=4,
            radius=[10, 10, 10, 10]
        )
        
        # Título
        titulo = MDLabel(
            text='Control de Notas',
            halign='center',
            font_style='H4',
            size_hint_y=0.2
        )
        
        # Campo usuario
        self.campo_usuario = MDTextField(
            hint_text='Usuario',
            mode='rectangle',
            icon_left='account',
            size_hint_y=0.15
        )
        
        # Campo contraseña
        self.campo_password = MDTextField(
            hint_text='Contraseña',
            mode='rectangle',
            password=True,
            icon_left='lock',
            size_hint_y=0.15
        )
        
        # Botón login
        self.boton_login = MDRaisedButton(
            text='Iniciar Sesión',
            size_hint_y=0.15,
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
        else:
            self.mensaje.text = "Usuario o contraseña incorrectos"
            self.mensaje.theme_text_color = 'Error'

        
        
    def limpiar_campos(self):
        """
        Limpia los campos de texto
        """
        self.campo_usuario.text = ''
        self.campo_contraseña.text = ''
        self.mensaje.text = ''


