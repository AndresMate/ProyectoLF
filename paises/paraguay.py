import re

class Paraguay:
    def __init__(self):
        self.nombre = "Paraguay"
        self.lexico = "El análisis léxico de la matrícula nos indica que el formato es: Cuatro letras seguidas de un espacio y tres dígitos."
        self.patron = re.compile(r'^[A-Z]{4} \d{3}$')  # Updated regex pattern

    def validar_matricula(self, matricula):
        if self.patron.match(matricula):
            partes = {
                "matricula": matricula,
                "letras": matricula[:4],
                "numeros": matricula[4:]
            }
            return True, partes
        return False, {}

    def derivar_matricula(self, partes):
        # Derivación por la izquierda
        matricula = partes["matricula"]
        pasos = ["<matricula>", "<paraguay>", "<letras>< ><numeros>"]
        letras = matricula[:4]
        numeros = matricula[4:]
        pasos.append(f"{letras}<numeros>")
        for i in range(len(numeros)):
            pasos.append(f"{letras} {numeros[:i + 1]}<numeros>")
        pasos[-1] = pasos[-1].replace("<numeros>", "")
        return pasos