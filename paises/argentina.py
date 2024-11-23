import re
from paises.pais import Pais

class Argentina(Pais):
    def __init__(self):
        super().__init__("Argentina")
        # Diccionario de provincias y sus rangos de letras iniciales
        self.provincias = {
            "Buenos Aires": ["AA", "AB", "AC", "AD"],
            "CABA": ["BA"],
            "Córdoba": ["EA", "EB", "EC"],
            "Santa Fe": ["FA", "FB", "FC"],
            "Mendoza": ["GA", "GB"],
            "Entre Ríos": ["HA", "HB"],
            "Salta": ["JA", "JB"],
            "Chaco": ["KA", "KB"],
            "Tucumán": ["LA", "LB"],
            "Misiones": ["MA", "MB"],
            "Corrientes": ["NA", "NB"],
            "San Juan": ["PA", "PB"],
            "San Luis": ["QA", "QB"],
            "Catamarca": ["RA", "RB"],
            "Jujuy": ["SA", "SB"],
            "Neuquén": ["TA", "TB"],
            "Río Negro": ["UA", "UB"],
            "Chubut": ["VA", "VB"],
            "Santa Cruz": ["WA", "WB"],
            "Tierra del Fuego": ["XA", "XB"]
        }

    def validar_matricula(self, matricula):
        # Validar formato general de Argentina
        patron = r"^[A-Z]{2}-\d{3}-[A-Z]{2}$"
        if re.match(patron, matricula):
            letras_inicio = matricula[:2]
            numeros = list(matricula[3:6])
            letras_final = matricula[7:]

            # Identificar la provincia según las letras iniciales
            for provincia, codigos in self.provincias.items():
                if letras_inicio in codigos:
                    return True, {
                        "letras_inicio": letras_inicio,
                        "numeros": numeros,
                        "letras_final": letras_final,
                        "provincia": provincia
                    }
        return False, {}

    def derivar_matricula(self, partes):
        # Derivación por la izquierda
        pasos = ["<matricula>", "<argentina>", "<letras2>-<numeros>-<letras2>"]
        pasos.append(f"{partes['letras_inicio']}-<numeros>-{partes['letras_final']}")
        for i, digito in enumerate(partes["numeros"]):
            pasos.append(f"{partes['letras_inicio']}-{''.join(partes['numeros'][:i + 1])}<numeros>-{partes['letras_final']}")
        pasos[-1] = pasos[-1].replace("<numeros>", "")
        return pasos
