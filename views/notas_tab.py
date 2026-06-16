
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.card import MDCard
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.label import MDLabel
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.list import OneLineListItem

from controllers.estudiante_controller import EstudianteController
from controllers.materia_controller import MateriaController
from controllers.nota_controller import NotaController


class NotasTab(MDBoxLayout):
    """
    Pestaña para gestionar notas.
    Contiene: selección de estudiante, selección de materia, 5 campos de notas,
    botón guardar, resultado e historial.
    """
    
    def __init__(self, profesor_id, **kwargs):
        super().__init__(**kwargs)
        self.profesor_id = profesor_id
        self.orientation = 'vertical'
        self.spacing = 15
        self.padding = 15
        

        # 3. CONTROLADORES
        self.estudiante_controller = EstudianteController()
        self.materia_controller = MateriaController()
        self.nota_controller = NotaController()
        

        # 4. VARIABLES PARA SELECCIONES
        self.estudiante_id = None
        self.materia_id = None
        self.estudiantes = []
        self.materias = []
        

        # 5. REFERENCIAS A MENÚS        
        self.menu_estudiantes = None
        self.menu_materias = None
        
        # Construir interfaz
        self.build_ui()
        
        # Cargar datos iniciales
        self.cargar_datos()
    
    
    def build_ui(self):
        """interfaz de la pestaña Notas"""
        
        tarjeta_seleccion = MDCard(
            orientation='vertical',
            padding=15,
            spacing=10,
            size_hint_y=None,
            height=120,
            elevation=2,
            radius=[10, 10, 10, 10]
        )
        
        # Dropdown: Estudiante
        self.dropdown_estudiante = MDRaisedButton(
            text="Seleccionar Estudiante",
            size_hint=(1, 1)
        )
        self.dropdown_estudiante.bind(on_release=self.abrir_menu_estudiantes)
        
        # Dropdown: Materia
        self.dropdown_materia = MDRaisedButton(
            text="Seleccionar Materia",
            size_hint=(1, 1)
        )
        self.dropdown_materia.bind(on_release=self.abrir_menu_materias)
        
        tarjeta_seleccion.add_widget(self.dropdown_estudiante)
        tarjeta_seleccion.add_widget(self.dropdown_materia)
        
        
        tarjeta_notas = MDCard(
            orientation='vertical',
            padding=15,
            spacing=10,
            size_hint_y=None,
            height=180,
            elevation=2,
            radius=[10, 10, 10, 10]
        )
        
        # Layout horizontal para 5 notas
        layout_notas = MDBoxLayout(
            orientation='horizontal',
            spacing=10,
            size_hint_y=0.5
        )
        
        self.campo_nota1 = MDTextField(
            hint_text="N1 (0-20)",
            mode="rectangle",
            input_filter="float"
        )
        self.campo_nota2 = MDTextField(
            hint_text="N2 (0-20)",
            mode="rectangle",
            input_filter="float"
        )
        self.campo_nota3 = MDTextField(
            hint_text="N3 (0-20)",
            mode="rectangle",
            input_filter="float"
        )
        self.campo_nota4 = MDTextField(
            hint_text="N4 (0-20)",
            mode="rectangle",
            input_filter="float"
        )
        self.campo_nota5 = MDTextField(
            hint_text="N5 (0-20)",
            mode="rectangle",
            input_filter="float"
        )
        
        layout_notas.add_widget(self.campo_nota1)
        layout_notas.add_widget(self.campo_nota2)
        layout_notas.add_widget(self.campo_nota3)
        layout_notas.add_widget(self.campo_nota4)
        layout_notas.add_widget(self.campo_nota5)
        
        # Botón Guardar
        self.boton_guardar = MDRaisedButton(
            text="Calcular y Guardar",
            size_hint_y=0.3,
            md_bg_color=(0.1, 0.5, 0.8, 1),
            pos_hint={"center_x": 0.5}
        )
        self.boton_guardar.bind(on_release=self.guardar_notas)
        
        tarjeta_notas.add_widget(layout_notas)
        tarjeta_notas.add_widget(self.boton_guardar)
     
        
        self.resultado_label = MDLabel(
            text="",
            halign="center",
            font_style="H5",
            size_hint_y=None,
            height=50
        )
        
        
        titulo_historial = MDLabel(
            text="Últimas notas guardadas",
            font_style="H6",
            size_hint_y=None,
            height=30
        )
        
        self.historial_label = MDLabel(
            text="Selecciona un estudiante y una materia para ver su historial",
            halign="center",
            theme_text_color="Secondary",
            size_hint_y=None,
            height=50
        )
        
        
        self.add_widget(tarjeta_seleccion)
        self.add_widget(tarjeta_notas)
        self.add_widget(self.resultado_label)
        self.add_widget(titulo_historial)
        self.add_widget(self.historial_label)
    
    
    def cargar_datos(self):
        """Carga estudiantes y materias desde la BD"""
        # Cargar estudiantes
        self.estudiantes = self.estudiante_controller.listar_todos()
        
        # Cargar materias del profesor
        self.materias = self.materia_controller.listar_por_profesor(self.profesor_id)
    
    
    def abrir_menu_estudiantes(self, instance):
        """Abre menú desplegable con estudiantes"""
        if not self.estudiantes:
            return
        
        menu_items = []
        for est in self.estudiantes:
            # est = (id, cedula, nombres, apellidos, pnf, trayecto, seccion)
            texto = f"{est[2]} {est[3]} ({est[1]})"
            menu_items.append({
                "text": texto,
                "viewclass": "OneLineListItem",
                "on_release": lambda x=est: self.seleccionar_estudiante(x)
            })
        
        self.menu_estudiantes = MDDropdownMenu(
            caller=instance,
            items=menu_items,
            width_mult=4
        )
        self.menu_estudiantes.open()
    
    def seleccionar_estudiante(self, estudiante):
        """Selecciona un estudiante y actualiza el dropdown"""
        self.estudiante_id = estudiante[0]
        texto = f"{estudiante[2]} {estudiante[3]} ({estudiante[1]})"
        self.dropdown_estudiante.text = texto
        self.menu_estudiantes.dismiss()
        self.actualizar_historial()
    
    def abrir_menu_materias(self, instance):
        """Abre menú desplegable con materias"""
        if not self.materias:
            return
        
        menu_items = []
        for mat in self.materias:
            # mat = (id, nombre, fecha_creacion)
            menu_items.append({
                "text": mat[1],
                "viewclass": "OneLineListItem",
                "on_release": lambda x=mat: self.seleccionar_materia(x)
            })
        
        self.menu_materias = MDDropdownMenu(
            caller=instance,
            items=menu_items,
            width_mult=4
        )
        self.menu_materias.open()
    
    def seleccionar_materia(self, materia):
        """Selecciona una materia y actualiza el dropdown"""
        self.materia_id = materia[0]
        self.dropdown_materia.text = materia[1]
        self.menu_materias.dismiss()
        self.actualizar_historial()
  
    def guardar_notas(self, instance):
        """Guarda las 5 notas calculando promedio y estado"""
        
        # Validar que hay estudiante y materia seleccionados
        if not self.estudiante_id or not self.materia_id:
            self.resultado_label.text = "⚠️ Selecciona un estudiante y una materia"
            self.resultado_label.theme_text_color = "Error"
            return
        
        # Obtener notas de los campos
        try:
            n1 = float(self.campo_nota1.text) if self.campo_nota1.text else 0
            n2 = float(self.campo_nota2.text) if self.campo_nota2.text else 0
            n3 = float(self.campo_nota3.text) if self.campo_nota3.text else 0
            n4 = float(self.campo_nota4.text) if self.campo_nota4.text else 0
            n5 = float(self.campo_nota5.text) if self.campo_nota5.text else 0
        except ValueError:
            self.resultado_label.text = "⚠️ Ingresa notas válidas (números)"
            self.resultado_label.theme_text_color = "Error"
            return
        
        # Validar rango (0-20)
        for nota in [n1, n2, n3, n4, n5]:
            if nota < 0 or nota > 20:
                self.resultado_label.text = "⚠️ Las notas deben estar entre 0 y 20"
                self.resultado_label.theme_text_color = "Error"
                return
        
        # Guardar notas
        resultado = self.nota_controller.guardar_notas(
            self.estudiante_id,
            self.materia_id,
            n1, n2, n3, n4, n5
        )
        
        if resultado['success']:
            # Mostrar éxito
            promedio = resultado['promedio']
            estado = resultado['estado']
            emoji = "✅" if estado == "APRUEBA" else "❌"
            color = (0, 0.6, 0, 1) if estado == "APRUEBA" else (0.8, 0, 0, 1)
            
            self.resultado_label.text = f"{emoji} Promedio: {promedio:.2f} - {estado}"
            self.resultado_label.theme_text_color = "Custom"
            self.resultado_label.text_color = color
            
            # Limpiar campos
            self.campo_nota1.text = ""
            self.campo_nota2.text = ""
            self.campo_nota3.text = ""
            self.campo_nota4.text = ""
            self.campo_nota5.text = ""
            
            # Actualizar historial
            self.actualizar_historial()
        else:
            self.resultado_label.text = f"⚠️ {resultado['message']}"
            self.resultado_label.theme_text_color = "Error"
    
    def actualizar_historial(self):
        """Actualiza el historial de notas del estudiante/materia seleccionado"""
        if not self.estudiante_id or not self.materia_id:
            self.historial_label.text = "Selecciona un estudiante y una materia"
            return
        
        historial = self.nota_controller.obtener_historial_estudiante_materia(
            self.estudiante_id,
            self.materia_id,
            limite=10
        )
        
        if not historial:
            self.historial_label.text = "No hay notas registradas para este estudiante en esta materia"
            return
        
        # Construir texto del historial
        texto = ""
        for h in historial:
            # h = (nota1-5, promedio, estado, fecha)
            promedio = h[5]
            estado = h[6]
            fecha = h[7][:10]  # Solo la fecha
            emoji = "✅" if estado == "APRUEBA" else "❌"
            texto += f"{emoji} Prom: {promedio:.2f} - {estado} ({fecha})\n"
        
        self.historial_label.text = texto
        self.historial_label.theme_text_color = "Primary"
        self.historial_label.halign = "left"