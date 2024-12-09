import re
from paises.pais import Pais
from tkinter import Tk, StringVar, OptionMenu, Button

class Brasil(Pais):
    def __init__(self):
        super().__init__("Brasil")
        self.tipos_vehiculos = {
            "rojo": "Comercial",
            "verde": "Especial",
            "blanco": "Colección",
            "gris": "Colección",
            "amarillo": "Diplomático",
            "negro": "Privado"
        }

    def validar_matricula(self, matricula):
        # Validar formato general de Brasil
        patron = r"^[A-Z]{3}\d[A-Z]\d{2}$"
        if re.match(patron, matricula):
            letras = matricula[:3]
            numeros = [matricula[3], matricula[5], matricula[6]]
            letra = matricula[4]

            # Crear ventana para seleccionar el color de las letras
            root = Tk()
            root.withdraw()  # Ocultar la ventana principal

            color_var = StringVar(root)
            color_var.set("Seleccione el color")

            color_options = ["rojo", "verde", "blanco", "gris", "amarillo", "negro"]
            color_dropdown = OptionMenu(root, color_var, *color_options)
            color_dropdown.pack()

            def on_select():
                root.quit()

            select_button = Button(root, text="Seleccionar", command=on_select)
            select_button.pack()

            root.deiconify()  # Mostrar la ventana principal
            root.mainloop()

            color = color_var.get()
            tipo_vehiculo = self.tipos_vehiculos.get(color.lower(), "Desconocido")
            return True, {
                "matricula": matricula,
                "letras": letras,
                "numeros": numeros,
                "letra": letra,
                "tipo_vehiculo": tipo_vehiculo
            }
        return False, {}

    def derivar_matricula(self, partes):
        """
        Realiza la derivación por la izquierda de una matrícula de Brasil.
        :param partes: Diccionario con las partes de la matrícula (letras, numeros, letra).
        :return: Lista de pasos de la derivación.
        """
        derivacion = f"{partes['letras']}{partes['numeros'][0]}{partes['letra']}{''.join(partes['numeros'][1:])}"
        pasos = ["<matricula>", "<brasil>", "<letras3><digito><letra><digito><digito>"]

        # Sustituimos cada carácter progresivamente
        acumulado = ""
        for char in derivacion:
            acumulado += char
            pasos.append(acumulado)

        return pasos