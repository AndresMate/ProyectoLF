import re
from paises.pais import Pais

class Ecuador(Pais):
    def __init__(self):
        super().__init__("Ecuador")
        # Diccionario de provincias con su letra inicial
        self.provincias = {
            "A": "Azuay",
            "B": "Bolívar",
            "C": "Carchi",
            "G": "Guayas",
            "P": "Pichincha",
            "R": "Los Ríos",
            "S": "Santa Elena",
            "T": "Tungurahua",
            "Z": "Zamora Chinchipe",
        }

    def validar_matricula(self, matricula):
        # Validar formato: L###LLL (1 letra, 3 números, 3 letras)
        patron = r"^[A-Z]\d{3}[A-Z]{3}$"
        if re.match(patron, matricula):
            primer_caracter = matricula[0]  # Primer carácter identifica la provincia
            numeros = matricula[1:4]
            letras = matricula[4:]

            # Identificar la provincia por el primer carácter
            if primer_caracter in self.provincias:
                provincia = self.provincias[primer_caracter]
                return True, {
                    "matricula": matricula,
                    "provincia": provincia
                }
        return False, {}

    def derivar_matricula(self, partes):
        # Derivación por la izquierda
        matricula = partes["matricula"]
        pasos = ["<matricula>", "<ecuador>", "<provincia><numeros><letras>"]
        provincia = matricula[0]
        numeros = matricula[1:4]
        letras = matricula[4:]
        pasos.append(f"{provincia}<numeros><letras>")
        for i in range(len(numeros)):
            pasos.append(f"{provincia}{numeros[:i+1]}<numeros><letras>")
        pasos[-1] = pasos[-1].replace("<numeros>", f"{numeros}")
        for i in range(len(letras)):
            pasos.append(f"{provincia}{numeros}{letras[:i+1]}<letras>")
        pasos[-1] = pasos[-1].replace("<letras>", "")
        return pasos
