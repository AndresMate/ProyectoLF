import re

class Chile:
    def __init__(self):
        self.nombre = "Chile"
        self.patron = re.compile(r'^[A-Z]{2}-[A-Z\d]{2} \d{2}$')  # Actualiza la expresión regular

    def validar_matricula(self, matricula):
        if self.patron.match(matricula):
            partes = {
                "matricula": matricula,
                "letras": matricula[:2],
                "caracteres": matricula[3:5],  # Ajusta los índices según el nuevo formato
                "numeros": matricula[6:]
            }
            return True, partes
        return False, {}

    def derivar_matricula(self, partes):
        # Derivación por la izquierda
        matricula = partes["matricula"]
        pasos = ["<matricula>", "<chile>", "<letras><caracteres><numeros>"]
        letras = matricula[:2]
        caracteres = matricula[3:5]  # Ajusta los índices según el nuevo formato
        numeros = matricula[6:]
        pasos.append(f"{letras}<caracteres><numeros>")
        for i in range(len(caracteres)):
            pasos.append(f"{letras}{caracteres[:i + 1]}<caracteres><numeros>")
        pasos[-1] = pasos[-1].replace("<caracteres>", f"{caracteres}")
        for i in range(len(numeros)):
            pasos.append(f"{letras}{caracteres}{numeros[:i + 1]}<numeros>")
        pasos[-1] = pasos[-1].replace("<numeros>", "")
        return pasos