from kivy.lang import Builder
from kivy.metrics import dp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.card import MDCard
from kivymd.uix.textfield import MDTextField, MDTextFieldHintText
from kivymd.uix.button import MDButton, MDButtonText
from kivymd.uix.label import MDLabel
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.list import MDListItem
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.gridlayout import MDGridLayout

from controllers.estudiante_controller import EstudianteController
from controllers.materia_controller import MateriaController
from controllers.nota_controller import NotaController

Builder.load_string('''
<MyMenuItem@MDListItem>:
    text: ""
    MDListItemHeadlineText:
        text: root.text
''')

# NUEVO: Heredamos de MDScrollView para que nunca se aplasten los elementos
class NotasTab(MDScrollView):
    def __init__(self, profesor_id, **kwargs):
        super().__init__(**kwargs)
        self.profesor_id = profesor_id
        
        self.estudiante_controller = EstudianteController()
        self.materia_controller = MateriaController()
        self.nota_controller = NotaController()
        
        self.estudiante_id = None
        self.materia_id = None
        
        self.menu_estudiantes = None
        self.menu_materias = None
        
        self.build_ui()
    
    def build_ui(self):
        # CONTENEDOR PRINCIPAL: Aquí va todo y se adaptará a la altura del contenido
        layout_principal = MDBoxLayout(
            orientation='vertical',
            spacing=dp(20),
            padding=dp(20),
            adaptive_height=True # Mágia responsiva
        )
        
        # --- TARJETA DE SELECCIÓN ---
        tarjeta_seleccion = MDCard(
            orientation='vertical',
            padding=dp(20),
            spacing=dp(15),
            elevation=2,
            radius=[10, 10, 10, 10],
            adaptive_height=True # Mágia responsiva
        )
        
        self.dropdown_estudiante = MDButton(
            MDButtonText(text="Seleccionar Estudiante", pos_hint={"center_x": 0.5, "center_y": 0.5}),
            style="elevated",
            size_hint_x=1 # Ocupa todo el ancho de la tarjeta
        )
        self.dropdown_estudiante.bind(on_release=self.abrir_menu_estudiantes)
        
        self.dropdown_materia = MDButton(
            MDButtonText(text="Seleccionar Materia", pos_hint={"center_x": 0.5, "center_y": 0.5}),
            style="elevated",
            size_hint_x=1
        )
        self.dropdown_materia.bind(on_release=self.abrir_menu_materias)
        
        tarjeta_seleccion.add_widget(self.dropdown_estudiante)
        tarjeta_seleccion.add_widget(self.dropdown_materia)
        
        # --- TARJETA DE NOTAS ---
        tarjeta_notas = MDCard(
            orientation='vertical',
            padding=dp(20),
            spacing=dp(20),
            elevation=2,
            radius=[10, 10, 10, 10],
            adaptive_height=True
        )
        
        # CAMBIO: Usamos MDGridLayout para organizar en 2 columnas y que no se aplaste
        layout_notas = MDGridLayout(
            cols=2,
            spacing=dp(15),
            adaptive_height=True
        )
        
        self.campo_nota1 = MDTextField(MDTextFieldHintText(text="N1 (0-20)"), mode="outlined", input_filter="float")
        self.campo_nota2 = MDTextField(MDTextFieldHintText(text="N2 (0-20)"), mode="outlined", input_filter="float")
        self.campo_nota3 = MDTextField(MDTextFieldHintText(text="N3 (0-20)"), mode="outlined", input_filter="float")
        self.campo_nota4 = MDTextField(MDTextFieldHintText(text="N4 (0-20)"), mode="outlined", input_filter="float")
        self.campo_nota5 = MDTextField(MDTextFieldHintText(text="N5 (0-20)"), mode="outlined", input_filter="float")
        
        layout_notas.add_widget(self.campo_nota1)
        layout_notas.add_widget(self.campo_nota2)
        layout_notas.add_widget(self.campo_nota3)
        layout_notas.add_widget(self.campo_nota4)
        layout_notas.add_widget(self.campo_nota5)
        
        self.boton_guardar = MDButton(
            MDButtonText(text="Calcular y Guardar", pos_hint={"center_x": 0.5, "center_y": 0.5}),
            style="elevated",
            theme_bg_color="Custom",
            md_bg_color=(0.1, 0.5, 0.8, 1),
            pos_hint={"center_x": 0.5},
            size_hint_x=0.8
        )
        self.boton_guardar.bind(on_release=self.guardar_notas)
        
        tarjeta_notas.add_widget(layout_notas)
        tarjeta_notas.add_widget(self.boton_guardar)
     
        # --- LABELS DE RESULTADOS ---
        self.resultado_label = MDLabel(
            text="",
            halign="center",
            font_style="Title",
            role="large",
            adaptive_height=True
        )
        
        titulo_historial = MDLabel(
            text="Últimas notas guardadas",
            font_style="Title",
            role="medium",
            adaptive_height=True
        )
        
        self.historial_label = MDLabel(
            text="Selecciona un estudiante y una materia para ver su historial",
            halign="center",
            theme_text_color="Secondary",
            adaptive_height=True
        )
        
        # Agregamos todo al layout principal
        layout_principal.add_widget(tarjeta_seleccion)
        layout_principal.add_widget(tarjeta_notas)
        layout_principal.add_widget(self.resultado_label)
        layout_principal.add_widget(titulo_historial)
        layout_principal.add_widget(self.historial_label)
        
        # Agregamos el layout principal al ScrollView
        self.add_widget(layout_principal)
    
    # ======================================================================
    # LÓGICA DE MENÚS (Ahora consultan la BD en tiempo real)
    # ======================================================================
    
    def abrir_menu_estudiantes(self, instance):
        """Abre menú desplegable consultando los estudiantes en el momento"""
        # 1. Obtenemos datos frescos
        estudiantes = self.estudiante_controller.listar_todos()
        
        if not estudiantes:
            self.resultado_label.text = "⚠️ No hay estudiantes registrados"
            self.resultado_label.theme_text_color = "Error"
            return
        
        # 2. Armamos el menú usando nuestra clase MyMenuItem
        menu_items = []
        for est in estudiantes:
            texto = f"{est[2]} {est[3]} ({est[1]})"
            menu_items.append({
                "text": texto,
                "viewclass": "MyMenuItem",  # Soluciona el menú en blanco
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
        
        for child in self.dropdown_estudiante.children:
            if isinstance(child, MDButtonText):
                child.text = texto
                break
                
        self.menu_estudiantes.dismiss()
        self.actualizar_historial()
    
    def abrir_menu_materias(self, instance):
        """Abre menú desplegable consultando materias en el momento"""
        # 1. Obtenemos datos frescos
        materias = self.materia_controller.listar_por_profesor(self.profesor_id)
        
        if not materias:
            self.resultado_label.text = "⚠️ No tienes materias creadas"
            self.resultado_label.theme_text_color = "Error"
            return
        
        # 2. Armamos el menú
        menu_items = []
        for mat in materias:
            menu_items.append({
                "text": mat[1],
                "viewclass": "MyMenuItem", # Soluciona el menú en blanco
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
        
        for child in self.dropdown_materia.children:
            if isinstance(child, MDButtonText):
                child.text = materia[1]
                break
                
        self.menu_materias.dismiss()
        self.actualizar_historial()
  
    # ======================================================================
    # LÓGICA DE NOTAS (Mantenida exactamente igual)
    # ======================================================================

    def guardar_notas(self, instance):
        """Guarda las 5 notas calculando promedio y estado"""
        if not self.estudiante_id or not self.materia_id:
            self.resultado_label.text = "⚠️ Selecciona un estudiante y una materia"
            self.resultado_label.theme_text_color = "Error"
            return
        
        # 1. NUEVA VALIDACIÓN: Capturar textos y verificar que no estén vacíos
        textos_notas = [
            self.campo_nota1.text.strip(),
            self.campo_nota2.text.strip(),
            self.campo_nota3.text.strip(),
            self.campo_nota4.text.strip(),
            self.campo_nota5.text.strip()
        ]
        
        # Si hay alguna cadena vacía en la lista, mostramos error
        if "" in textos_notas:
            self.resultado_label.text = "⚠️ Por favor, llena todos los campos de notas"
            self.resultado_label.theme_text_color = "Error"
            return
        
        # 2. Conversión segura a números
        try:
            n1 = float(textos_notas[0])
            n2 = float(textos_notas[1])
            n3 = float(textos_notas[2])
            n4 = float(textos_notas[3])
            n5 = float(textos_notas[4])
        except ValueError:
            self.resultado_label.text = "⚠️ Ingresa notas válidas (solo números)"
            self.resultado_label.theme_text_color = "Error"
            return
        
        # 3. Validar el rango (0 a 20)
        for nota in [n1, n2, n3, n4, n5]:
            if nota < 0 or nota > 20:
                self.resultado_label.text = "⚠️ Las notas deben estar entre 0 y 20"
                self.resultado_label.theme_text_color = "Error"
                return
        
        # 4. Guardar resultados
        resultado = self.nota_controller.guardar_notas(
            self.estudiante_id,
            self.materia_id,
            n1, n2, n3, n4, n5
        )
        
        if resultado['success']:
            promedio = resultado['promedio']
            estado = resultado['estado']
            emoji = "✅" if estado == "APRUEBA" else "❌"
            color = (0, 0.6, 0, 1) if estado == "APRUEBA" else (0.8, 0, 0, 1)
            
            self.resultado_label.text = f"{emoji} Promedio: {promedio:.2f} - {estado}"
            self.resultado_label.theme_text_color = "Custom"
            self.resultado_label.text_color = color
            
            self.campo_nota1.text = ""
            self.campo_nota2.text = ""
            self.campo_nota3.text = ""
            self.campo_nota4.text = ""
            self.campo_nota5.text = ""
            
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
        
        texto = ""
        for h in historial:
            promedio = h[5]
            estado = h[6]
            fecha = h[7][:10]
            emoji = "✅" if estado == "APRUEBA" else "❌"
            texto += f"{emoji} Prom: {promedio:.2f} - {estado} ({fecha})\n"
        
        self.historial_label.text = texto
        self.historial_label.theme_text_color = "Primary"
        self.historial_label.halign = "left"