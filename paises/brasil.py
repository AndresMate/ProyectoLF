import re
from paises.pais import Pais

class Brasil(Pais):
    def __init__(self):
        super().__init__("Brasil")
        # Rangos de letras asignados a cada estado
        self.ciudad = {
            "Acre": ("AAA", "BEZ"),
            "Alagoas": ("BFA", "CAZ"),
            "Amapá": ("CBA", "DAZ"),
            "Amazonas": ("DBA", "EAZ"),
            "Bahia": ("EBA", "GAZ"),
            "Ceará": ("GBA", "HAZ"),
            "Distrito Federal": ("HBA", "JAZ"),
            "Espírito Santo": ("JBA", "KAZ"),
            "Goiás": ("KBA", "LAZ"),
            "Maranhão": ("LBA", "MAZ"),
            "Mato Grosso": ("MBA", "NAZ"),
            "Mato Grosso do Sul": ("NBA", "OAZ"),
            "Minas Gerais": ("OBA", "PAZ"),
            "Pará": ("PBA", "QAZ"),
            "Paraíba": ("QBA", "RAZ"),
            "Paraná": ("RBA", "SAZ"),
            "Pernambuco": ("SBA", "TAZ"),
            "Piauí": ("TBA", "UAZ"),
            "Rio de Janeiro": ("UBA", "VAZ"),
            "Rio Grande do Norte": ("VBA", "WAZ"),
            "Rio Grande do Sul": ("WBA", "XAZ"),
            "Rondônia": ("XBA", "YAZ"),
            "Roraima": ("YBA", "ZAZ"),
            "Santa Catarina": ("ZBA", "ZHZ"),
            "São Paulo": ("ZIA", "ZZZ"),
            "Sergipe": ("ZJA", "ZQZ"),
            "Tocantins": ("ZRA", "ZZZ")
        }

    def validar_matricula(self, matricula):
        # Validar formato general de Brasil
        patron = r"^[A-Z]{3}\d[A-Z]\d{2}$"
        if re.match(patron, matricula):
            letras = matricula[:3]
            numeros = [matricula[3], matricula[5], matricula[6]]
            letra = matricula[4]

            # Verificar el estado según las letras iniciales
            for ciudad, (inicio, fin) in self.ciudad.items():
                if inicio <= letras <= fin:
                    return True, {
                        "matricula": matricula,
                        "letras": letras,
                        "numeros": numeros,
                        "letra": letra,
                        "ciudad": ciudad
                    }
        return False, {}

    def derivar_matricula(self, partes):
        # Derivación por la izquierda
        pasos = ["<matricula>", "<brasil>", "<letras3><digito><letra><digito><digito>"]
        pasos.append(f"{partes['letras']}{partes['numeros'][0]}<letra><digito><digito>")
        pasos.append(f"{partes['letras']}{partes['numeros'][0]}{partes['letra']}<digito><digito>")
        pasos.append(f"{partes['letras']}{partes['numeros'][0]}{partes['letra']}{partes['numeros'][1]}<digito>")
        pasos[-1] = f"{partes['letras']}{partes['numeros'][0]}{partes['letra']}{''.join(partes['numeros'][1:])}"
        return pasos
