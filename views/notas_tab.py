# ============================================================
# 1. IMPORTACIONES
# ============================================================

from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.datatables import MDDataTable
from kivymd.uix.dialog import MDDialog, MDDialogHeadlineText, MDDialogContentContainer, MDDialogButtonContainer
from kivymd.uix.button import MDButton, MDButtonText
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.textfield import MDTextField, MDTextFieldHintText
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.list import MDListItem
from kivymd.uix.label import MDLabel
from kivy.metrics import dp

from controllers.nota_controller import NotaController
from controllers.estudiante_controller import EstudianteController
from controllers.materia_controller import MateriaController


# ============================================================
# 2. CLASE PRINCIPAL
# ============================================================

class NotasTab(MDScreen):
    """
    Pestaña de Notas - Muestra una tabla con todas las notas registradas.
    """
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # Controladores
        self.nota_controller = NotaController()
        self.estudiante_controller = EstudianteController()
        self.materia_controller = MateriaController()
        
        # Variables de selección
        self.estudiante_id = None
        self.materia_id = None
        
        # Diálogo y menús (creados UNA VEZ en __init__)
        self.dialog = None
        self.menu_estudiantes = None
        self.menu_materias = None
        
        # Cargar datos iniciales
        self.cargar_notas()
    
    def on_enter(self, *args):
        """
        Se ejecuta cada vez que la pestaña es mostrada.
        Recarga automática de datos.
        """
        self.cargar_notas()
    
    # ============================================================
    # 3. CARGA DE DATOS
    # ============================================================
    
    def cargar_notas(self):
        """
        Carga las notas desde el controlador y actualiza la tabla.
        """
        if not hasattr(self.ids, 'tabla_notas'):
            return
        
        notas = self.nota_controller.obtener_todas()
        
        if not notas:
            self.ids.tabla_notas.row_data = []
            self.ids.lbl_mensaje.text = "No hay notas registradas"
            return
        
        filas = []
        for i, nota in enumerate(notas):
            filas.append((
                str(i + 1),
                nota[0],
                nota[1],
                f"{nota[2]:.2f}",
                nota[3],
                nota[4]
            ))
        
        self.ids.tabla_notas.row_data = filas
        self.ids.lbl_mensaje.text = ""
    
    # ============================================================
    # 4. DIÁLOGO DE AGREGAR NOTAS
    # ============================================================
    
    def abrir_dialogo_agregar(self):
        """
        Abre el diálogo para agregar una nueva nota.
        """
        self.estudiante_id = None
        self.materia_id = None
        
        contenido = self._crear_contenido_dialogo()
        
        self.dialog = MDDialog(
            MDDialogHeadlineText(text="Agregar Nota"),
            MDDialogContentContainer(contenido),
            MDDialogButtonContainer(
                MDButton(
                    MDButtonText(text="CANCELAR"),
                    style="text",
                    on_release=lambda x: self.dialog.dismiss()
                ),
                MDButton(
                    MDButtonText(text="GUARDAR"),
                    style="elevated",
                    theme_bg_color="Custom",
                    md_bg_color=(0.1, 0.5, 0.8, 1),
                    on_release=self.guardar_notas_dialogo
                ),
            )
        )
        self.dialog.open()
    
    def _crear_contenido_dialogo(self):
        """
        Crea el contenido del diálogo.
        """
        contenido = MDBoxLayout(
            orientation='vertical',
            spacing=dp(16),
            padding=dp(16),
            size_hint_y=None,
            height=dp(420)
        )
        
        # Botón estudiante
        self.btn_estudiante = MDButton(
            MDButtonText(text="Seleccionar Estudiante"),
            style="outlined",
            size_hint=(1, None),
            height=dp(48)
        )
        self.btn_estudiante.bind(on_release=self.abrir_menu_estudiantes)
        
        # Botón materia
        self.btn_materia = MDButton(
            MDButtonText(text="Seleccionar Materia"),
            style="outlined",
            size_hint=(1, None),
            height=dp(48)
        )
        self.btn_materia.bind(on_release=self.abrir_menu_materias)
        
        # Campos de notas
        self.campo_nota1 = MDTextField(
            MDTextFieldHintText(text="Nota 1 (0-20)"),
            mode="outlined"
        )
        self.campo_nota2 = MDTextField(
            MDTextFieldHintText(text="Nota 2 (0-20)"),
            mode="outlined"
        )
        self.campo_nota3 = MDTextField(
            MDTextFieldHintText(text="Nota 3 (0-20)"),
            mode="outlined"
        )
        self.campo_nota4 = MDTextField(
            MDTextFieldHintText(text="Nota 4 (0-20)"),
            mode="outlined"
        )
        self.campo_nota5 = MDTextField(
            MDTextFieldHintText(text="Nota 5 (0-20)"),
            mode="outlined"
        )
        
        # Mensaje de error (usando Custom + text_color)
        self.lbl_error_dialogo = MDLabel(
            text="",
            halign="center",
            theme_text_color="Custom",
            text_color=(0.8, 0, 0, 1),  # Rojo fijo
            font_style="Body1",
            size_hint_y=None,
            height=dp(30)
        )
        
        # Ensamblar
        contenido.add_widget(self.btn_estudiante)
        contenido.add_widget(self.btn_materia)
        contenido.add_widget(self.campo_nota1)
        contenido.add_widget(self.campo_nota2)
        contenido.add_widget(self.campo_nota3)
        contenido.add_widget(self.campo_nota4)
        contenido.add_widget(self.campo_nota5)
        contenido.add_widget(self.lbl_error_dialogo)
        
        return contenido
    
    # ============================================================
    # 5. MENÚS DESPLEGABLES
    # ============================================================
    
    def crear_menu_estudiantes(self):
        estudiantes = self.estudiante_controller.listar_todos()
        if not estudiantes:
            return None
        
        menu_items = []
        for est in estudiantes:
            texto = f"{est[1]} - {est[2]} {est[3]}"
            menu_items.append({
                "text": texto,
                "viewclass": "MDListItem",  # ← KivyMD 2.0
                "on_release": lambda x=est: self.seleccionar_estudiante(x)
            })
        
        return MDDropdownMenu(
            items=menu_items,
            width_mult=4,
        )
    
    def crear_menu_materias(self):
        app = MDApp.get_running_app()
        profesor_id = app.profesor_actual['id'] if hasattr(app, 'profesor_actual') else None
        
        if not profesor_id:
            return None
        
        materias = self.materia_controller.listar_por_profesor(profesor_id)
        if not materias:
            return None
        
        menu_items = []
        for mat in materias:
            menu_items.append({
                "text": mat[1],
                "viewclass": "MDListItem",  # ← KivyMD 2.0
                "on_release": lambda x=mat: self.seleccionar_materia(x)
            })
        
        return MDDropdownMenu(
            items=menu_items,
            width_mult=4,
        )
    
    def abrir_menu_estudiantes(self, instance):
        if not self.menu_estudiantes:
            self.menu_estudiantes = self.crear_menu_estudiantes()
        
        if self.menu_estudiantes:
            self.menu_estudiantes.caller = instance
            self.menu_estudiantes.open()
    
    def abrir_menu_materias(self, instance):
        if not self.menu_materias:
            self.menu_materias = self.crear_menu_materias()
        
        if self.menu_materias:
            self.menu_materias.caller = instance
            self.menu_materias.open()
    
    def seleccionar_estudiante(self, estudiante):
        self.estudiante_id = estudiante[0]
        for child in self.btn_estudiante.children:
            if isinstance(child, MDButtonText):
                child.text = f"{estudiante[1]} - {estudiante[2]} {estudiante[3]}"
                break
        
        if self.menu_estudiantes:
            self.menu_estudiantes.dismiss()
        self.lbl_error_dialogo.text = ""
    
    def seleccionar_materia(self, materia):
        self.materia_id = materia[0]
        for child in self.btn_materia.children:
            if isinstance(child, MDButtonText):
                child.text = materia[1]
                break
        
        if self.menu_materias:
            self.menu_materias.dismiss()
        self.lbl_error_dialogo.text = ""
    
    # ============================================================
    # 6. GUARDAR NOTAS
    # ============================================================
    
    def guardar_notas_dialogo(self, instance):
        if not self.estudiante_id or not self.materia_id:
            self.lbl_error_dialogo.text = "Selecciona un estudiante y una materia"
            return
        
        try:
            n1 = float(self.campo_nota1.text) if self.campo_nota1.text else 0
            n2 = float(self.campo_nota2.text) if self.campo_nota2.text else 0
            n3 = float(self.campo_nota3.text) if self.campo_nota3.text else 0
            n4 = float(self.campo_nota4.text) if self.campo_nota4.text else 0
            n5 = float(self.campo_nota5.text) if self.campo_nota5.text else 0
        except ValueError:
            self.lbl_error_dialogo.text = "Ingresa notas válidas (números)"
            return
        
        for nota in [n1, n2, n3, n4, n5]:
            if nota < 0 or nota > 20:
                self.lbl_error_dialogo.text = "Las notas deben estar entre 0 y 20"
                return
        
        resultado = self.nota_controller.guardar_notas(
            self.estudiante_id,
            self.materia_id,
            n1, n2, n3, n4, n5
        )
        
        if resultado['success']:
            self.dialog.dismiss()
            self.cargar_notas()
            self.ids.lbl_mensaje.text = f"Notas guardadas: Promedio {resultado['promedio']:.2f} - {resultado['estado']}"
            # CAMBIO: Usar Custom en lugar de Primary
            self.ids.lbl_mensaje.theme_text_color = "Custom"
            self.ids.lbl_mensaje.text_color = (0, 0.7, 0, 1)  # Verde éxito
        else:
            self.lbl_error_dialogo.text = f"❌ {resultado['message']}"
    
    # ============================================================
    # 7. EVENTOS DE TABLA
    # ============================================================
    
    def on_row_press(self, instance_table, instance_row):
        """
        Maneja el clic en una fila de la tabla.
        """
        dialogo_detalle = MDDialog(
            MDDialogHeadlineText(text="Detalle de Nota"),
            MDDialogContentContainer(
                MDLabel(text="No hay detalles disponibles aún.")
            ),
            MDDialogButtonContainer(
                MDButton(
                    MDButtonText(text="CERRAR"),
                    style="text",
                    on_release=lambda x: dialogo_detalle.dismiss()
                ),
            )
        )
        dialogo_detalle.open()