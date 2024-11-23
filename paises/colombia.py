import pandas as pd
import re

def cargar_rangos(archivo_excel):
    # Leer el archivo Excel
    data = pd.read_excel(archivo_excel, engine="openpyxl")
    rangos = {}

    # Procesar cada fila del archivo
    for _, row in data.iterrows():
        rango_inicial = str(row["RANGO"]) if not pd.isna(row["RANGO"]) else "ZZZ999"
        rango_final = str(row["Unnamed: 1"]) if not pd.isna(row["Unnamed: 1"]) else "ZZZ999"
        departamento = row["LOCALIZACION"]  # Columna del departamento
        ciudad = row["Unnamed: 3"]  # Columna de la ciudad
        servicio = row["SERVICIO"]  # Columna del servicio

        # Manejar valores nulos en las columnas
        if pd.isna(departamento):
            departamento = "Desconocido"
        if pd.isna(ciudad):
            ciudad = "No disponible"
        if pd.isna(servicio):
            servicio = "No disponible"

        # Registrar los rangos en el diccionario
        if departamento not in rangos:
            rangos[departamento] = []
        rangos[departamento].append((rango_inicial, rango_final, ciudad, servicio))

    return rangos

def derivar_matricula(partes):
    # Derivación por la izquierda para Colombia
    matricula = partes["matricula"]
    pasos = ["<matricula>", "<colombia>", "<prefijo><numeros>"]
    prefijo = matricula[:3]
    numeros = matricula[3:]
    pasos.append(f"{prefijo}<numeros>")
    for i in range(len(numeros)):
        pasos.append(f"{prefijo}{numeros[:i+1]}<numeros>")
    pasos[-1] = pasos[-1].replace("<numeros>", "")
    return pasos

class Colombia:
    def __init__(self, archivo_excel):
        self.nombre = "Colombia"
        self.rangos_departamentos = cargar_rangos(archivo_excel)

    def validar_matricula(self, matricula):
        # Validar formato general de Colombia
        patron = r"^[A-Z]{3}\d{3}$"
        if re.match(patron, matricula):
            prefijo = matricula[:6]  # Las primeras 6 posiciones identifican el rango
            for departamento, rangos in self.rangos_departamentos.items():
                for inicio, fin, ciudad, servicio in rangos:
                    if inicio <= prefijo <= fin:
                        return True, {
                            "matricula": matricula,
                            "departamento": departamento,
                            "ciudad": ciudad,
                            "servicio": servicio
                        }
        return False, {}