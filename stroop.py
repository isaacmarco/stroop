from psychopy import visual, core, event
from psychopy.sound import microphone
import random
import os

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
    ("MARRON", "brown"),
]

# generacion balanceada
items = []
for word, color in condiciones:
    items.append((word, color))
    for _, other_color in condiciones:
        if other_color != color:
            items.append((word, other_color))

# generacion de prueba
items = [('ROJO', 'red'), ('AZUL', 'blue'), ('VERDE', 'green')]

random.shuffle(items)

# Carpeta para audios
audio_dir = "recordings"
os.makedirs(audio_dir, exist_ok=True)

# Micrófono
mic = microphone.Microphone()

# =====================
# INSTRUCCIONES
# =====================
instr = visual.TextStim(
    win,
    text=(
        "Di el COLOR de la palabra.\n"
        "r=rojo, v=verde, a=azul, m=marrón\n\n"
        "Pulsa una tecla para empezar."
    )
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
    mic.start()

    # Fijación (0.5 s)
    fix.draw()
    win.flip()
    core.wait(0.5)

    # Estímulo Stroop (1 s)
    stim.text = word
    stim.color = color
    stim.draw()
    win.flip()

    clock.reset()
    keys = event.waitKeys(
        maxWait=1.0,
        keyList=["r", "v", "a", "m"],
        timeStamped=clock
    )

    # limpiar pantalla
    win.flip()

    # ---- FIN GRABACIÓN Y GUARDADO ----
    mic.stop()
    audio_file = os.path.join(audio_dir, f"trial_{trial:03d}.wav")
    recording = mic.getRecording()
    recording.save(audio_file)

    # Procesar respuesta
    if keys:
        key, rt = keys[0]
    else:
        key, rt = None, None

    correct = (
        (color == "red" and key == "r") or
        (color == "green" and key == "v") or
        (color == "blue" and key == "a") or
        (color == "brown" and key == "m")
    )

    results.append((trial, word, color, key, rt, correct, audio_file))

    core.wait(0.5)

# =====================
# FINAL
# =====================
end = visual.TextStim(win, text="Fin de la tarea.\nGracias.")
end.draw()
win.flip()
core.wait(2)
win.close()

for r in results:
    print(r)
