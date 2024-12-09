import re
from paises.pais import Pais

class Argentina(Pais):
    def __init__(self):
        super().__init__("Argentina")



    def validar_matricula(self, matricula):
        # Validar formato general de Argentina sin guiones
        patron = r"^[A-Z]{2} \d{3} [A-Z]{2}$"
        if re.match(patron, matricula):
            letras_inicio = matricula[:2]
            numeros = list(matricula[2:5])
            letras_final = matricula[5:]

            # No identificar la provincia según las letras iniciales
            return True, {
                "letras_inicio": letras_inicio,
                "numeros": numeros,
                "letras_final": letras_final
            }
        return False, {}


    def derivar_matricula(self, partes):
        """
        Realiza la derivación por la izquierda de una matrícula de Argentina.
        :param partes: Diccionario con las partes de la matrícula (letras_inicio, numeros, letras_final).
        :return: Lista de pasos de la derivación.
        """
        derivacion = f"{partes['letras_inicio']}{''.join(partes['numeros'])}{partes['letras_final']}"
        pasos = ["<matricula>", "<argentina>", "<letras2><numeros><letras2>"]

        # Sustituimos cada carácter progresivamente
        acumulado = ""
        for char in derivacion:
            acumulado += char
            pasos.append(acumulado)

        return pasos