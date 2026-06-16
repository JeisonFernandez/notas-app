# ============================================================
# 1. IMPORTACIONES
# ============================================================

from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.card import MDCard
from kivymd.uix.textfield import MDTextField, MDTextFieldLeadingIcon, MDTextFieldHintText
from kivymd.uix.button import MDButton, MDButtonText
from kivymd.uix.label import MDLabel
from kivymd.uix.list import MDList, MDListItem, MDListItemHeadlineText, MDListItemSupportingText
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.dialog import MDDialog, MDDialogHeadlineText, MDDialogContentContainer, MDDialogButtonContainer

from controllers.estudiante_controller import EstudianteController


# ============================================================
# 2. CLASE PRINCIPAL
# ============================================================

class EstudiantesTab(MDBoxLayout):
    """
    Pestaña para gestionar estudiantes.
    Contiene: lista de estudiantes, campo de búsqueda, botón agregar.
    """
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.spacing = 10
        self.padding = 15
        
        # Controlador
        self.estudiante_controller = EstudianteController()
        
        # Diálogo para agregar estudiante
        self.dialog_agregar = None
        
        self.build_ui()
        self.cargar_estudiantes()
    
    # ============================================================
    # 3. CONSTRUIR INTERFAZ
    # ============================================================
    
    def build_ui(self):
        """Construye la interfaz de la pestaña Estudiantes"""
        
        # ============================================
        # 3.1. BARRA DE BÚSQUEDA Y AGREGAR
        # ============================================
        
        barra_superior = MDBoxLayout(
            orientation='horizontal',
            spacing=10,
            size_hint_y=None,
            height=60
        )
        
        # Campo de búsqueda
        self.campo_buscar = MDTextField(
            MDTextFieldLeadingIcon(icon="magnify"),
            MDTextFieldHintText(text="Buscar por nombre, apellido o cédula..."),
            mode="outlined",
            size_hint_x=0.8
        )
        self.campo_buscar.bind(on_text_validate=self.buscar_estudiantes)
        
        # Botón Agregar
        self.boton_agregar = MDButton(
            MDButtonText(text="Agregar"),
            style="elevated",
            theme_bg_color="Custom",
            md_bg_color=(0.1, 0.6, 0.2, 1),
            size_hint_x=0.2
        )
        self.boton_agregar.bind(on_release=self.abrir_dialogo_agregar)
        
        barra_superior.add_widget(self.campo_buscar)
        barra_superior.add_widget(self.boton_agregar)
        
        # ============================================
        # 3.2. LISTA DE ESTUDIANTES (con scroll)
        # ============================================
        
        self.scroll_estudiantes = MDScrollView(
            size_hint_y=1
        )
        
        self.lista_estudiantes = MDList()
        self.scroll_estudiantes.add_widget(self.lista_estudiantes)
        
        # ============================================
        # 3.3. ARMAR TODO
        # ============================================
        
        self.add_widget(barra_superior)
        self.add_widget(self.scroll_estudiantes)
    
    # ============================================================
    # 4. CARGAR ESTUDIANTES
    # ============================================================
    
    def cargar_estudiantes(self, texto_busqueda=None):
        """
        Carga estudiantes desde la BD y los muestra en la lista.
        
        Args:
            texto_busqueda (str): Texto para buscar (opcional)
        """
        # Limpiar lista actual
        self.lista_estudiantes.clear_widgets()
        
        # Obtener datos
        if texto_busqueda and texto_busqueda.strip():
            estudiantes = self.estudiante_controller.buscar(texto_busqueda)
        else:
            estudiantes = self.estudiante_controller.listar_todos()
        
        # Mostrar mensaje si no hay estudiantes
        if not estudiantes:
            item = MDListItem(MDListItemHeadlineText(text="No hay estudiantes registrados"))
            self.lista_estudiantes.add_widget(item)
            return
        
        # Agregar cada estudiante a la lista
        for est in estudiantes:
            # est = (id, cedula, nombres, apellidos, pnf, trayecto, seccion)
            nombre_completo = f"{est[2]} {est[3]}"
            info = f"{est[1]} | {est[4]} | {est[5]}° | Sección {est[6]}"
            
            item = MDListItem(
                MDListItemHeadlineText(text=nombre_completo),
                MDListItemSupportingText(text=info)
            )
            self.lista_estudiantes.add_widget(item)
    
    def buscar_estudiantes(self, instance):
        """Ejecuta búsqueda cuando se presiona Enter en el campo de búsqueda"""
        texto = self.campo_buscar.text
        self.cargar_estudiantes(texto)
    
    # ============================================================
    # 5. AGREGAR ESTUDIANTE (Diálogo)
    # ============================================================
    
    def abrir_dialogo_agregar(self, instance):
        """Abre un diálogo para agregar un nuevo estudiante"""
        
        # ============================================
        # 5.1. CONTENIDO DEL DIÁLOGO
        # ============================================
        
        layout_dialogo = MDBoxLayout(
            orientation='vertical',
            spacing=10,
            padding=10,
            size_hint_y=None,
            height=400
        )
        
        self.campo_cedula = MDTextField(
            MDTextFieldHintText(text="Cédula (ej: V-12345678)"),
            mode="outlined"
        )
        self.campo_nombres = MDTextField(
            MDTextFieldHintText(text="Nombres"),
            mode="outlined"
        )
        self.campo_apellidos = MDTextField(
            MDTextFieldHintText(text="Apellidos"),
            mode="outlined"
        )
        self.campo_pnf = MDTextField(
            MDTextFieldHintText(text="PNF (ej: Informática)"),
            mode="outlined"
        )
        self.campo_trayecto = MDTextField(
            MDTextFieldHintText(text="Trayecto (1-4)"),
            mode="outlined",
            input_filter="int"
        )
        self.campo_seccion = MDTextField(
            MDTextFieldHintText(text="Sección (ej: A, B, Única)"),
            mode="outlined"
        )
        
        layout_dialogo.add_widget(self.campo_cedula)
        layout_dialogo.add_widget(self.campo_nombres)
        layout_dialogo.add_widget(self.campo_apellidos)
        layout_dialogo.add_widget(self.campo_pnf)
        layout_dialogo.add_widget(self.campo_trayecto)
        layout_dialogo.add_widget(self.campo_seccion)
        
        # ============================================
        # 5.2. DIÁLOGO
        # ============================================
        
        self.dialog_agregar = MDDialog(
            MDDialogHeadlineText(text="Agregar Estudiante"),
            MDDialogContentContainer(layout_dialogo),
            MDDialogButtonContainer(
                MDButton(
                    MDButtonText(text="Cancelar"), 
                    style="text", 
                    on_release=lambda x: self.dialog_agregar.dismiss()
                ),
                MDButton(
                    MDButtonText(text="Guardar"), 
                    style="elevated", 
                    theme_bg_color="Custom", 
                    md_bg_color=(0.1, 0.6, 0.2, 1), 
                    on_release=self.guardar_estudiante
                )
            )
        )
        self.dialog_agregar.open()
    
    def guardar_estudiante(self, instance):
        """Guarda el nuevo estudiante desde el diálogo"""
        
        # Obtener datos del diálogo
        cedula = self.campo_cedula.text
        nombres = self.campo_nombres.text
        apellidos = self.campo_apellidos.text
        pnf = self.campo_pnf.text
        trayecto = self.campo_trayecto.text
        seccion = self.campo_seccion.text
        
        # Llamar al controlador
        resultado = self.estudiante_controller.crear(
            cedula, nombres, apellidos, pnf, trayecto, seccion
        )
        
        if resultado['success']:
            # Cerrar diálogo
            self.dialog_agregar.dismiss()
            
            # Limpiar campos (para la próxima vez que se abra)
            self.limpiar_campos_dialogo()
            
            # Recargar lista
            self.cargar_estudiantes()
            
            # Mostrar mensaje de éxito (opcional, podemos usar un snackbar)
            self.mostrar_mensaje("✅ Estudiante creado exitosamente")
        else:
            # Mostrar error en el diálogo
            self.mostrar_mensaje_dialogo(resultado['message'])
    
    def limpiar_campos_dialogo(self):
        """Limpia los campos del diálogo"""
        self.campo_cedula.text = ""
        self.campo_nombres.text = ""
        self.campo_apellidos.text = ""
        self.campo_pnf.text = ""
        self.campo_trayecto.text = ""
        self.campo_seccion.text = ""
    
    def mostrar_mensaje_dialogo(self, mensaje):
        """Muestra un mensaje de error dentro del diálogo"""
        # Buscar si ya existe un label de mensaje
        for child in self.dialog_agregar.content_cls.children:
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
        self.dialog_agregar.content_cls.add_widget(label_error)
    
    def mostrar_mensaje(self, mensaje):
        """
        Muestra un mensaje temporal usando un snackbar.
        """
        print(f"📢 {mensaje}")