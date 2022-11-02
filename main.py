import numpy as np
from pyglet.gl import *
import math

# definiranje struktura podataka koje ce biti potrebne
p_tocke = []
tangente = []
osi = []
kutovi = []
vrhovi_obj = []
poligon = []
s = np.array([0, 0, 1])  # pocetna orjentacija
B = np.array([[-1, 3, -3, 1], [3, -6, 3, 0], [-3, 0, 3, 0], [1, 4, 1, 0]])
Bt = np.array([[-1, 3, -3, 1], [2, -4, 2, 0], [-1, 0, 1, 0]])
V = [[0, 0, 0], [0, 10, 5], [10, 10, 10], [10, 0, 15], [0, 0, 20], [0, 10, 25], [10, 10, 30], [10, 0, 35], [0, 0, 40],
     [0, 10, 45], [10, 10, 50], [10, 0, 55]]

trenutni_indeks = 0
skaliranje = 15

width = 1500
height = 1000
window = pyglet.window.Window(1500, 1000)


def crtaj_spiralu():
    glBegin(GL_LINE_STRIP)
    boja = 0
    povecanje = 1. / len(p_tocke)
    for pm, tg in zip(p_tocke, tangente):
        # mozda ne radi sveucilisna profesorica nije sigurna - radi jebla te sveucilisna profesorica
        glVertex3f(*list(pm / skaliranje))
        glColor3f(1, boja, 1)
        boja += povecanje
        glVertex3f(*list((pm + tg) / skaliranje))
    glEnd()


def clean_up():
    glTranslatef(-0.15, -0.3, 0)


def crtaj_objekt():
    glColor3f(1, 1, 1)
    glTranslatef(*list(p_tocke[trenutni_indeks] / skaliranje))
    glRotatef(kutovi[trenutni_indeks], *list(osi[trenutni_indeks]))
    clean_up()
    glScalef(0.15, 0.15, 0.15)

    glBegin(GL_TRIANGLES)
    for pol in poligon:
        for j in pol:
            glVertex3f(*vrhovi_obj[j - 1])
    glEnd()


def update(*args):
    global trenutni_indeks
    novi_indeks = trenutni_indeks + 1
    if novi_indeks >= len(p_tocke):
        novi_indeks = 0
    trenutni_indeks = novi_indeks


@window.event
def on_draw():
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(60, float(width) / float(height), 0.1, 100)
    glMatrixMode(GL_MODELVIEW)
    # crtez unaprijed da se vidi
    # rotiramo crtez
    glClear(pyglet.gl.GL_COLOR_BUFFER_BIT)
    glLoadIdentity()
    glTranslatef(0, 2.0, -7.0)
    glRotatef(45, 1, 0, 0)
    crtaj_spiralu()
    crtaj_objekt()


def main():
    global vrhovi_obj, poligon, osi, p_tocke, kutovi, tangente
    # ucitatavanje objekta
    obj = open('tetraedar.obj', 'r')
    for line in obj:
        if line.startswith("#") or not line.split():
            continue
        line = line.split()
        if line[0] == "v":
            vrhovi_obj += [list(map(float, line[1:]))]
        elif line[0] == "f":
            poligon += [list(map(int, line[1:]))]

    for i in range(0, len(V) - 3):
        t = 0
        step = 0.1
        R = np.array([V[i], V[i + 1], V[i + 2], V[i + 3]])
        while t <= 1:
            # translacija
            p = (1 / 6 * np.dot(np.dot([t * t * t, t * t, t, 1], B), R))
            p_tocke.append(p)
            # orjentacija
            e = 1 / 2 * np.dot(np.dot([t * t, t, 1], Bt), R)
            tangente.append(e)
            osi.append(np.cross(s, e))
            cos = (np.multiply(s, e)) / (np.linalg.norm(s) * np.linalg.norm(e))
            kut = math.acos(cos[0])
            kutovi.append(math.degrees(kut))
            t += step

    pyglet.clock.schedule(update, .5)
    pyglet.app.run()


if __name__ == '__main__':
    main()
