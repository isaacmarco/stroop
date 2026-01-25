from vosk import Model, KaldiRecognizer
from vosk import SetLogLevel
from palabra_reconocida import PalabraReconocida
import json
import wave


class ReconocimientoVoz:

    def __init__(self, ruta_modelo):
        print('Cargando modelo')
        self.palabras_reconocidas = []
        self.ruta_modelo = ruta_modelo
        self.modelo = self.__cargar_modelo()
        SetLogLevel(-1)  # reduce el nivel de log de VOSK

    def __cargar_modelo(self):
        return Model(self.ruta_modelo)

    def obtener_informacion_palabras(self, res):
        # creamos un objeto con informacion sobre cada palabra reconocida
        if "result" in res:
            for palabra in res["result"]:
                obj = PalabraReconocida(
                    palabra=palabra["word"],
                    inicio=palabra["start"],
                    fin=palabra["end"],
                )
                self.palabras_reconocidas.append(obj)

    def reconocer(self, wav):
        # limpiamos el reconocimiento anterior
        self.palabras_reconocidas = []
        # se intenta reconocer la lista de palabras en el wav
        gramatica = json.dumps(['rojo', 'verde', 'azul', 'amarillo'])
        wf = wave.open(wav, "rb")
        # comprobar que es un wav mono a 16khz
        assert wf.getnchannels() == 1
        assert wf.getframerate() == 16000
        # hacer el reconocimiento
        rec = KaldiRecognizer(self.modelo, wf.getframerate(), gramatica)
        rec.SetWords(True)
        # Procesar audio para obtener las palabras
        while True:
            data = wf.readframes(4000)
            if len(data) == 0:
                break
            if rec.AcceptWaveform(data):
                self.obtener_informacion_palabras(json.loads(rec.Result()))
        # Procesar la informacion pendiente
        self.obtener_informacion_palabras(json.loads(rec.FinalResult()))
        wf.close()
        return self.palabras_reconocidas

