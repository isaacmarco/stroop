import json
from Item import Item, Colores
from corrector import Corrector
from reconocimiento import ReconocimientoVoz

# crear items de debug
items = [
    Item(0, Colores.ROJO), Item(1, Colores.VERDE)#, Item(2, Colores.AZUL),

]
'''
   Item(3, Colores.AMARILLO),
   Item(4, Colores.ROJO), Item(5, Colores.VERDE), Item(6, Colores.AZUL), Item(7, Colores.AMARILLO),
   Item(8, Colores.ROJO), Item(9, Colores.VERDE), Item(10, Colores.AZUL), Item(11, Colores.AMARILLO),
   Item(12, Colores.ROJO), Item(13, Colores.VERDE), Item(14, Colores.AZUL), Item(15, Colores.AMARILLO),
   '''
# reconocemos el audio de cada item
reconocimiento_voz = ReconocimientoVoz("c:/vosk/vosk-model-small-es-0.42")
for i, item in enumerate(items):
    # abrimos el wav
    fichero = f'recordings/item{i}.wav'
    print(f'Procesando item {fichero}')
    # obtenemos las palabras reconocidas en ese item
    palabras = reconocimiento_voz.reconocer(fichero)

    item.palabras_reconocidas = palabras


# corregimos los items
corrector = Corrector(items)
corrector.corregir()
# convertir la lista de items en un diccionario
diccionario = [
    {
        'id': item.id,
        'color': item.color,
        'respuesta': item.respuesta,
        'correccion': item.correccion,
        'palabras': [p.to_dict() for p in item.palabras_reconocidas],
    } for item in items
]

json = json.dumps({'correccion' : diccionario}, indent=2)
with open('correcciones/correccion.json', 'w', encoding='utf-8') as f:
    f.write(json)
