import tkinter as tk
from tkinter import messagebox, scrolledtext, ttk
from PIL import Image, ImageTk
import importlib

# Definición de colores y estilos
COLORS = {
    'primary': '#1B4F72',  # Azul oscuro para título
    'secondary': '#3498DB',  # Azul secundario
    'accent': '#E74C3C',  # Rojo para alertas
    'background': '#CAFA5A',  # Color mostaza para fondo
    'text': '#2C3E50',  # Color texto principal
    'success': '#27AE60'  # Verde para éxito
}

def crear_imagen_bandera(pais):
    """Crea un Label con la bandera del país"""
    try:
        image_path = f"banderas/{pais.lower()}.png"
        image = Image.open(image_path)
        image = image.resize((50, 30), Image.Resampling.LANCZOS)  # Ajustar el tamaño de la imagen
        photo = ImageTk.PhotoImage(image)
        label = tk.Label(image=photo, bg=COLORS['background'])
        label.image = photo  # Keep a reference to avoid garbage collection
        return label
    except Exception as e:
        print(f"Error al cargar la imagen de la bandera para {pais}: {e}")
        return None

class MatriculasApp:
    def __init__(self, root):
        self.entry_matricula = None
        self.text_resultado = None
        self.btn_limpiar = None
        self.btn_analizar = None
        self.bandera_frame = None
        self.root = root
        self.root.title("Análisis de Matrículas Internacionales")
        self.root.geometry("800x700")
        self.root.configure(bg=COLORS['background'])

        # Configurar archivo Excel y países
        archivo_excel_colombia = "paises/PlacasColombia.xlsx"
        self.paises = self.cargar_paises(archivo_excel_colombia)

        self.bandera_label = None
        self.setup_ui()

    def mostrar_bandera(self, pais_nombre):
        """Muestra la bandera del país"""
        bandera_label = crear_imagen_bandera(pais_nombre)
        if bandera_label:
            return bandera_label
        else:
            return None

    def mostrar_formato(self, pais):
        """Muestra el formato de la matrícula del país seleccionado"""
        mensajes = {
            "Argentina": "Ejemplo de matrícula: AA895AA",
            "Ecuador": "Ejemplo de matrícula: ABC-1234",
            "El Salvador": "Ejemplo de matrícula: AB123 456",
            "Haiti": "Ejemplo de matrícula: AA 12345",
            "México": "Ejemplo de matrícula: ABC-123",
            "Panamá": "Ejemplo de matrícula: 123456 o AB1234",
            "Paraguay": "Ejemplo de matrícula: ABCD123",
            "Perú": "Ejemplo de matrícula: ABC-123",
            "Costa Rica": "Ejemplo de matrícula: ABC-1234"
        }

        mensaje = mensajes.get(pais.nombre, f"No hay formatos de matrícula disponibles para {pais.nombre}.")
        messagebox.showinfo("Formato de Matrícula", mensaje)

    def cargar_paises(self, archivo_excel_colombia):
        paises = ["argentina", "brasil","bolivia","chile", "colombia","cuba","costa","salvador" ,"ecuador","haiti" ,"mexico","panama","paraguay","peru","rd", "uruguay", "venezuela" ]
        clases_paises = []
        for pais in paises:
            modulo = importlib.import_module(f"paises.{pais}")
            clase_pais = getattr(modulo, pais.capitalize())
            if pais == "colombia":
                clases_paises.append(clase_pais(archivo_excel_colombia))
            else:
                clases_paises.append(clase_pais())
        return clases_paises

    def setup_ui(self):
        # Frame principal
        main_frame = tk.Frame(self.root, bg=COLORS['background'])
        main_frame.pack(expand=True, fill='both', padx=20, pady=20)

        # Título
        title_label = tk.Label(
            main_frame,
            text="Sistema de Identification de Matrículas",
            font=('Arial', 24, 'bold'),
            bg=COLORS['background'],
            fg=COLORS['primary']
        )
        title_label.pack(pady=(0, 20))

        # Frame para la bandera
        self.bandera_frame = tk.Frame(main_frame, bg=COLORS['background'])
        self.bandera_frame.pack(pady=10)

        # Frame para entrada
        input_frame = tk.Frame(main_frame, bg=COLORS['background'])
        input_frame.pack(fill='x', padx=50)

        # Etiqueta y entrada de matrícula
        label_matricula = tk.Label(
            input_frame,
            text="Ingrese la matrícula:",
            font=('Arial', 12, 'bold'),
            bg=COLORS['background'],
            fg=COLORS['text']
        )
        label_matricula.pack(pady=(0, 5))

        self.entry_matricula = tk.Entry(
            input_frame,
            font=('Arial', 14),
            width=30,
            justify='center'
        )
        self.entry_matricula.pack(pady=(0, 10))

        # Botón de análisis
        self.btn_analizar = tk.Button(
            input_frame,
            text="🔍 Analizar Matrícula",
            command=self.analizar_matricula,
            bg=COLORS['primary'],
            fg='white',
            font=('Arial', 12, 'bold'),
            relief='raised',
            cursor='hand2',
            padx=20,
            pady=10
        )
        self.btn_analizar.pack(pady=10)

        # Botón de limpiar
        self.btn_limpiar = tk.Button(
            input_frame,
            text="🧹 Limpiar",
            command=self.limpiar_pantalla,
            bg=COLORS['accent'],
            fg='white',
            font=('Arial', 12, 'bold'),
            relief='raised',
            cursor='hand2',
            padx=20,
            pady=10
        )
        self.btn_limpiar.pack(pady=10)

        # Configurar hover effects
        self.btn_analizar.bind('<Enter>', lambda e: self.btn_analizar.config(
            bg=COLORS['secondary']))
        self.btn_analizar.bind('<Leave>', lambda e: self.btn_analizar.config(
            bg=COLORS['primary']))
        self.btn_limpiar.bind('<Enter>', lambda e: self.btn_limpiar.config(
            bg=COLORS['secondary']))
        self.btn_limpiar.bind('<Leave>', lambda e: self.btn_limpiar.config(
            bg=COLORS['accent']))

        # Área de resultados
        result_frame = tk.Frame(main_frame, bg=COLORS['background'])
        result_frame.pack(fill='both', expand=True, padx=20, pady=(20, 0))

        # Título de resultados
        result_label = tk.Label(
            result_frame,
            text="📋 Resultados del Análisis",
            font=('Arial', 14, 'bold'),
            bg=COLORS['background'],
            fg=COLORS['primary']
        )
        result_label.pack(pady=(0, 10))

        # Área de texto con scroll
        self.text_resultado = scrolledtext.ScrolledText(
            result_frame,
            width=70,
            height=15,
            font=('Arial', 11),
            bg='white',
            wrap=tk.WORD
        )
        self.text_resultado.pack(fill='both', expand=True)

        # Frame para las banderas de los países con scroll
        flags_frame = tk.Frame(main_frame, bg=COLORS['background'])
        flags_frame.pack(pady=10, fill='x')

        canvas = tk.Canvas(flags_frame, bg=COLORS['background'])
        scrollbar = ttk.Scrollbar(flags_frame, orient="horizontal", command=canvas.xview)
        scrollable_frame = tk.Frame(canvas, bg=COLORS['background'])

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(xscrollcommand=scrollbar.set)

        canvas.pack(side="top", fill="x", expand=True)
        scrollbar.pack(side="bottom", fill="x")

        # Crear botones de banderas
        for pais in self.paises:
            bandera_label = crear_imagen_bandera(pais.nombre)
            if bandera_label:
                btn_bandera = tk.Button(
                    scrollable_frame,
                    image=bandera_label.image,
                    command=lambda p=pais: self.mostrar_formato(p),
                    bg=COLORS['background'],
                    relief='flat',
                    cursor='hand2'
                )
                btn_bandera.image = bandera_label.image  # Keep a reference to avoid garbage collection
                btn_bandera.pack(side='left', padx=5)
