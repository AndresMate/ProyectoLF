import re
from paises.pais import Pais

class Costa(Pais):
    def __init__(self):
        super().__init__("Costa Rica")


        self.tipos = {
            "privados": r"^[B-Z]{3}-\d{4}$",
            "especiales": r"^(AB|SJB|C|CC|CD|CL|D|M|PE|TA|TSJ|VH) \d{5}$"
        }

    def validar_matricula(self, matricula):
        if re.match(self.tipos["privados"], matricula):
            letras, numeros = matricula.split("-")
            return True, {
                "tipo": "privados",
                "matricula": matricula,
                "letras": letras,
                "numeros": numeros
            }
        elif re.match(self.tipos["especiales"], matricula):
            tipo, numeros = matricula.split(" ")
            return True, {
                "tipo": "especiales",
                "matricula": matricula,
                "categoria": tipo,
                "numeros": numeros
            }
        return False, {}

    def derivar_matricula(self, partes):

        matricula = partes["matricula"]
        pasos = ["<matricula>"]
        if partes["tipo"] == "privados":
            letras, numeros = matricula.split("-")
            pasos.append("<privados>")
            pasos.append("<letras><separador><numeros>")
            for i in range(len(letras)):
                pasos.append(f"{letras[:i+1]}<letras><separador><numeros>")
            pasos[-1] = pasos[-1].replace("<letras>", letras)
            pasos.append(f"{letras}-<numeros>")
            for i in range(len(numeros)):
                pasos.append(f"{letras}-{numeros[:i+1]}<numeros>")
            pasos[-1] = pasos[-1].replace("<numeros>", numeros)
        elif partes["tipo"] == "especiales":
            tipo, numeros = matricula.split(" ")
            pasos.append("<especiales>")
            pasos.append("<categoria><espacio><numeros>")
            for i in range(len(tipo)):
                pasos.append(f"{tipo[:i+1]}<categoria><espacio><numeros>")
            pasos[-1] = pasos[-1].replace("<categoria>", tipo)
            pasos.append(f"{tipo} <numeros>")
            for i in range(len(numeros)):
                pasos.append(f"{tipo} {numeros[:i+1]}<numeros>")
            pasos[-1] = pasos[-1].replace("<numeros>", numeros)
        return pasos