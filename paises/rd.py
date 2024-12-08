import re
from paises.pais import Pais

class Rd(Pais):
    def __init__(self):
        super().__init__("República Dominicana")
        self.patron = re.compile(r'^[A-Z] \d{6}$')  # Regex pattern for the license plate format
        self.tipos_vehiculos = {
            "A": "Automóvil privado",
            "B": "Automóvil interurbano público",
            "C": "Automóvil turístico",
            "D": "Autobús público urbano",
            "F": "Remolque",
            "G": "Jeep",
            "H": "Ambulancia",
            "I": "Autobús privado",
            "J": "Montacargas",
            "L": "Carga",
            "M": "Carro fúnebre",
            "R": "Autobús público interurbano",
            "S": "Volteo",
            "T": "Automóvil público urbano",
            "U": "Máquinas pesadas",
            "P": "Autobús turístico"
        }

    def validar_matricula(self, matricula):
        if self.patron.match(matricula):
            letra = matricula[0]
            if letra in self.tipos_vehiculos:
                partes = {
                    "matricula": matricula,
                    "letra": letra,
                    "numeros": matricula[2:],
                    "tipo_vehiculo": self.tipos_vehiculos[letra]
                }
                return True, partes
        return False, {}

    def derivar_matricula(self, partes):
        # Derivación por la izquierda
        matricula = partes["matricula"]
        pasos = ["<matricula>", "<republicadominicana>", "<letra><numeros>"]
        letra = matricula[0]
        numeros = matricula[2:]
        pasos.append(f"{letra}<numeros>")
        for i in range(len(numeros)):
            pasos.append(f"{letra}{numeros[:i + 1]}<numeros>")
        pasos[-1] = pasos[-1].replace("<numeros>", "")
        return pasos