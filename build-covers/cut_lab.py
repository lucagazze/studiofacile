# -*- coding: utf-8 -*-
"""Recorta el avatar con bata (portada del PDF) sobre alfa.
Quita crema + blobs por color y se queda solo con el componente mas grande.
"""
import os
import numpy as np
from collections import deque
from PIL import Image
import fitz

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "art3d", "avatar-lab.png")
PDF = r"C:\Users\lucag\Downloads\drive-download-20260830T155037Z-1-001\KIT COMPLETO\Farmacologia-Illustrata.pdf"

# (color, tolerancia) — el lila del blob va mas alto que el resto,
# pero por debajo de los 22 que lo separan del lila de la capsula
BG = [((247, 246, 241), 13), ((185, 230, 210), 17), ((222, 193, 241), 17)]
BOX = (740, 1330, 1820, 3010)

d = fitz.open(PDF)
pix = d[0].get_pixmap(dpi=300)
page = Image.frombytes("RGB", (pix.width, pix.height), pix.samples).crop(BOX)
a = np.asarray(page).astype(np.int16)
h, w = a.shape[:2]

# mascara de "es fondo" por color
isbg = np.zeros((h, w), bool)
for c, tol in BG:
    isbg |= (np.abs(a - np.array(c)).max(axis=2) <= tol)

# floodfill desde los bordes: solo el fondo conectado se vuelve transparente
out = np.zeros((h, w), bool)
q = deque()
for x in range(w):
    for y in (0, h - 1):
        if isbg[y, x]:
            q.append((y, x)); out[y, x] = True
for y in range(h):
    for x in (0, w - 1):
        if isbg[y, x] and not out[y, x]:
            q.append((y, x)); out[y, x] = True
while q:
    y, x = q.popleft()
    for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        ny, nx = y + dy, x + dx
        if 0 <= ny < h and 0 <= nx < w and isbg[ny, nx] and not out[ny, nx]:
            out[ny, nx] = True
            q.append((ny, nx))

keep = ~out

# quedarse con el componente mas grande (mata los puntitos del anillo y los circulos)
lab = np.zeros((h, w), np.int32)
cur, best, bestn = 0, 0, 0
for y0 in range(h):
    for x0 in range(w):
        if keep[y0, x0] and lab[y0, x0] == 0:
            cur += 1
            n = 0
            st = [(y0, x0)]
            lab[y0, x0] = cur
            while st:
                y, x = st.pop()
                n += 1
                for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    ny, nx = y + dy, x + dx
                    if 0 <= ny < h and 0 <= nx < w and keep[ny, nx] and lab[ny, nx] == 0:
                        lab[ny, nx] = cur
                        st.append((ny, nx))
            if n > bestn:
                bestn, best = n, cur

alpha = np.where(lab == best, 255, 0).astype(np.uint8)
im = page.convert("RGBA")
arr = np.asarray(im).copy()
arr[:, :, 3] = alpha
im = Image.fromarray(arr)
im = im.crop(im.getbbox())            # -> 902 x 1354, sistema de referencia fijo

# restos del borde del blob lila pegados a la manga (medidos sobre ese recorte)
arr2 = np.asarray(im).copy()
arr2[700:, 700:, 3] = 0            # borde del blob lila contra la manga
im = Image.fromarray(arr2)

# apertura morfologica: borra el arco fino del anillo punteado, respeta la figura
from PIL import ImageFilter
im.putalpha(im.split()[3].filter(ImageFilter.MinFilter(7)).filter(ImageFilter.MaxFilter(7)))
im = im.crop(im.getbbox())

# ultimos restos del borde del blob, medidos sobre la imagen final
arr3 = np.asarray(im).copy()
H3, W3 = arr3.shape[:2]
# corte suave del lado derecho: evita el canto duro donde estaba el blob
x0, x1 = int(W3 * .93), W3
ramp = np.linspace(1.0, 0.0, x1 - x0)
band = arr3[int(H3 * .5):, x0:x1, 3].astype(float) * ramp
arr3[int(H3 * .5):, x0:x1, 3] = band.astype(np.uint8)
im = Image.fromarray(arr3)
im = im.crop(im.getbbox())

os.makedirs(os.path.dirname(OUT), exist_ok=True)
im.save(OUT)
print("avatar-lab", im.size, "px del personaje:", bestn)
