import re
from paises.pais import Pais

class Uruguay(Pais):
    def __init__(self):
        super().__init__("Uruguay")
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

    def validar_matricula(self, matricula):
        patron = r"^[A-Z]{1}[A-Z]{2} \d{4}$"
        if re.match(patron, matricula):
            primer_caracter = matricula[0]
            letras = matricula[1:3]
            numeros = matricula[3:]

            # Identificar la región según el primer carácter
            if primer_caracter in self.regiones:
                departamentos = ", ".join(self.regiones[primer_caracter])
                return True, {
                    "matricula": matricula,
                    "region": primer_caracter,
                    "departamentos": departamentos
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
