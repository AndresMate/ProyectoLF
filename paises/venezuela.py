import re
from paises.pais import Pais

class Venezuela(Pais):
    def __init__(self):
        super().__init__("Venezuela")

        self.regiones = {
            "A": "Distrito Capital",
            "B": "Anzoátegui",
            "C": "Apure",
            "D": "Aragua",
            "E": "Barinas",
            "F": "Bolivar",
            "G": "Carabobo",
            "H": "Cojedes",
            "I": "Falcón",
            "J": "Guárico",
            "K": "Lara",
            "L": "Mérida",
            "M": "Miranda",
            "N": "Monagas",
            "O": "Nueva Esparta",
            "P": "Portuguesa",
            "R": "Sucre",
            "S": "Táchira",
            "T": "Trujillo",
            "U": "Yaracuy",
            "V": "Zulia",
            "W": "La Guaira",
            "X": "Amazonas",
            "Y": "Delta Amacuro"
        }

        self.tipos_vehiculo = {
            "Automóviles particulares": r"^[A-Z]{2}\d{3}[A-Z]{1}[A-Z]{1}$",
            "Transporte público urbano": r"^01[A-Z]{2}\d{2}[A-Z]{1}$",
            "Transporte público suburbano": r"^31[A-Z]{2}\d{2}[A-Z]{1}$",
            "Taxis": r"^7[A-Z]\d[A-Z]\d[A-Z]{1}$",
            "Transporte público interurbano": r"^6123[A-Z]\d[A-Z]{1}$"
        }

    def validar_matricula(self, matricula):

        for tipo, patron in self.tipos_vehiculo.items():
            if re.match(patron, matricula):
                region = matricula[-1]
                if region in self.regiones:
                    return True, {
                        "matricula": matricula,
                        "tipo": tipo,
                        "region": region,
                        "estado": self.regiones[region]
                    }
        return False, {}

    def derivar_matricula(self, partes):

        matricula = partes["matricula"]
        tipo = partes["tipo"]
        region = matricula[-1]
        pasos = [f"<{tipo}>", f"<{matricula}>"]

        if tipo == "Automóviles particulares":
            pasos.append(f"<{matricula[:2]}><{matricula[2:5]}><{matricula[5:6]}><{region}>")
        elif tipo == "Transporte público urbano":
            pasos.append(f"<01><{matricula[2:4]}><{matricula[4:6]}><{region}>")
        elif tipo == "Transporte público suburbano":
            pasos.append(f"<31><{matricula[2:4]}><{matricula[4:6]}><{region}>")
        elif tipo == "Taxis":
            pasos.append(f"<7><{matricula[1]}><{matricula[2]}><{matricula[3]}><{region}>")
        elif tipo == "Transporte público interurbano":
            pasos.append(f"<6123><{matricula[4]}><{matricula[5]}><{region}>")

        return pasos
