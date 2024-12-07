import re
from paises.pais import Pais

class Peru(Pais):
    def __init__(self):
        super().__init__("Perú")
        self.regiones = {
            "P": ["Tumbes", "Piura"],
            "M": ["Lambayeque", "Cajamarca", "Amazonas"],
            "S": ["San Martín"],
            "L": ["Loreto"],
            "T": ["La Libertad"],
            "U": ["Ucayali"],
            "H": ["Ancash"],
            "W": ["Junín", "Huánuco", "Pasco"],
            "A": ["Lima"], "B": ["Lima"], "C": ["Lima"], "D": ["Lima"], "F": ["Lima"],
            "X": ["Cusco", "Apurímac", "Madre de Dios"],
            "Y": ["Ica", "Ayacucho", "Huancavelica"],
            "V": ["Arequipa"],
            "Z": ["Moquegua", "Tacna", "Puno"]
        }
        self.tipos_vehiculos = {
            r"^[A-Z]\d[A-Z]-\d{3}$": "Vehículo público",
            r"^[A-Z]{2}\d-\d{3}$": "Vehículo gubernamental",
            r"^[A-Z]{3}-\d{3}$": "Vehículo particular"
        }

    def validar_matricula(self, matricula):
        for patron, tipo in self.tipos_vehiculos.items():
            if re.match(patron, matricula):
                region = matricula[0]
                if region in self.regiones:
                    departamentos = ", ".join(self.regiones[region])
                    return True, {
                        "matricula": matricula,
                        "region": region,
                        "departamentos": departamentos,
                        "servicio": tipo
                    }
        return False, {}

    def derivar_matricula(self, partes):
        matricula = partes["matricula"]
        pasos = ["<matricula>", "<peru>", "<region><numeros><letras>"]
        region = matricula[0]
        numeros = matricula[1:4]
        letras = matricula[4:]
        pasos.append(f"{region}<numeros><letras>")
        for i in range(len(numeros)):
            pasos.append(f"{region}{numeros[:i+1]}<numeros><letras>")
        pasos[-1] = pasos[-1].replace("<numeros>", f"{numeros}")
        for i in range(len(letras)):
            pasos.append(f"{region}{numeros}{letras[:i+1]}<letras>")
        pasos[-1] = pasos[-1].replace("<letras>", "")
        return pasos