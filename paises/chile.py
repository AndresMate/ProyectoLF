import re

class Chile:
    def __init__(self):
        self.nombre = "Chile"
        self.letras_permitidas = "BCDFGHJKLPRSTVWXYZ"
        self.patron = re.compile(r'^[BCDFGHJKLPRSTVWXYZ]{2}-[BCDFGHJKLPRSTVWXYZ]{2} \d{2}$')

    def validar_matricula(self, matricula):
        if self.patron.match(matricula):
            partes = {
                "matricula": matricula,
                "letras1": matricula[:2],
                "letras2": matricula[3:5],
                "numeros": matricula[6:]
            }
            return True, partes
        return False, {}

    def derivar_matricula(self, partes):
        # Derivación por la izquierda
        matricula = partes["matricula"]
        pasos = ["<matricula>", "<chile>", "<letras1><letras2><numeros>"]
        letras1 = partes["letras1"]
        letras2 = partes["letras2"]
        numeros = partes["numeros"]
        pasos.append(f"{letras1}<letras2><numeros>")
        for i in range(len(letras2)):
            pasos.append(f"{letras1}{letras2[:i + 1]}<letras2><numeros>")
        pasos[-1] = pasos[-1].replace("<letras2>", f"{letras2}")
        for i in range(len(numeros)):
            pasos.append(f"{letras1}{letras2}{numeros[:i + 1]}<numeros>")
        pasos[-1] = pasos[-1].replace("<numeros>", "")
        return pasos