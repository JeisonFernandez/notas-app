# ============================================================
# 1. IMPORTACIONES
# ============================================================

from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.card import MDCard
from kivymd.uix.textfield import MDTextField, MDTextFieldHintText
from kivymd.uix.button import MDButton, MDButtonText
from kivymd.uix.label import MDLabel
from kivymd.uix.list import MDList, MDListItem, MDListItemHeadlineText, MDListItemSupportingText
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.dialog import MDDialog, MDDialogHeadlineText, MDDialogContentContainer, MDDialogButtonContainer

from controllers.materia_controller import MateriaController


# ============================================================
# 2. CLASE PRINCIPAL
# ============================================================

class MateriasTab(MDBoxLayout):
    """
    Pestaña para gestionar materias.
    Contiene: lista de materias, botón crear materia.
    """
    
    def __init__(self, profesor_id, **kwargs):
        super().__init__(**kwargs)
        self.profesor_id = profesor_id
        self.orientation = 'vertical'
        self.spacing = 10
        self.padding = 15
        
        # Controlador
        self.materia_controller = MateriaController()
        
        # Diálogo para crear materia
        self.dialog_crear = None
        
        self.build_ui()
        self.cargar_materias()
    
    # ============================================================
    # 3. CONSTRUIR INTERFAZ
    # ============================================================
    
    def build_ui(self):
        """Construye la interfaz de la pestaña Materias"""
        
        # ============================================
        # 3.1. BARRA SUPERIOR: Título + Botón Crear
        # ============================================
        
        barra_superior = MDBoxLayout(
            orientation='horizontal',
            spacing=10,
            size_hint_y=None,
            height=50
        )
        
        titulo = MDLabel(
            text="Mis Materias",
            font_style="Title",
            role="large",
            size_hint_x=0.7
        )
        
        self.boton_crear = MDButton(
            MDButtonText(text="Crear Materia"),
            style="elevated",
            theme_bg_color="Custom",
            md_bg_color=(0.1, 0.5, 0.8, 1),
            size_hint_x=0.3
        )
        self.boton_crear.bind(on_release=self.abrir_dialogo_crear)
        
        barra_superior.add_widget(titulo)
        barra_superior.add_widget(self.boton_crear)
        
        # ============================================
        # 3.2. LISTA DE MATERIAS (con scroll)
        # ============================================
        
        self.scroll_materias = MDScrollView(
            size_hint_y=1
        )
        
        self.lista_materias = MDList()
        self.scroll_materias.add_widget(self.lista_materias)
        
        # ============================================
        # 3.3. ARMAR TODO
        # ============================================
        
        self.add_widget(barra_superior)
        self.add_widget(self.scroll_materias)
    
    # ============================================================
    # 4. CARGAR MATERIAS
    # ============================================================
    
    def cargar_materias(self):
        """Carga materias del profesor desde la BD y las muestra en la lista"""
        
        # Limpiar lista actual
        self.lista_materias.clear_widgets()
        
        # Obtener datos
        materias = self.materia_controller.listar_por_profesor(self.profesor_id)
        
        # Mostrar mensaje si no hay materias
        if not materias:
            item = MDListItem(MDListItemHeadlineText(text="No tienes materias creadas aún"))
            self.lista_materias.add_widget(item)
            return
        
        # Agregar cada materia a la lista
        for mat in materias:
            # mat = (id, nombre, fecha_creacion)
            item = MDListItem(
                MDListItemHeadlineText(text=mat[1]),
                MDListItemSupportingText(text=f"Creada: {mat[2][:10]}" if mat[2] else "Creada: recientemente")
            )
            self.lista_materias.add_widget(item)
    
    # ============================================================
    # 5. CREAR MATERIA (Diálogo)
    # ============================================================
    
    def abrir_dialogo_crear(self, instance):
        """Abre un diálogo para crear una nueva materia"""
        
        # ============================================
        # 5.1. CONTENIDO DEL DIÁLOGO
        # ============================================
        
        layout_dialogo = MDBoxLayout(
            orientation='vertical',
            spacing=10,
            padding=10,
            size_hint_y=None,
            height=150
        )
        
        self.campo_nombre_materia = MDTextField(
            MDTextFieldHintText(text="Nombre de la materia"),
            mode="outlined"
        )
        
        layout_dialogo.add_widget(self.campo_nombre_materia)
        
        # ============================================
        # 5.2. DIÁLOGO
        # ============================================
        
        self.dialog_crear = MDDialog(
            MDDialogHeadlineText(text="Crear Materia"),
            MDDialogContentContainer(layout_dialogo),
            MDDialogButtonContainer(
                MDButton(
                    MDButtonText(text="Cancelar"), 
                    style="text", 
                    on_release=lambda x: self.dialog_crear.dismiss()
                ),
                MDButton(
                    MDButtonText(text="Crear"), 
                    style="elevated", 
                    theme_bg_color="Custom", 
                    md_bg_color=(0.1, 0.5, 0.8, 1), 
                    on_release=self.guardar_materia
                )
            )
        )
        self.dialog_crear.open()
    
    def guardar_materia(self, instance):
        """Guarda la nueva materia desde el diálogo"""
        
        nombre = self.campo_nombre_materia.text
        
        # Llamar al controlador
        resultado = self.materia_controller.crear(nombre, self.profesor_id)
        
        if resultado['success']:
            # Cerrar diálogo
            self.dialog_crear.dismiss()
            
            # Limpiar campo
            self.campo_nombre_materia.text = ""
            
            # Recargar lista
            self.cargar_materias()
            
            # Mostrar mensaje de éxito
            self.mostrar_mensaje("✅ Materia creada exitosamente")
        else:
            # Mostrar error en el diálogo
            self.mostrar_mensaje_dialogo(resultado['message'])
    
    def limpiar_campos_dialogo(self):
        """Limpia los campos del diálogo"""
        self.campo_nombre_materia.text = ""
    
    def mostrar_mensaje_dialogo(self, mensaje):
        """Muestra un mensaje de error dentro del diálogo"""
        # Buscar si ya existe un label de mensaje
        for child in self.dialog_crear.content_cls.children:
            if isinstance(child, MDLabel) and child.text.startswith("❌"):
                child.text = f"❌ {mensaje}"
                return
        
        # Si no existe, crearlo
        label_error = MDLabel(
            text=f"❌ {mensaje}",
            halign="center",
            theme_text_color="Error",
            size_hint_y=None,
            height=30
        )
        self.dialog_crear.content_cls.add_widget(label_error)
    
    def mostrar_mensaje(self, mensaje):
        """Muestra un mensaje temporal"""
        print(f"📢 {mensaje}")