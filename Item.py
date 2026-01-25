from enum import Enum

class Colores(Enum):
    ROJO = 0
    VERDE = 1
    AZUL = 2
    AMARILLO = 3

class Correccion(Enum):
    CORRECTA    = 0
    INCORRECTA  = 1
    SIN_DEFINIR = 2

class Item:
    def __init__(self, color):
        self.color = str(color)
        self.correccion = str(Correccion.SIN_DEFINIR)
        self.respuesta = str(Correccion.SIN_DEFINIR)
        self.palabras_reconocidas = []
