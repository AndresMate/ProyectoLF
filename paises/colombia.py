import pandas as pd
import re

def cargar_rangos(archivo_excel):
    data = pd.read_excel(archivo_excel, engine="openpyxl")
    rangos = {}
    for _, row in data.iterrows():
        rango_inicial = str(row["RANGO"]) if not pd.isna(row["RANGO"]) else "ZZZ999"
        rango_final = str(row["Unnamed: 1"]) if not pd.isna(row["Unnamed: 1"]) else "ZZZ999"
        departamento = row["LOCALIZACION"]
        ciudad = row["Unnamed: 3"]
        servicio = row["SERVICIO"]

        if pd.isna(departamento):
            departamento = "Desconocido"
        if pd.isna(ciudad):
            ciudad = "No disponible"
        if pd.isna(servicio):
            servicio = "No disponible"

        if departamento not in rangos:
            rangos[departamento] = []
        rangos[departamento].append((rango_inicial, rango_final, ciudad, servicio))

    return rangos

class Colombia:
    def __init__(self, archivo_excel):
        self.nombre = "Colombia"
        self.lexico = "El análisis léxico de la matrícula nos indica que el formato es: Tres letras en mayúscula seguidas de un espacio y tres números."
        self.rangos_departamentos = cargar_rangos(archivo_excel)

    def validar_matricula(self, matricula):
        patron = r"^[A-Z]{3} \d{3}$"
        if re.match(patron, matricula):
            prefijo = matricula[:6]
            for departamento, rangos in self.rangos_departamentos.items():
                for inicio, fin, ciudad, servicio in rangos:
                    if inicio <= prefijo <= fin:
                        return True, {
                            "matricula": matricula,
                            "departamento": departamento,
                            "ciudad": ciudad,
                            "servicio": servicio
                        }
            # If not found in Excel, still return valid
            return True, {
                "matricula": matricula,
                "departamento": "Desconocido",
                "ciudad": "No disponible",
                "servicio": "No disponible"
            }
        return False, {}

    @staticmethod
    def derivar_matricula(partes):
        matricula = partes["matricula"]
        pasos = ["<matricula>", "<colombia>", "<prefijo><numeros>"]
        prefijo = matricula[:3]
        numeros = matricula[3:]
        pasos.append(f"{prefijo}<numeros>")
        for i in range(len(numeros)):
            pasos.append(f"{prefijo}{numeros[:i + 1]}<numeros>")
        pasos[-1] = pasos[-1].replace("<numeros>", "")
        return pasos