##################

    def analizar_matricula(self):
        # Implementar la lógica de análisis de matrícula
        matricula = self.entry_matricula.get().strip().upper()
        resultados = []

        self.text_resultado.delete(1.0, tk.END)
        self.text_resultado.configure(bg='white')

        for pais in self.paises:
            valido, partes = pais.validar_matricula(matricula)
            if valido:
                derivacion = []
                if hasattr(pais, "derivar_matricula"):
                    derivacion = pais.derivar_matricula(partes)

                resultado = f"\n=== RESULTADO PARA {pais.nombre.upper()} ===\n\n"
                resultado += f"🚗 Matrícula analizada: {matricula}\n"
                resultado += f"📍 País identificado: {pais.nombre}\n"

                if "region" in partes:
                    resultado += f"🗺️ Región: {partes['region']}\n"
                if "departamentos" in partes:
                    resultado += f"📌 Departamentos: {partes['departamentos']}\n"
                if "provincia" in partes:
                    resultado += f"🏛️ Provincia: {partes['provincia']}\n"
                if "departamento" in partes:
                    resultado += f"🏢 Departamento: {partes['departamento']}\n"
                if "ciudad" in partes:
                    resultado += f"🌆 Ciudad: {partes['ciudad']}\n"
                if "tipo_vehiculo" in partes:
                    resultado += f"🔤 Tipo de vehículo: {partes['tipo_vehiculo']}\n"

                resultado += "\n📝 Derivación por la izquierda:\n"
                for paso in derivacion:
                    resultado += f"➜ {paso}\n"

                resultado += "\n" + "=" * 50 + "\n"

                resultados.append((pais.nombre, resultado, self.mostrar_bandera(pais.nombre)))

        if resultados:
            if len(resultados) > 1:
                self.text_resultado.insert(tk.END, "⚠️ ¡ATENCIÓN! La matrícula es válida en múltiples países:\n")
                for pais, res, bandera in resultados:
                    if bandera:
                        self.text_resultado.window_create(tk.END, window=bandera)
                    self.text_resultado.insert(tk.END, res)
            else:
                if resultados[0][2]:
                    self.text_resultado.window_create(tk.END, window=resultados[0][2])
                self.text_resultado.insert(tk.END, resultados[0][1])

            self.text_resultado.configure(bg='#E8F8F5')
        else:
            self.text_resultado.configure(bg='#FADBD8')
            messagebox.showerror("Error", "❌ Formato de matrícula inválido o no corresponde a ningún país disponible.")

    def limpiar_pantalla(self):
        # Implementar la lógica para limpiar la pantalla
        self.entry_matricula.delete(0, tk.END)
        self.text_resultado.delete(1.0, tk.END)
        #self.mostrar_bandera("")

if __name__ == "__main__":
    root = tk.Tk()
    app = MatriculasApp(root)
    root.mainloop()