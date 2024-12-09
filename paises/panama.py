import re
from paises.pais import Pais

class Panama(Pais):
    def __init__(self):
        super().__init__("Panamá")
        self.lexico = "El análisis léxico de la matrícula nos indica que el formato es: Seis dígitos o dos letras seguidas de cuatro dígitos."
        self.formatos = {
            "numerico": r"^\d{6}$",
            "alfanumerico": r"^[A-Z]{2}\d{4}$"
        }

    def validar_matricula(self, matricula):
        if re.match(self.formatos["numerico"], matricula):
            return True, {
                "tipo": "numerico",
                "matricula": matricula,
                "numeros": matricula
            }
        elif re.match(self.formatos["alfanumerico"], matricula):
            letras = matricula[:2]
            numeros = matricula[2:]
            return True, {
                "tipo": "alfanumerico",
                "matricula": matricula,
                "letras": letras,
                "numeros": numeros
            }
        return False, {}

    def derivar_matricula(self, partes):
        matricula = partes["matricula"]
        pasos = ["<matricula>"]
        if partes["tipo"] == "numerico":
            pasos.append("<numerico>")
            pasos.append("<numeros>")
            for i in range(1, len(matricula) + 1):
                pasos.append(f"{matricula[:i]}<numeros>")
            pasos[-1] = pasos[-1].replace("<numeros>", "")
        elif partes["tipo"] == "alfanumerico":
            letras = matricula[:2]
            numeros = matricula[2:]
            pasos.append("<alfanumerico>")
            pasos.append("<letras><numeros>")
            for i in range(len(letras)):
                pasos.append(f"{letras[:i+1]}<letras><numeros>")
            pasos[-1] = pasos[-1].replace("<letras>", letras)
            pasos.append(f"{letras}<numeros>")
            for i in range(len(numeros)):
                pasos.append(f"{letras}{numeros[:i+1]}<numeros>")
            pasos[-1] = pasos[-1].replace("<numeros>", "")
        return pasos
