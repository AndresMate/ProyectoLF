import re
from paises.pais import Pais
from tkinter import Tk, StringVar, OptionMenu, Button

class Brasil(Pais):
    def __init__(self):
        super().__init__("Brasil")
        # Rangos de letras asignados a cada estado
        self.ciudad = {
            "Acre": ("AAA", "BEZ"),
            "Alagoas": ("BFA", "CAZ"),
            "Amapá": ("CBA", "DAZ"),
            "Amazonas": ("DBA", "EAZ"),
            "Bahia": ("EBA", "GAZ"),
            "Ceará": ("GBA", "HAZ"),
            "Distrito Federal": ("HBA", "JAZ"),
            "Espírito Santo": ("JBA", "KAZ"),
            "Goiás": ("KBA", "LAZ"),
            "Maranhão": ("LBA", "MAZ"),
            "Mato Grosso": ("MBA", "NAZ"),
            "Mato Grosso do Sul": ("NBA", "OAZ"),
            "Minas Gerais": ("OBA", "PAZ"),
            "Pará": ("PBA", "QAZ"),
            "Paraíba": ("QBA", "RAZ"),
            "Paraná": ("RBA", "SAZ"),
            "Pernambuco": ("SBA", "TAZ"),
            "Piauí": ("TBA", "UAZ"),
            "Rio de Janeiro": ("UBA", "VAZ"),
            "Rio Grande do Norte": ("VBA", "WAZ"),
            "Rio Grande do Sul": ("WBA", "XAZ"),
            "Rondônia": ("XBA", "YAZ"),
            "Roraima": ("YBA", "ZAZ"),
            "Santa Catarina": ("ZBA", "ZHZ"),
            "São Paulo": ("ZIA", "ZZZ"),
            "Sergipe": ("ZJA", "ZQZ"),
            "Tocantins": ("ZRA", "ZZZ")
        }
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

            # Verificar el estado según las letras iniciales
            for ciudad, (inicio, fin) in self.ciudad.items():
                if inicio <= letras <= fin:
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
                        "ciudad": ciudad,
                        "tipo_vehiculo": tipo_vehiculo
                    }
        return False, {}

    def derivar_matricula(self, partes):
        # Derivación por la izquierda
        pasos = ["<matricula>", "<brasil>", "<letras3><digito><letra><digito><digito>",
                 f"{partes['letras']}{partes['numeros'][0]}<letra><digito><digito>",
                 f"{partes['letras']}{partes['numeros'][0]}{partes['letra']}<digito><digito>",
                 f"{partes['letras']}{partes['numeros'][0]}{partes['letra']}{''.join(partes['numeros'][1:])}"]
        pasos[-1] = pasos[-1].replace("<letra>", partes['letra'])
        return pasos