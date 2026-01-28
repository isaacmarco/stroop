# pip install simpleaudio
# o pip install sounddevice
import json
import tkinter as tk
from tkinter import ttk
import os
import threading
import wave
#import simpleaudio as sa
import sounddevice as sd
import soundfile as sf

# =====================
# CONFIG
# =====================
JSON_FILE = "correcciones/correccion.json"
RECORDINGS_DIR = "recordings"

COLOR_MAP = {
    "Correccion.CORRECTA": "green",
    "Correccion.INCORRECTA": "red",
    "Correccion.SIN_DEFINIR": "gray"
}

# =====================
# AUDIO
# =====================
def play_wav(path):
    if not os.path.exists(path):
        print(f"No existe: {path}")
        return

    def _play():
        data, sr = sf.read(path)
        sd.play(data, sr)
        sd.wait()
        '''
        with wave.open(path, 'rb') as wf:
            audio = sa.WaveObject.from_wave_read(wf)
            play = audio.play()
            play.wait_done()
        '''
    threading.Thread(target=_play, daemon=True).start()

# =====================
# UI
# =====================
root = tk.Tk()
root.title("Revisión Stroop")

main_frame = ttk.Frame(root, padding=10)
main_frame.pack(fill="both", expand=True)

# -------- Etiqueta superior --------
label_total = ttk.Label(main_frame, text="Total de aciertos: 0", font=("Arial", 12, "bold"))
label_total.pack(anchor="w", pady=(0, 10))

items_frame = ttk.Frame(main_frame)
items_frame.pack(fill="both", expand=True)

# =====================
# CARGA JSON
# =====================
with open(JSON_FILE, "r", encoding="utf-8") as f:
    data = json.load(f)

items = data["correccion"]

total_aciertos = 0

for item in items:
    item_id = item["id"]
    color = item["color"]
    respuesta = item["respuesta"]
    correccion = item["correccion"]

    if correccion == "Correccion.CORRECTA":
        total_aciertos += 1

    bg_color = COLOR_MAP.get(correccion, "gray")

    row = ttk.Frame(items_frame)
    row.pack(fill="x", pady=2)

    # ---- Botón reproducir audio ----
    audio_path = os.path.join(RECORDINGS_DIR, f"item{item_id}.wav")

    play_btn = ttk.Button(
        row,
        text="▶",
        width=3,
        command=lambda p=audio_path: play_wav(p)
    )
    play_btn.pack(side="left", padx=(0, 5))

    # ---- Botón principal ----
    text_btn = f"{color}  →  {respuesta}"

    btn = tk.Button(
        row,
        text=text_btn,
        bg=bg_color,
        fg="white",
        anchor="w",
        relief="raised"
    )
    btn.pack(side="left", fill="x", expand=True)

# actualizar total
label_total.config(text=f"Total de aciertos: {total_aciertos}")

# =====================
# RUN
# =====================
root.mainloop()
