# -*- coding: utf-8 -*-
"""Mockups del Kit (tablets + collage de muestras) para la landing.
Render con Playwright, fondo transparente -> mockups/*.webp
"""
import os, io, asyncio, random

ROOT = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(ROOT)
OUT = os.path.join(SITE, "mockups")
os.makedirs(OUT, exist_ok=True)

COV = "out"  # portadas de los bonus
MAIN = "../portadas-tienda/01_Farmacologia-Illustrata.png"
B1 = "opciones/FINAL-bonus1-farmacia-clinica.png"
B2 = "opciones/FINAL-bonus2-schede-ripasso.png"

CSS = """
*{margin:0;padding:0;box-sizing:border-box}
body{background:transparent}
.stage{position:relative}
.tab{position:absolute;border-radius:38px;padding:13px;
  background:linear-gradient(150deg,#4a4d55 0%,#2c2e35 38%,#212329 100%);
  box-shadow:0 34px 64px rgba(15,23,42,.34), 0 8px 18px rgba(15,23,42,.20),
             inset 0 1px 0 rgba(255,255,255,.22), inset 0 -1px 0 rgba(0,0,0,.35);}
.tab .scr{width:100%;height:100%;border-radius:26px;overflow:hidden;background:#fff;
  box-shadow:inset 0 0 0 1px rgba(0,0,0,.35)}
.tab .scr img{width:100%;height:100%;object-fit:cover;display:block}
.tab .gl{position:absolute;inset:13px;border-radius:26px;pointer-events:none;
  background:linear-gradient(118deg,rgba(255,255,255,.30) 0%,rgba(255,255,255,.07) 26%,
             rgba(255,255,255,0) 46%)}
.sheet{position:absolute;border-radius:10px;overflow:hidden;background:#fff;
  box-shadow:0 16px 34px rgba(15,23,42,.20)}
.sheet img{width:100%;height:100%;object-fit:cover;display:block}
"""


def page(w, h, body):
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>{CSS}
body{{width:{w}px;height:{h}px}}</style></head><body>
<div class="stage" style="width:{w}px;height:{h}px">{body}</div></body></html>"""


def tab(src, x, y, w, h, z=1, rot=0, scale=1.0):
    return (f'<div class="tab" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px;'
            f'z-index:{z};transform:rotate({rot}deg) scale({scale})">'
            f'<div class="scr"><img src="{src}" alt=""></div><div class="gl"></div></div>')


# ------------------------------------------------------------------ trio
# Geometria calcada de la 57.webp original (lienzo 1200x886, contenido x 36..1164,
# y 35..873): los tres tablets arrancan a la misma altura y el central baja mas.
def trio():
    return (tab(B1, 36, 35, 460, 640, 1)
            + tab(B2, 704, 35, 460, 640, 1)
            + tab(MAIN, 300, 35, 600, 838, 3))


HERO = page(1200, 886, trio())
COMBO = page(1200, 886, trio())
SOLO1 = page(720, 1000, tab(B1, 40, 40, 640, 920, 2))
SOLO2 = page(720, 1000, tab(B2, 40, 40, 640, 920, 2))

# --------------------------------------------------------------- collage
SAMPLES = ["../amostras/vie-somministrazione.webp", "../amostras/percorso-farmaco.webp",
           "../amostras/distribuzione.webp", "../amostras/nefrone.webp",
           "../amostras/cinetica-x-dinamica.webp", "../amostras/interazioni-warfarin.webp",
           "../amostras/interazioni-ibuprofene.webp"]

# (x, y, w, rot) — hojas alrededor del tablet central
SHEETS = [(-60, -30, 470, -7), (330, -70, 470, 5), (660, -20, 470, 9),
          (-90, 480, 470, 4), (620, 500, 470, -6),
          (-40, 990, 470, -9), (350, 1030, 470, 3), (680, 980, 470, 7)]


def collage():
    parts = []
    for i, (x, y, w, rot) in enumerate(SHEETS):
        src = SAMPLES[i % len(SAMPLES)]
        h = int(w * 1874 / 1405)
        parts.append(f'<div class="sheet" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px;'
                     f'z-index:1;transform:rotate({rot}deg)"><img src="{src}" alt=""></div>')
    parts.append(tab(MAIN, 270, 400, 560, 786, 6))
    return "".join(parts)


COLLAGE = page(1100, 1620, collage())

PAGES = [("hero-kit", HERO, 1200, 886),
         ("combo-entregaveis", COMBO, 1200, 886),
         ("bonus-1", SOLO1, 720, 1000),
         ("bonus-2", SOLO2, 720, 1000),
         ("combo-amostras", COLLAGE, 1100, 1620)]


async def main():
    from playwright.async_api import async_playwright
    from PIL import Image
    async with async_playwright() as pw:
        b = await pw.chromium.launch()
        for name, html, w, h in PAGES:
            pg = await b.new_page(viewport={"width": w, "height": h}, device_scale_factor=2)
            f = os.path.join(ROOT, f"_mk_{name}.html")
            open(f, "w", encoding="utf-8").write(html)
            await pg.goto("file:///" + f.replace("\\", "/"))
            await pg.wait_for_timeout(700)
            png = await pg.screenshot(omit_background=True,
                                      clip={"x": 0, "y": 0, "width": w, "height": h})
            im = Image.open(io.BytesIO(png)).convert("RGBA")
            p = os.path.join(OUT, name + ".webp")
            im.save(p, "WEBP", quality=90, method=6)
            print(name, im.size, os.path.getsize(p) // 1024, "KB")
            await pg.close()
        await b.close()


asyncio.run(main())
