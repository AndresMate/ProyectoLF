
class Pais:
    def __init__(self, nombre):
        self.nombre = nombre

    def validar_matricula(self, matricula):
        raise NotImplementedError("Este método debe implementarse en las subclases.")

    def derivar_matricula(self, partes):
        raise NotImplementedError("Este método debe implementarse en las subclases.")
