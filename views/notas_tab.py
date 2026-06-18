import os
from kivy.lang import Builder
from kivy.metrics import dp
from kivy.properties import StringProperty
from kivy.clock import Clock

from kivymd.uix.screen import MDScreen
from kivymd.uix.list import MDListItem, MDListItemHeadlineText, MDListItemSupportingText, MDListItemTertiaryText, MDListItemTrailingIcon
from kivymd.uix.dialog import MDDialog, MDDialogHeadlineText, MDDialogContentContainer, MDDialogButtonContainer
from kivymd.uix.button import MDButton, MDButtonText
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.textfield import MDTextField, MDTextFieldHintText
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.label import MDLabel

from controllers.nota_controller import NotaController
from controllers.estudiante_controller import EstudianteController
from controllers.materia_controller import MateriaController

# Cargar el archivo .kv asociado explícitamente
kv_path = os.path.join(os.path.dirname(__file__), 'notas_tab.kv')
Builder.load_file(kv_path)

class MenuListItem(MDListItem):
    text = StringProperty()

class NotasTab(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # Color fijo para evitar el parpadeo de fondo al cambiar de tab
        self.md_bg_color = (0.08, 0.08, 0.08, 1)

        self.nota_controller = NotaController()
        self.estudiante_controller = EstudianteController()
        self.materia_controller = MateriaController()
        
        self.dialog = None
        self.dialog_detalle = None
        self.menu_estudiantes = None
        self.menu_materias = None
        self.estudiante_id = None
        self.materia_id = None
        
    def on_enter(self, *args):
        Clock.schedule_once(lambda dt: self.cargar_notas_seguro(), 0.1)

    # ==========================================
    # LÓGICA DE LISTADO
    # ==========================================
    def cargar_notas_seguro(self):
        if 'lista_notas' not in self.ids:
            Clock.schedule_once(lambda dt: self.cargar_notas_seguro(), 0.2)
            return

        self.ids.lista_notas.clear_widgets()
        notas = self.nota_controller.obtener_todas()
        
        if not notas:
            self.mostrar_mensaje("No hay notas registradas.", (0.5, 0.5, 0.5, 1))
            return
            
        self.mostrar_mensaje("", (0,0,0,0))
        
        for nota in notas:
            promedio = float(nota[3]) if nota[3] else 0.0
            
            # Quitamos el MDListItemTrailingIcon para evitar conflictos de clics
            item = MDListItem(
                MDListItemHeadlineText(text=f"{nota[1]} - {nota[2]}"),
                MDListItemSupportingText(text=f"Promedio: {promedio:.2f} | Estado: {nota[4]}"),
                MDListItemTertiaryText(text=f"Fecha: {nota[5]}"),
                on_release=lambda x, n=nota: self.ver_detalle(n)
            )
            self.ids.lista_notas.add_widget(item)

    def mostrar_mensaje(self, texto, color):
        if 'lbl_mensaje' in self.ids:
            lbl = self.ids.lbl_mensaje
            lbl.text = texto
            lbl.text_color = color
            lbl.height = dp(30) if texto else dp(0)

    # ==========================================
    # LÓGICA DEL DIÁLOGO (Agregar Nota)
    # ==========================================
    def abrir_dialogo_agregar(self):
        self.estudiante_id = None
        self.materia_id = None
        
        contenido = self._crear_contenido_dialogo()
        
        self.dialog = MDDialog(
            MDDialogHeadlineText(text="Registrar Nueva Nota"),
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
                    on_release=self.guardar_nota
                )
            )
        )
        self.dialog.open()

    def _crear_contenido_dialogo(self):
        layout = MDBoxLayout(
            orientation='vertical',
            spacing=dp(15),
            padding=dp(10),
            adaptive_height=True
        )
        
        self.btn_est = MDButton(
            MDButtonText(text="Seleccionar Estudiante", pos_hint={"center_x": 0.5, "center_y": 0.5}), 
            style="outlined", 
            size_hint_x=1
        )
        self.btn_est.bind(on_release=self.mostrar_menu_estudiantes)
        
        self.btn_mat = MDButton(
            MDButtonText(text="Seleccionar Materia", pos_hint={"center_x": 0.5, "center_y": 0.5}), 
            style="outlined", 
            size_hint_x=1
        )
        self.btn_mat.bind(on_release=self.mostrar_menu_materias)
        
        self.campos_notas = []
        box_notas = MDGridLayout(
            cols=3, 
            spacing=dp(10), 
            adaptive_height=True
        )
        
        for i in range(5):
            tf = MDTextField(MDTextFieldHintText(text=f"N{i+1}"), mode="outlined")
            self.campos_notas.append(tf)
            box_notas.add_widget(tf)
            
        self.lbl_error_dlg = MDLabel(
            text="", 
            theme_text_color="Custom", 
            text_color=(1,0,0,1), 
            size_hint_y=None, 
            height=dp(20),
            font_style="Body",
            role="small"
        )
        
        layout.add_widget(self.btn_est)
        layout.add_widget(self.btn_mat)
        layout.add_widget(box_notas)
        layout.add_widget(self.lbl_error_dlg)
        
        return layout

    # ==========================================
    # LÓGICA DE MENÚS DESPLEGABLES
    # ==========================================
    def mostrar_menu_estudiantes(self, instancia_boton):
        estudiantes = self.estudiante_controller.listar_todos()
        menu_items = [
            {
                "text": f"{est[1]} - {est[2]} {est[3]}",
                "viewclass": "MenuListItem",
                "on_release": lambda x=est: self.seleccionar_estudiante(x)
            } for est in estudiantes
        ]
        self.menu_estudiantes = MDDropdownMenu(caller=instancia_boton, items=menu_items)
        self.menu_estudiantes.open()

    def seleccionar_estudiante(self, estudiante):
        self.estudiante_id = estudiante[0]
        self.btn_est.children[0].text = f"{estudiante[1]} - {estudiante[2]}"
        self.menu_estudiantes.dismiss()

    def mostrar_menu_materias(self, instancia_boton):
        materias = self.materia_controller.listar_por_profesor(profesor_id=1) 
        menu_items = [
            {
                "text": mat[1],
                "viewclass": "MenuListItem",
                "on_release": lambda x=mat: self.seleccionar_materia(x)
            } for mat in materias
        ]
        self.menu_materias = MDDropdownMenu(caller=instancia_boton, items=menu_items)
        self.menu_materias.open()

    def seleccionar_materia(self, materia):
        self.materia_id = materia[0]
        self.btn_mat.children[0].text = materia[1]
        self.menu_materias.dismiss()

    # ==========================================
    # CRUD Y DETALLES
    # ==========================================
    def guardar_nota(self, *args):
        if not self.estudiante_id or not self.materia_id:
            self.lbl_error_dlg.text = "Seleccione estudiante y materia"
            return
            
        notas_valores = []
        try:
            for campo in self.campos_notas:
                if not campo.text.strip():
                    raise ValueError
                val = float(campo.text)
                if val < 0 or val > 20: 
                    raise ValueError
                notas_valores.append(val)
        except ValueError:
            self.lbl_error_dlg.text = "Debe ingresar 5 notas validas (0 a 20)"
            return
            
        resultado = self.nota_controller.guardar_notas(
            self.estudiante_id, self.materia_id, *notas_valores
        )
        
        if resultado['success']:
            self.dialog.dismiss()
            self.cargar_notas_seguro()
            self.mostrar_mensaje(f"Guardado exitosamente.", (0, 0.7, 0, 1))
        else:
            self.lbl_error_dlg.text = resultado['message']

    def eliminar_nota(self, nota_id):
        resultado = self.nota_controller.eliminar_nota(nota_id)
        if resultado.get('success'):
            self.cargar_notas_seguro()
            self.mostrar_mensaje("Registro eliminado exitosamente.", (0, 0.7, 0, 1))
        else:
            self.mostrar_mensaje("Error al eliminar el registro.", (1, 0, 0, 1))

    def ver_detalle(self, nota):
        # nota = (id, estudiante, materia, promedio, estado, fecha, n1, n2, n3, n4, n5)
        promedio = float(nota[3]) if nota[3] else 0.0
        
        # 1. Contenedor principal con padding y spacing generoso
        contenido = MDBoxLayout(
            orientation="vertical", 
            adaptive_height=True, 
            spacing=dp(15),
            padding=dp(10)
        )
        
        # Helper para etiquetas limpias
        def crear_label(texto, estilo="Body", rol="medium"):
            return MDLabel(
                text=texto, 
                font_style=estilo, 
                role=rol, 
                adaptive_height=True,
                shorten=True,
                shorten_from='right'
            )

        # 2. Información del registro
        contenido.add_widget(crear_label(f"Estudiante: {nota[1]}", "Title", "medium"))
        contenido.add_widget(crear_label(f"Materia: {nota[2]}"))
        
        # 3. Cuadrícula de notas (Estructura 2-2-1)
        box_notas = MDBoxLayout(orientation='vertical', spacing=dp(10), adaptive_height=True)
        self.campos_edicion_notas = []
        for i in range(5):
            tf = MDTextField(
                MDTextFieldHintText(text=f"N{i+1}"), 
                mode="outlined",
                text=str(nota[6+i]) if nota[6+i] is not None else "0"
            )
            self.campos_edicion_notas.append(tf)

        # Filas de edición
        fila1 = MDGridLayout(cols=2, spacing=dp(10), adaptive_height=True)
        fila1.add_widget(self.campos_edicion_notas[0]); fila1.add_widget(self.campos_edicion_notas[1])
        
        fila2 = MDGridLayout(cols=2, spacing=dp(10), adaptive_height=True)
        fila2.add_widget(self.campos_edicion_notas[2]); fila2.add_widget(self.campos_edicion_notas[3])
        
        fila3 = MDBoxLayout(adaptive_height=True)
        fila3.add_widget(self.campos_edicion_notas[4])

        box_notas.add_widget(fila1); box_notas.add_widget(fila2); box_notas.add_widget(fila3)
        contenido.add_widget(box_notas)
        
        # 4. Info de resultados
        info_resultados = MDBoxLayout(orientation="vertical", adaptive_height=True, spacing=dp(5))
        info_resultados.add_widget(crear_label(f"Promedio Actual: {promedio:.2f}", "Title", "small"))
        info_resultados.add_widget(crear_label(f"Estado Actual: {nota[4]}", "Title", "small"))
        
        self.lbl_error_edicion = MDLabel(
            text="", theme_text_color="Custom", text_color=(1,0,0,1), 
            size_hint_y=None, height=dp(20), font_style="Body", role="small"
        )
        info_resultados.add_widget(self.lbl_error_edicion)
        contenido.add_widget(info_resultados)
        
        # 5. BOTONES DE ACCIÓN (Estructura personalizada para evitar desbordes)
        box_botones_final = MDBoxLayout(orientation="vertical", spacing=dp(10), adaptive_height=True, padding=[0, dp(10), 0, 0])

        fila_acciones = MDBoxLayout(orientation="horizontal", spacing=dp(10), size_hint_y=None, height=dp(50))
        
        btn_eliminar = MDButton(
            MDButtonText(text="ELIMINAR", theme_text_color="Custom", text_color=(0.8, 0.1, 0.1, 1)),
            style="text", size_hint_x=0.5,
            on_release=lambda x, n_id=nota[0]: self.ejecutar_eliminar_desde_dialogo(n_id)
        )
        btn_guardar = MDButton(
            MDButtonText(text="GUARDAR"),
            style="elevated", size_hint_x=0.5,
            on_release=lambda x, n_id=nota[0]: self.guardar_edicion_notas(n_id)
        )
        fila_acciones.add_widget(btn_eliminar)
        fila_acciones.add_widget(btn_guardar)

        btn_cerrar = MDButton(
            MDButtonText(text="CERRAR"),
            style="text", size_hint_x=1,
            on_release=lambda x: self.dialog_detalle.dismiss()
        )

        box_botones_final.add_widget(fila_acciones)
        box_botones_final.add_widget(btn_cerrar)
        contenido.add_widget(box_botones_final)
        
        # 6. Lanzar diálogo
        self.dialog_detalle = MDDialog(
            MDDialogHeadlineText(text="Detalle y Edición"),
            MDDialogContentContainer(contenido),
        )
        self.dialog_detalle.open()

    def ejecutar_eliminar_desde_dialogo(self, nota_id):
        """Cierra el diálogo y luego elimina la nota"""
        self.dialog_detalle.dismiss()
        self.eliminar_nota(nota_id)

    def guardar_edicion_notas(self, nota_id):
        notas_valores = []
        try:
            for campo in self.campos_edicion_notas:
                if not campo.text.strip():
                    raise ValueError
                val = float(campo.text)
                if val < 0 or val > 20: 
                    raise ValueError
                notas_valores.append(val)
        except ValueError:
            self.lbl_error_edicion.text = "Debe ingresar 5 notas validas (0 a 20)"
            return
            
        resultado = self.nota_controller.actualizar_notas(nota_id, *notas_valores)
        
        if resultado['success']:
            self.dialog_detalle.dismiss()
            self.cargar_notas_seguro()
            self.mostrar_mensaje(f"Actualizado. Nuevo Promedio: {resultado['promedio']:.2f}", (0, 0.7, 0, 1))
        else:
            self.lbl_error_edicion.text = resultado['message']