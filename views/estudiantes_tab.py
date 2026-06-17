import os
from kivy.lang import Builder
from kivy.metrics import dp

from kivymd.uix.screen import MDScreen
from kivymd.uix.list import MDListItem, MDListItemHeadlineText, MDListItemSupportingText, MDListItemTrailingIcon
from kivymd.uix.dialog import MDDialog, MDDialogHeadlineText, MDDialogContentContainer, MDDialogButtonContainer
from kivymd.uix.button import MDButton, MDButtonText
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.textfield import MDTextField, MDTextFieldHintText
from kivymd.uix.label import MDLabel

from controllers.estudiante_controller import EstudianteController

# Cargar el archivo .kv asociado explícitamente
kv_path = os.path.join(os.path.dirname(__file__), 'estudiantes_tab.kv')
Builder.load_file(kv_path)

class EstudiantesTab(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # El verdadero Controlador
        self.estudiante_controller = EstudianteController()
        
        self.dialog = None
        self.estudiantes_totales = [] # Caché para la búsqueda
        
    def on_enter(self, *args):
        self.cargar_estudiantes()

    # ==========================================
    # LÓGICA DE LISTADO Y BÚSQUEDA
    # ==========================================
    def cargar_estudiantes(self):
        """Obtiene los datos de la BD y refresca la lista."""
        self.estudiantes_totales = self.estudiante_controller.listar_todos()
        self.renderizar_lista(self.estudiantes_totales)

    def filtrar_estudiantes(self, texto):
        """Filtra la lista en memoria sin golpear la BD repetidamente."""
        if not texto:
            self.renderizar_lista(self.estudiantes_totales)
            return
            
        texto = texto.lower()
        filtrados = [
            est for est in self.estudiantes_totales 
            if texto in est[1].lower() or texto in est[2].lower() or texto in est[3].lower()
        ]
        self.renderizar_lista(filtrados)

    def renderizar_lista(self, datos):
        self.ids.lista_estudiantes.clear_widgets()
        
        if not datos:
            self.mostrar_mensaje("No se encontraron estudiantes.", (0.5, 0.5, 0.5, 1))
            return
            
        self.mostrar_mensaje("", (0,0,0,0))
        
        for est in datos:
            # est = (id, cedula, nombre, apellido, ...)
            item = MDListItem(
                MDListItemHeadlineText(text=f"{est[2]} {est[3]}"),
                MDListItemSupportingText(text=f"C.I: {est[1]}"),
                MDListItemTrailingIcon(
                    icon="delete",
                    on_release=lambda x, estudiante_id=est[0]: self.eliminar_estudiante(estudiante_id)
                )
            )
            self.ids.lista_estudiantes.add_widget(item)

    def mostrar_mensaje(self, texto, color):
        lbl = self.ids.lbl_mensaje
        lbl.text = texto
        lbl.text_color = color
        lbl.height = dp(30) if texto else dp(0)

    # ==========================================
    # LÓGICA DEL DIÁLOGO Y CRUD
    # ==========================================
    def abrir_dialogo_agregar(self):
        contenido = MDBoxLayout(orientation='vertical', spacing=dp(10), size_hint_y=None, height=dp(350))
        
        self.campo_cedula = MDTextField(MDTextFieldHintText(text="Cédula"), mode="outlined")
        self.campo_nombre = MDTextField(MDTextFieldHintText(text="Nombre"), mode="outlined")
        self.campo_apellido = MDTextField(MDTextFieldHintText(text="Apellido"), mode="outlined")
        self.campo_pnf = MDTextField(MDTextFieldHintText(text="PNF"), mode="outlined")
        self.campo_trayecto = MDTextField(MDTextFieldHintText(text="Trayecto"), mode="outlined")
        self.lbl_error_dlg = MDLabel(text="", theme_text_color="Custom", text_color=(1,0,0,1), size_hint_y=None, height=dp(20))
        
        contenido.add_widget(self.campo_cedula)
        contenido.add_widget(self.campo_nombre)
        contenido.add_widget(self.campo_apellido)
        contenido.add_widget(self.campo_pnf)
        contenido.add_widget(self.campo_trayecto)
        contenido.add_widget(self.lbl_error_dlg)
        
        self.dialog = MDDialog(
            MDDialogHeadlineText(text="Nuevo Estudiante"),
            MDDialogContentContainer(contenido),
            MDDialogButtonContainer(
                MDButton(MDButtonText(text="CANCELAR"), style="text", on_release=lambda x: self.dialog.dismiss()),
                MDButton(MDButtonText(text="GUARDAR"), style="elevated", on_release=self.guardar_estudiante)
            )
        )
        self.dialog.open()

    def guardar_estudiante(self, instance):
        ced = self.campo_cedula.text.strip()
        nom = self.campo_nombre.text.strip()
        ape = self.campo_apellido.text.strip()
        pnf = self.campo_pnf.text.strip()
        tray = self.campo_trayecto.text.strip()
        
        if not ced or not nom or not ape or not pnf or not tray:
            self.lbl_error_dlg.text = "Todos los campos son obligatorios"
            return
            
        # Llamada al VERDADERO controlador
        resultado = self.estudiante_controller.crear(ced, nom, ape, pnf, tray)
        
        if resultado.get('success'):
            self.dialog.dismiss()
            self.cargar_estudiantes()
            self.mostrar_mensaje("Estudiante registrado con éxito.", (0, 0.7, 0, 1))
        else:
            self.lbl_error_dlg.text = resultado.get('message', 'Error al guardar')

    def eliminar_estudiante(self, estudiante_id):
        # Aquí llamarías al método de tu controlador para eliminar
        resultado = self.estudiante_controller.eliminar(estudiante_id)
        if resultado.get('success'):
            self.cargar_estudiantes()
            self.mostrar_mensaje("Estudiante eliminado.", (0, 0.7, 0, 1))
        else:
            self.mostrar_mensaje(resultado.get('message', 'Error al eliminar'), (1, 0, 0, 1))