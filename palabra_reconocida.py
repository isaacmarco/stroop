class PalabraReconocida:

    def __init__(self, palabra, inicio, fin):
        self.palabra = palabra
        self.inicio = inicio
        self.fin = fin

    def to_dict(self):
        return {
            "palabra": self.palabra,
            "inicio": self.inicio,
            "fin": self.fin,
        }

    def __str__(self):
        return f'{self.palabra} {self.inicio} - {self.fin}'