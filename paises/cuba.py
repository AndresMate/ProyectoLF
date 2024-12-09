import re
from paises.pais import Pais

class Cuba(Pais):
    def __init__(self):
        super().__init__("Cuba")
        self.patron_vehiculos = re.compile(r'^[A-Z] \d{3} \d{3}$')
        self.tipos_vehiculos = {
            "A": "Oficial",
            "C": "Diplomático",
            "D": "Diplomático",
            "E": "Diplomático",
            "K": "Extranjeros",
            "F": "FAR",
            "M": "MININT",
            "T": "Turismo"
        }

    def validar_matricula(self, matricula):
        if self.patron_vehiculos.match(matricula):
            letra = matricula[0]
            if letra in self.tipos_vehiculos:
                tipo_vehiculo = self.tipos_vehiculos[letra]
            else:
                tipo_vehiculo = "General"
            partes = {
                "matricula": matricula,
                "letra": letra,
                "numeros": matricula[1:],
                "tipo_vehiculo": tipo_vehiculo
            }
            return True, partes
        return False, {}

    def derivar_matricula(self, partes):
        # Derivación por la izquierda
        matricula = partes["matricula"]
        pasos = ["<matricula>", "<cuba>", "<letra><numeros>"]
        letra = partes["letra"]
        numeros = partes["numeros"]
        pasos.append(f"{letra}<numeros>")
        for i in range(len(numeros)):
            pasos.append(f"{letra}{numeros[:i + 1]}<numeros>")
        pasos[-1] = pasos[-1].replace("<numeros>", "")
        return pasos