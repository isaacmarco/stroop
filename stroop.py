from psychopy import visual, core, event
import random

win = visual.Window(size=(800,600), color="black")

stim = visual.TextStim(win, text="", height=0.15)
fix = visual.TextStim(win, text="+", height=0.2, color="white")

conds = [
    ("ROJO", "red"),
    ("VERDE", "green"),
    ("AZUL", "blue"),
    ("MARRON", "brown"),
]

items = []
for word, color in conds:
    # item congruente
    items.append((word, color))
    # genera incongruente
    for _, other_color in conds:
        if other_color != color:
            items.append((word, other_color))

random.shuffle(items)

instr = visual.TextStim(win, text=
    "Di el COLOR de la palabra.\n"
    "r=rojo, v=verde, a=azul, m=marrón\n\n"
    "Pulsa una tecla para empezar."
)
instr.draw()
win.flip()
event.waitKeys()

clock = core.Clock()
results = []

# comenzamos el test
for word, color in items:
    # Fijación 500 ms
    fix.draw()
    win.flip()
    core.wait(0.5)

    # Estímulo Stroop
    stim.text = word
    stim.color = color
    stim.draw()
    win.flip()

    clock.reset()
    key = event.waitKeys(keyList=["r","v","a","m"])[0]
    rt = clock.getTime()

    correct = (
        (color=="red" and key=="r") or
        (color=="green" and key=="v") or
        (color=="blue" and key=="a") or
        (color=="brown" and key=="m")
    )

    results.append((word, color, key, rt, correct))

    win.flip()
    core.wait(0.5)

end = visual.TextStim(win, text="Fin de la tarea.\nGracias.")
end.draw()
win.flip()
core.wait(2)
win.close()

for r in results:
    print(r)
