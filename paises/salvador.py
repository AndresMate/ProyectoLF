import re
from paises.pais import Pais

class Salvador(Pais):
    def __init__(self):
        super().__init__("El Salvador")
        self.patron = re.compile(r'^[A-Z]{1,2}\d{3} \d{3}$')
        self.tipos_vehiculos = {
            "A": "Alquiler",
            "AB": "Autobús",
            "C": "Camión",
            "D": "Discapacitados",
            "E": "Ejército",
            "F": "Furgoneta",
            "M": "Motos",
            "N": "Nacional",
            "O": "Oficial",
            "P": "Particular",
            "T": "Trailer",
            "V": "Vendedor"
        }

    def validar_matricula(self, matricula):
        if self.patron.match(matricula):
            letras = matricula[0]
            if letras in self.tipos_vehiculos:
                partes = {
                    "matricula": matricula,
                    "letras": letras,
                    "numeros": matricula[1:],
                    "tipo_vehiculo": self.tipos_vehiculos[letras]
                }
                return True, partes
        return False, {}


    def derivar_matricula(self, partes):
        # Derivación por la izquierda
        matricula = partes["matricula"]
        pasos = ["<matricula>", "<el salvador>", "<letra><numeros>"]
        letras = partes["letras"]
        numeros = partes["numeros"]
        pasos.append(f"{letras}<numeros>")
        for i in range(len(numeros)):
            pasos.append(f"{letras}{numeros[:i + 1]}<numeros>")
        pasos[-1] = pasos[-1].replace("<numeros>", "")
        return pasos