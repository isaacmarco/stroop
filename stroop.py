from psychopy import visual, core, event
from psychopy.sound import microphone
import random
import os
import soundfile as sf
import numpy as np
from scipy.signal import resample_poly

# =====================
# SETUP
# =====================
win = visual.Window(size=(800,600), color="black")
stim = visual.TextStim(win, text="", height=0.15)
fix = visual.TextStim(win, text="+", height=0.2, color="white")

condiciones = [
    ("ROJO", "red"),
    ("VERDE", "green"),
    ("AZUL", "blue"),
    ("AMARILLO", "yellow")
]

# generacion balanceada
items = []
for word, color in condiciones:
    items.append((word, color))
    for _, other_color in condiciones:
        if other_color != color:
            items.append((word, other_color))

# generacion de prueba
items = [
    ('ROJO', 'red'), ('VERDE', 'green') #, ('AZUL', 'blue'), ('AMARILLO', 'yellow'),
    #('ROJO', 'red'), ('VERDE', 'green'), ('AZUL', 'blue'), ('AMARILLO', 'yellow'),
    #('ROJO', 'red'), ('VERDE', 'green'), ('AZUL', 'blue'), ('AMARILLO', 'yellow'),
    #('ROJO', 'red'), ('VERDE', 'green'), ('AZUL', 'blue'), ('AMARILLO', 'yellow'),
]

# todavia no randomizamos los items
# random.shuffle(items)

# Carpeta para audios
audio_dir = "recordings"
os.makedirs(audio_dir, exist_ok=True)

# Micrófono
mic = microphone.Microphone()
'''
    device=None,      # dispositivo por defecto
    channels=1,       # MONO
    sampleRateHz=16000
)'''

# =====================
# INSTRUCCIONES
# =====================
instr = visual.TextStim(
    win,
    text=("Di el COLOR de la palabra. Pulsa una tecla para comenzar.")
)
instr.draw()
win.flip()
event.waitKeys()

clock = core.Clock()
results = []

# =====================
# EXPERIMENTO
# =====================
for trial, (word, color) in enumerate(items):

    # ---- INICIO GRABACIÓN ----
    # duración total: fijación (0.5) + estímulo (1.0)


    # Fijación (0.5 s)
    fix.draw()
    win.flip()
    core.wait(0.5)

    mic.start()

    # Estímulo Stroop (1 s)
    stim.text = word
    stim.color = color
    stim.draw()
    win.flip()

    clock.reset()
    core.wait(1.0)

    # limpiar pantalla
    win.flip()

    # ---- FIN GRABACIÓN Y GUARDADO ----
    mic.stop()
    audio_file = os.path.join(audio_dir, f'item{trial}.wav')
    audio = mic.getRecording().asMono()

    data = audio.samples
    orig_sr = audio.sampleRateHz  # probablemente 48000
    target_sr = 16000
    if orig_sr != target_sr:
        data = resample_poly(data, target_sr, orig_sr)
    sf.write(audio_file, data, target_sr, subtype="PCM_16")

    core.wait(0.5)

# =====================
# FINAL
# =====================
end = visual.TextStim(win, text="Fin de la tarea.\nGracias.")
end.draw()
win.flip()
core.wait(2)
win.close()
