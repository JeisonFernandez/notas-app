import os
from kivy.lang import Builder
from kivy.metrics import dp

from kivymd.uix.screen import MDScreen
from kivymd.uix.list import MDListItem, MDListItemHeadlineText, MDListItemTrailingIcon
from kivymd.uix.dialog import MDDialog, MDDialogHeadlineText, MDDialogContentContainer, MDDialogButtonContainer
from kivymd.uix.button import MDButton, MDButtonText
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.textfield import MDTextField, MDTextFieldHintText
from kivymd.uix.label import MDLabel

from controllers.materia_controller import MateriaController

# Cargar el archivo .kv asociado explícitamente
kv_path = os.path.join(os.path.dirname(__file__), 'materias_tab.kv')
Builder.load_file(kv_path)

class MateriasTab(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        self.materia_controller = MateriaController()
        self.dialog = None
        
        # ID del profesor logueado (Por ahora quemado en 1 para pruebas)
        # En el futuro, esto se tomará de MDApp.get_running_app().profesor_actual['id']
        self.profesor_id_actual = 1 
        
    def on_enter(self, *args):
        self.cargar_materias()

    # ==========================================
    # LÓGICA DE LISTADO
    # ==========================================
    def cargar_materias(self):
        self.ids.lista_materias.clear_widgets()
        
        materias = self.materia_controller.listar_por_profesor(self.profesor_id_actual)
        
        if not materias:
            self.mostrar_mensaje("No tienes materias registradas.", (0.5, 0.5, 0.5, 1))
            return
            
        self.mostrar_mensaje("", (0,0,0,0))
        
        for mat in materias:
            # mat = (id, nombre, profesor_id)
            item = MDListItem(
                MDListItemHeadlineText(text=mat[1]),
                MDListItemTrailingIcon(
                    icon="delete",
                    on_release=lambda x, materia_id=mat[0]: self.eliminar_materia(materia_id)
                )
            )
            self.ids.lista_materias.add_widget(item)

    def mostrar_mensaje(self, texto, color):
        lbl = self.ids.lbl_mensaje
        lbl.text = texto
        lbl.text_color = color
        lbl.height = dp(30) if texto else dp(0)

    # ==========================================
    # LÓGICA DEL DIÁLOGO Y CRUD
    # ==========================================
    def abrir_dialogo_agregar(self):
        contenido = MDBoxLayout(orientation='vertical', spacing=dp(10), size_hint_y=None, height=dp(120))
        
        self.campo_nombre = MDTextField(MDTextFieldHintText(text="Nombre de la Materia"), mode="outlined")
        self.lbl_error_dlg = MDLabel(text="", theme_text_color="Custom", text_color=(1,0,0,1), size_hint_y=None, height=dp(20))
        
        contenido.add_widget(self.campo_nombre)
        contenido.add_widget(self.lbl_error_dlg)
        
        self.dialog = MDDialog(
            MDDialogHeadlineText(text="Nueva Materia"),
            MDDialogContentContainer(contenido),
            MDDialogButtonContainer(
                MDButton(MDButtonText(text="CANCELAR"), style="text", on_release=lambda x: self.dialog.dismiss()),
                MDButton(MDButtonText(text="GUARDAR"), style="elevated", on_release=self.guardar_materia)
            )
        )
        self.dialog.open()

    def guardar_materia(self, instance):
        nombre = self.campo_nombre.text.strip()
        
        if not nombre:
            self.lbl_error_dlg.text = "El nombre es obligatorio"
            return
            
        # Llamar al controlador para guardar
        resultado = self.materia_controller.crear(nombre, self.profesor_id_actual)
        
        if resultado.get('success'):
            self.dialog.dismiss()
            self.cargar_materias()
            self.mostrar_mensaje("Materia agregada con éxito.", (0, 0.7, 0, 1))
        else:
            self.lbl_error_dlg.text = resultado.get('message', 'Error al guardar')

    def eliminar_materia(self, materia_id):
        resultado = self.materia_controller.eliminar(materia_id)
        if resultado.get('success'):
            self.cargar_materias()
            self.mostrar_mensaje("Materia eliminada.", (0, 0.7, 0, 1))
        else:
            self.mostrar_mensaje(resultado.get('message', 'Error al eliminar (¿Tiene notas asociadas?)'), (1, 0, 0, 1))