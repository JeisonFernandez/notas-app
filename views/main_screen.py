from kivymd.uix.screen import MDScreen
from kivymd.uix.tab import MDTabsPrimary, MDTabsItem, MDTabsItemIcon, MDTabsItemText
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.appbar import MDTopAppBar, MDTopAppBarLeadingButtonContainer, MDActionTopAppBarButton, MDTopAppBarTitle, MDTopAppBarTrailingButtonContainer
from kivymd.uix.button import MDButton, MDButtonText
from kivymd.uix.dialog import MDDialog, MDDialogHeadlineText, MDDialogContentContainer, MDDialogButtonContainer
from kivymd.uix.label import MDLabel

# NUEVO: Importaciones para gestionar el contenido de las pestañas
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.metrics import dp

# Importar los contenidos de cada pestaña
from views.notas_tab import NotasTab
from views.estudiantes_tab import EstudiantesTab
from views.materias_tab import MateriasTab


class MainScreen(MDScreen):
    """
    Pantalla principal con navegación por pestañas.
    """
    
    def __init__(self, profesor_actual=None, **kwargs):
        super().__init__(**kwargs)

        if not profesor_actual:
          raise ValueError("Se requiere un profesor logueado para acceder a MainScreen")

        self.profesor_actual = profesor_actual
        self.build_ui()
    
    def build_ui(self):
        # Layout principal (vertical)
        layout_principal = MDBoxLayout(
            orientation='vertical',
            spacing=0
        )
        
        # 1. BARRA SUPERIOR (TopAppBar)
        self.top_bar = MDTopAppBar(
            MDTopAppBarLeadingButtonContainer(
                MDActionTopAppBarButton(icon="menu", on_release=lambda x: None)
            ),
            MDTopAppBarTitle(text="Control de Notas"),
            MDTopAppBarTrailingButtonContainer(
                MDActionTopAppBarButton(icon="logout", on_release=self.cerrar_sesion)
            ),
            type="small"
        )
        
        # 2. BARRA DE PESTAÑAS (Solo los encabezados/botones)
        self.tabs = MDTabsPrimary(
            MDTabsItem(
                MDTabsItemIcon(icon="notebook"),
                MDTabsItemText(text="Notas"),
                on_release=lambda x: self.cambiar_pestana("Notas")
            ),
            MDTabsItem(
                MDTabsItemIcon(icon="account-group"),
                MDTabsItemText(text="Estudiantes"),
                on_release=lambda x: self.cambiar_pestana("Estudiantes")
            ),
            MDTabsItem(
                MDTabsItemIcon(icon="book-open-variant"),
                MDTabsItemText(text="Materias"),
                on_release=lambda x: self.cambiar_pestana("Materias")
            )
        )
        
        # 3. CONTENEDOR DE CONTENIDO (ScreenManager)
        self.sm_contenido = ScreenManager()
        
        # Envolver la vista Notas en una pantalla
        pantalla_notas = Screen(name="Notas")
        self.tab_notas = NotasTab(profesor_id=self.profesor_actual['id'])
        pantalla_notas.add_widget(self.tab_notas)
        
        # Envolver la vista Estudiantes en una pantalla
        pantalla_estudiantes = Screen(name="Estudiantes")
        self.tab_estudiantes = EstudiantesTab()
        pantalla_estudiantes.add_widget(self.tab_estudiantes)
        
        # Envolver la vista Materias en una pantalla
        pantalla_materias = Screen(name="Materias")
        self.tab_materias = MateriasTab(profesor_id=self.profesor_actual['id'])
        pantalla_materias.add_widget(self.tab_materias)
        
        # Agregar las pantallas al manager de contenido
        self.sm_contenido.add_widget(pantalla_notas)
        self.sm_contenido.add_widget(pantalla_estudiantes)
        self.sm_contenido.add_widget(pantalla_materias)
        
        # 4. ARMAR TODO EN ORDEN VERTICAL
        layout_principal.add_widget(self.top_bar)
        layout_principal.add_widget(self.tabs)
        layout_principal.add_widget(self.sm_contenido) # Agregamos el contenido real
        
        self.add_widget(layout_principal)
        
    def cambiar_pestana(self, nombre_pantalla):
        """Cambia el contenido del ScreenManager al tocar una pestaña"""
        self.sm_contenido.current = nombre_pantalla
    
    def cerrar_sesion(self, instance):
        self.dialog = MDDialog(
            MDDialogHeadlineText(text="Cerrar Sesión"),
            MDDialogContentContainer(
                MDLabel(text="¿Estás seguro de que quieres cerrar sesión?")
            ),
            MDDialogButtonContainer(
                MDButton(
                    MDButtonText(text="Cancelar"), 
                    style="text", 
                    on_release=lambda x: self.dialog.dismiss()
                ),
                MDButton(
                    MDButtonText(text="Sí, cerrar"), 
                    style="elevated", 
                    theme_bg_color="Custom", 
                    md_bg_color=(0.8, 0.2, 0.2, 1), 
                    on_release=lambda x: self._confirmar_logout()
                )
            )
        )
        self.dialog.open()
    
    def _confirmar_logout(self):
        self.dialog.dismiss()
        self.cerrar_sesion_real()
    
    def cerrar_sesion_real(self):
        pass