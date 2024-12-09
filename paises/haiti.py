import re
from paises.pais import Pais

class Haiti(Pais):
    def __init__(self):
        super().__init__("Haiti")
        self.lexico = "El análisis léxico de la matrícula nos indica que el formato es: Dos letras seguidas de un espacio y cinco dígitos."
        self.patron = re.compile(r'^[A-Z]{2} \d{5}$')  # Regex pattern for the license plate format

    def validar_matricula(self, matricula):
        if self.patron.match(matricula):
            letras = matricula[:2]
            if letras[0] == letras[1]:  # Check if the first two letters are the same
                partes = {
                    "matricula": matricula,
                    "letras": letras,
                    "numeros": matricula[2:]
                }
                return True, partes
        return False, {}

    def derivar_matricula(self, partes):
        # Derivación por la izquierda
        matricula = partes["matricula"]
        pasos = ["<matricula>", "<haiti>", "<letras><numeros>"]
        letras = partes["letras"]
        numeros = partes["numeros"]
        pasos.append(f"{letras}<numeros>")
        for i in range(len(numeros)):
            pasos.append(f"{letras}{numeros[:i + 1]}<numeros>")
        pasos[-1] = pasos[-1].replace("<numeros>", "")
        return pasos