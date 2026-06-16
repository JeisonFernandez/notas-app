from kivymd.uix.screen import MDScreen
from kivymd.uix.tab import MDTabsPrimary, MDTabsItem, MDTabsItemIcon, MDTabsItemText
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.topappbar import MDTopAppBar
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.label import MDLabel

# Importar los contenidos de cada pestaña
from views.notas_tab import NotasTab
from views.estudiantes_tab import EstudiantesTab
from views.materias_tab import MateriasTab


class MainScreen(MDScreen):
    """
    Pantalla principal con navegación por pestañas (MDTabs).
    Contiene 3 pestañas: Notas, Estudiantes, Materias.
    """
    
    def __init__(self, profesor_actual=None, **kwargs):
        """
        Constructor. Recibe el profesor logueado.
        
        Args:
            profesor_actual (dict): Datos del profesor logueado
                                   {'id': 1, 'usuario': 'admin', 'nombre': '...'}
        """

        super().__init__(**kwargs)

        # Validar que el profesor existe
        if not profesor_actual:
          raise ValueError("Se requiere un profesor logueado para acceder a MainScreen")

        self.profesor_actual = profesor_actual
        self.build_ui()
    
    def build_ui(self):
        """Construye la interfaz"""
        
        # Layout principal (vertical)
        layout_principal = MDBoxLayout(
            orientation='vertical',
            spacing=0
        )
        
  
        # 1. BARRA SUPERIOR (TopAppBar)
        self.top_bar = MDTopAppBar(
            title="Control de Notas",
            elevation=2,
            left_action_items=[["menu", lambda x: None]],  # Menú (placeholder)
            right_action_items=[["logout", self.cerrar_sesion]]
        )
        
        """PESTAÑAS"""
        
        # Crear las 3 pestañas
        self.tab_notas = NotasTab(profesor_id=self.profesor_actual['id'])
        self.tab_estudiantes = EstudiantesTab()
        self.tab_materias = MateriasTab(profesor_id=self.profesor_actual['id'])
        

        # 3. CONTENEDOR DE PESTAÑAS (MDTabsPrimary)
        self.tabs = MDTabsPrimary(
            # Pestaña 1: Notas
            MDTabsItem(
                MDTabsItemIcon(icon="notebook"),
                MDTabsItemText(text="Notas"),
                # El contenido (widget) de la pestaña
                self.tab_notas
            ),
            # Pestaña 2: Estudiantes
            MDTabsItem(
                MDTabsItemIcon(icon="account-group"),
                MDTabsItemText(text="Estudiantes"),
                self.tab_estudiantes
            ),
            # Pestaña 3: Materias
            MDTabsItem(
                MDTabsItemIcon(icon="book-open-variant"),
                MDTabsItemText(text="Materias"),
                self.tab_materias
            ),
            # Propiedades del contenedor
            pos_hint={"top": 1},
            size_hint_y=0.95,
            type="carousel",  # Deslizamiento entre pestañas
        )
        
        # 4. ARMAR TODO
        layout_principal.add_widget(self.top_bar)
        layout_principal.add_widget(self.tabs)
        
        self.add_widget(layout_principal)
    
    def cerrar_sesion(self, instance):
        """
        Cierra la sesión y vuelve a la pantalla de login.
        Este método será llamado desde la app principal.
        """
        # La app principal manejará el logout
        # Por ahora solo notificamos
        from kivymd.uix.dialog import MDDialog
        from kivymd.uix.button import MDRaisedButton
        
        dialog = MDDialog(
            title="Cerrar Sesión",
            text="¿Estás seguro de que quieres cerrar sesión?",
            buttons=[
                MDRaisedButton(
                    text="Cancelar",
                    on_release=lambda x: dialog.dismiss()
                ),
                MDRaisedButton(
                    text="Sí, cerrar",
                    md_bg_color=(0.8, 0.2, 0.2, 1),
                    on_release=lambda x: self._confirmar_logout(dialog)
                )
            ]
        )
        dialog.open()
    
    def _confirmar_logout(self, dialog):
        """Confirma el cierre de sesión y notifica a la app"""
        dialog.dismiss()
        # La app principal manejará el logout
        # Llamamos a un método que la app principal debe implementar
        self.cerrar_sesion_real()
    
    def cerrar_sesion_real(self):
        """
        Este método será sobrescrito por la app principal.
        La app principal se encarga de cambiar a la pantalla de login.
        """
        # La app principal reemplazará este método
        pass