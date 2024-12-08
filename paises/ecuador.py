import re
from paises.pais import Pais

class Ecuador(Pais):
    def __init__(self):
        super().__init__("Ecuador")
        self.provincias = {
            "A": "Azuay",
            "B": "Bolívar",
            "U": "Cañar",
            "C": "Carchi",
            "X": "Cotopaxi",
            "H": "Chimborazo",
            "O": "El Oro",
            "E": "Esmeraldas",
            "Q": "Orellana",
            "W": "Galápagos",
            "G": "Guayas",
            "I": "Imbabura",
            "L": "Loja",
            "R": "Los Rios",
            "M": "Manabí",
            "V": "Morona Santiago",
            "N": "Napo",
            "S": "Pastaza",
            "P": "Pichincha",
            "Y": "Santa Elena",
            "J": "Santo Domingo de los Tsáchilas",
            "K": "Sucumbíos",
            "T": "Tungurahua",
            "Z": "Zamora Chinchipe",
        }
        self.segunda_letra_significado = {
            "Vehículos comerciales": ["A", "U", "Z"],
            "Vehículos gubernamentales": ["E"],
            "Vehículos de uso oficial": ["X"],
            "Gads regionales": ["M"],
        }

    def validar_matricula(self, matricula):
        patron = r"^[A-Z]{3}-\d{4}$"
        if re.match(patron, matricula):
            primer_caracter = matricula[0]
            segundo_caracter = matricula[1]
            numeros = matricula[4:]

            if primer_caracter in self.provincias:
                provincia = self.provincias[primer_caracter]
                significado_segunda_letra = "Vehículos Particulares"
                for significado, letras in self.segunda_letra_significado.items():
                    if segundo_caracter in letras:
                        significado_segunda_letra = significado
                        break
                return True, {
                    "matricula": matricula,
                    "provincia": provincia,
                    "servicio": significado_segunda_letra
                }
        return False, {}

    def derivar_matricula(self, partes):
        matricula = partes["matricula"]
        pasos = ["<matricula>", "<ecuador>", "<provincia><letras><numeros>"]
        provincia = matricula[0]
        letras = matricula[1:3]
        numeros = matricula[4:]
        pasos.append(f"{provincia}<letras><numeros>")
        for i in range(len(letras)):
            pasos.append(f"{provincia}{letras[:i + 1]}<letras><numeros>")
        pasos[-1] = pasos[-1].replace("<letras>", f"{letras}")
        for i in range(len(numeros)):
            pasos.append(f"{provincia}{letras}{numeros[:i + 1]}<numeros>")
        pasos[-1] = pasos[-1].replace("<numeros>", "")
        return pasos