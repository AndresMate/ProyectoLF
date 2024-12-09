import re
from paises.pais import Pais
from tkinter import Tk, StringVar, OptionMenu, Button

class Uruguay(Pais):
    def __init__(self):
        super().__init__("Uruguay")
        self.lexico = "El análisis léxico de la matrícula nos indica que el formato es: Una letra seguida de dos letras, un espacio y cuatro dígitos."
        self.regiones = {
            "A": ["Canelones"],
            "B": ["Maldonado"],
            "C": ["Rocha"],
            "D": ["Treinta y Tres"],
            "E": ["Cerro Largo"],
            "F": ["Rivera"],
            "G": ["Artigas"],
            "H": ["Salto"],
            "I": ["Paysandú"],
            "J": ["Río Negro"],
            "K": ["Soriano"],
            "L": ["Colonia"],
            "M": ["San José"],
            "N": ["Flores"],
            "O": ["Florida"],
            "P": ["Lavalleja"],
            "Q": ["Durazno"],
            "R": ["Tacuarembó"],
            "S": ["Montevideo"]
        }
        self.tipos_vehiculos = {
            ("Blanco", "Negro"): "Vehículos particulares",
            ("Blanco", "Rojo"): "Vehículos comerciales y de transporte público",
            ("Blanco", "Azul"): "Vehículos oficiales y gubernamentales",
            ("Amarillo", "Negro"): "Matrículas temporales"
        }

    def validar_matricula(self, matricula):
        patron = r"^[A-Z]{1}[A-Z]{2} \d{4}$"
        if re.match(patron, matricula):
            primer_caracter = matricula[0]
            letras = matricula[1:3]
            numeros = matricula[3:]

            # Identificar la región según el primer carácter
            if primer_caracter in self.regiones:
                departamentos = ", ".join(self.regiones[primer_caracter])

                # Crear ventana para seleccionar colores
                root = Tk()
                root.withdraw()  # Ocultar la ventana principal

                fondo_var = StringVar(root)
                fondo_var.set("Seleccione el color del fondo")
                caract_var = StringVar(root)
                caract_var.set("Seleccione el color de los caracteres")

                fondo_options = ["Blanco", "Amarillo"]
                caract_options = ["Negro", "Rojo", "Azul"]

                fondo_dropdown = OptionMenu(root, fondo_var, *fondo_options)
                fondo_dropdown.pack()

                caract_dropdown = OptionMenu(root, caract_var, *caract_options)
                caract_dropdown.pack()

                def on_select():
                    root.quit()

                select_button = Button(root, text="Seleccionar", command=on_select)
                select_button.pack()

                root.deiconify()  # Mostrar la ventana principal
                root.mainloop()

                fondo = fondo_var.get()
                caract = caract_var.get()
                tipo_vehiculo = self.tipos_vehiculos.get((fondo, caract), "Desconocido")

                return True, {
                    "matricula": matricula,
                    "region": primer_caracter,
                    "departamentos": departamentos,
                    "color_fondo": fondo,
                    "color_caracteres": caract,
                    "tipo_vehiculo": tipo_vehiculo
                }
        return False, {}

    def derivar_matricula(self, partes):
        matricula = partes["matricula"]
        pasos = ["<matricula>", "<uruguay>", "<region><letras><numeros>"]
        region = matricula[0]
        letras = matricula[1:3]
        numeros = matricula[3:]
        pasos.append(f"{region}<letras><numeros>")
        for i in range(len(letras)):
            pasos.append(f"{region}{letras[:i+1]}<letras><numeros>")
        pasos[-1] = pasos[-1].replace("<letras>", f"{letras}")
        for i in range(len(numeros)):
            pasos.append(f"{region}{letras} {numeros[:i+1]}<numeros>")
        pasos[-1] = pasos[-1].replace("<numeros>", "")
        return pasos
