from Item import Correccion, Colores


class Corrector:

    def __init__(self, items):
       self.items = items

    def corregir(self):

        print('Realizando correccion')

        for item in self.items:

            if not item.palabras_reconocidas:
                # no hay respuesta, indicamos el item como sin definir
                item.correccion = str(Correccion.SIN_DEFINIR)
                continue

            correcciones = {
                'rojo': Colores.ROJO,
                'verde': Colores.VERDE,
                'azul': Colores.AZUL,
                'amarillo': Colores.AMARILLO,
            }

            # aunque se hayan detectado varias palabras correctas, por como es la tarea
            # debemos quedarnos con la primera respuesta (la no inhibida)
            palabra_respuesta = item.palabras_reconocidas[0].palabra

            # comprobar si existe en el diccionario de correcciones
            if not palabra_respuesta in correcciones:
                continue

            # guardamos la respuesta en el item como un enum
            item.respuesta = str(correcciones[palabra_respuesta])

            # comprobar si es correcta (los colores coinciden)
            if item.respuesta == item.color:
                item.correccion = str(Correccion.CORRECTA)
            else:
                item.correccion = str(Correccion.INCORRECTA)
