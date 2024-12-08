import re
from paises.pais import Pais


class Mexico(Pais):
    def __init__(self):
        super().__init__("México")
        self.regiones = {
            "Aguascalientes": ("AAA", "AFZ"),
            "Baja California": ("AGA", "CYZ"),
            "Baja California Sur": ("CZA", "DEZ"),
            "Campeche": ("DFA", "DKZ"),
            "Chihuahua": ("DTA", "ETZ"),
            "Chiapas": ("DLA", "DSZ"),
            "Ciudad de México": ("A01", "Z99"),
            "Coahuila": ("EUA", "FPZ"),
            "Colima": ("FRA", "FWZ"),
            "Durango": ("FXA", "GFZ"),
            "Guanajuato": ("GGA", "GYZ"),
            "Guerrero": ("GZA", "HFZ"),
            "Hidalgo": ("HGA", "HRZ"),
            "Jalisco": ("HSA", "LFZ"),
            "Estado de México": ("LGA", "PEZ"),
            "Michoacán": ("PFA", "PUZ"),
            "Morelos": ("PVA", "RDZ"),
            "Nayarit": ("REA", "RJZ"),
            "Nuevo León": ("RKA", "TGZ"),
            "Oaxaca": ("THA", "TMZ"),
            "Puebla": ("TNA", "UJZ"),
            "Querétaro": ("UKA", "UPZ"),
            "Quintana Roo": ("URA", "UVZ"),
            "San Luis Potosí": ("UWA", "VEZ"),
            "Sinaloa": ("VFA", "VSZ"),
            "Sonora": ("VTA", "WKZ"),
            "Tabasco": ("WLA", "WWZ"),
            "Tamaulipas": ("WXA", "XSZ"),
            "Tlaxcala": ("XTA", "XXZ"),
            "Veracruz": ("XYA", "YVZ"),
            "Yucatán": ("YWA", "ZCZ"),
            "Zacatecas": ("ZDA", "ZHZ")
        }

        self.tipos_matricula = {
            "Transportes privados (Distrito Federal)": r"^[A-Z]\d{2}-[A-Z]{3}$",
            "Transportes privados (Entidades Federales)": r"^[A-Z]{3}-\d{3}-[A-Z]$",
            "Público local (Distrito Federal)": r"^[A-Z]-\d{4}-[A-Z]$|^\d{3}-[A-Z]-\d{3}$|^\d{3}-\d{3}$",
            "Público local (Entidades Federales)": r"^[A-Z]-\d{3}-[A-Z]{3}$|^[A-Z]-\d{5}-[A-Z]$"
        }

    def validar_matricula(self, matricula):

        for tipo, patron in self.tipos_matricula.items():
            if re.match(patron, matricula):
                for estado, (inicio, fin) in self.regiones.items():
                    if inicio <= matricula[:3] <= fin:
                        return True, {
                            "matricula": matricula,
                            "tipo": tipo,
                            "estado": estado
                        }
        return False, {}

    def derivar_matricula(self, partes):
        matricula = partes["matricula"]
        tipo = partes["tipo"]
        estado = partes["estado"]
        pasos = [f"<{tipo}>", f"<{matricula}>", f"<{estado}>"]

        if tipo.startswith("Transportes privados"):
            pasos.append(f"<{matricula[:3]}><{matricula[3:6]}><{matricula[6:]}>")
        elif "Público local" in tipo:
            if len(matricula.split("-")[0]) == 1:  # A-000-AAA
                pasos.append(f"<{matricula[0]}><{matricula[2:5]}><{matricula[6:]}>")
            else:  # 000-000
                partes = matricula.split("-")
                pasos.append(f"<{partes[0]}><{partes[1]}>")

        return pasos
