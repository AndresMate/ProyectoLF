import re
from paises.pais import Pais

class Bolivia(Pais):
    def __init__(self):
        super().__init__("Bolivia")

        self.regiones = {
            "B": ["Beni"],
            "C": ["Cochabamba"],
            "H": ["Chuquisaca"],
            "L": ["La Paz"],
            "N": ["Pando"],
            "O": ["Oruro"],
            "P": ["Potosí"],
            "S": ["Santa Cruz"],
            "T": ["Tarija"]
        }

    def validar_matricula(self, matricula):

        patron = r"^[A-Z]\d{3}[A-Z]{3}$"
        if re.match(patron, matricula):
            primer_caracter = matricula[0]  # El primer carácter identifica la región
            numeros = matricula[1:4]
            letras = matricula[4:]

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
        pasos = ["<matricula>", "<bolivia>", "<region><numeros><letras>"]
        region = matricula[0]
        numeros = matricula[1:4]
        letras = matricula[4:]
        pasos.append(f"{region}<numeros><letras>")
        for i in range(len(numeros)):
            pasos.append(f"{region}{numeros[:i+1]}<numeros><letras>")
        pasos[-1] = pasos[-1].replace("<numeros>", f"{numeros}")
        for i in range(len(letras)):
            pasos.append(f"{region}{numeros}{letras[:i+1]}<letras>")
        pasos[-1] = pasos[-1].replace("<letras>", "")
        return pasos
