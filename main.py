import tkinter as tk
from tkinter import messagebox, scrolledtext, ttk
from paises.argentina import Argentina
from paises.brasil import Brasil
from paises.colombia import Colombia
from paises.ecuador import Ecuador
from paises.peru import Peru

# Definición de colores y estilos
COLORS = {
    'primary': '#1B4F72',  # Azul oscuro para título
    'secondary': '#3498DB',  # Azul secundario
    'accent': '#E74C3C',  # Rojo para alertas
    'background': '#F4D03F',  # Color mostaza para fondo
    'text': '#2C3E50',  # Color texto principal
    'success': '#27AE60'  # Verde para éxito
}

# Diccionario de banderas por país
BANDERAS = {
    'Argentina': '🇦🇷',
    'Brasil': '🇧🇷',
    'Colombia': '🇨🇴',
    'Ecuador': '🇪🇨',
    'Perú': '🇵🇪'
}


def crear_imagen_bandera(pais):
    """Crea un Label con la bandera del país"""
    if pais in BANDERAS:
        return tk.Label(
            text=BANDERAS[pais],
            font=('Arial', 48),  # Tamaño grande para la bandera
            bg=COLORS['background']
        )
    return None


class MatriculasApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Análisis de Matrículas Internacionales")
        self.root.geometry("800x700")  # Un poco más alto para la bandera
        self.root.configure(bg=COLORS['background'])

        # Configurar archivo Excel y países
        archivo_excel_colombia = "PlacasColombia.xlsx"
        self.paises = [
            Colombia(archivo_excel_colombia),
            Argentina(),
            Brasil(),
            Ecuador(),
            Peru()
        ]

        self.setup_ui()

    def setup_ui(self):
        # Frame principal
        main_frame = tk.Frame(self.root, bg=COLORS['background'])
        main_frame.pack(expand=True, fill='both', padx=20, pady=20)

        # Título
        title_label = tk.Label(
            main_frame,
            text="Sistema de Análisis de Matrículas",
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

        # Configurar hover effects
        self.btn_analizar.bind('<Enter>', lambda e: self.btn_analizar.config(
            bg=COLORS['secondary']))
        self.btn_analizar.bind('<Leave>', lambda e: self.btn_analizar.config(
            bg=COLORS['primary']))

    def mostrar_bandera(self, pais):
        # Limpiar el frame de la bandera
        for widget in self.bandera_frame.winfo_children():
            widget.destroy()

        # Crear y mostrar la nueva bandera
        bandera_label = crear_imagen_bandera(pais)
        if bandera_label:
            bandera_label.pack(in_=self.bandera_frame)

    def analizar_matricula(self):
        matricula = self.entry_matricula.get().strip().upper()
        resultados = []

        # Limpiar bandera anterior
        for widget in self.bandera_frame.winfo_children():
            widget.destroy()

        for pais in self.paises:
            valido, partes = pais.validar_matricula(matricula)
            if valido:
                derivacion = []
                if hasattr(pais, "derivar_matricula"):
                    derivacion = pais.derivar_matricula(partes)

                # Mostrar la bandera del país
                self.mostrar_bandera(pais.nombre)

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

                resultado += "\n📝 Derivación por la izquierda:\n"
                for paso in derivacion:
                    resultado += f"➜ {paso}\n"

                resultado += "\n" + "=" * 50 + "\n"

                resultados.append((pais.nombre, resultado))

        # Mostrar resultados
        self.text_resultado.delete(1.0, tk.END)

        if resultados:
            if len(resultados) > 1:
                self.text_resultado.insert(tk.END, "⚠️ ¡ATENCIÓN! La matrícula es válida en múltiples países:\n")
                for pais, res in resultados:
                    self.text_resultado.insert(tk.END, res)
            else:
                self.text_resultado.insert(tk.END, resultados[0][1])

            self.text_resultado.configure(bg='#E8F8F5')  # Verde suave para éxito
        else:
            self.text_resultado.configure(bg='#FADBD8')  # Rojo suave para error
            messagebox.showerror("Error", "❌ Formato de matrícula inválido o no corresponde a ningún país disponible.")


if __name__ == "__main__":
    root = tk.Tk()
    app = MatriculasApp(root)
    root.mainloop()