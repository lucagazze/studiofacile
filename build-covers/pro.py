# -*- coding: utf-8 -*-
"""Portadas 'pro' de los 2 bonus, en la linea de las originales:
fondo de gradiente, escena/hero con glow, titulo en placa. Sin IA (keys caidas):
usa los renders 3D en alta y los iconos del proyecto del libro.
"""
import os, io, asyncio, math

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "opciones")
os.makedirs(OUT, exist_ok=True)
W, H, SCALE = 794, 1123, 3

WAVE = ('<svg class="wave {c}" style="top:{t}px" viewBox="0 0 1000 220" '
        'preserveAspectRatio="none" height="220"><path d="{d}"/></svg>')
D1 = "M0,120 C160,40 330,180 520,110 C700,44 860,140 1000,86 L1000,220 L0,220 Z"
D2 = "M0,150 C200,80 340,196 540,140 C740,84 880,170 1000,120 L1000,220 L0,220 Z"


def sparks(items):
    return "".join(
        f'<img class="spark" src="art/{n}.png" style="width:{w}px;left:{x}px;top:{y}px;'
        f'transform:rotate({r}deg)">' for n, w, x, y, r in items)


def dots(items):
    return "".join(f'<div class="dot" style="width:{s}px;height:{s}px;left:{x}px;top:{y}px;'
                   f'opacity:{o}"></div>' for s, x, y, o in items)


def rays(cx, cy, n, ln, w, spread=360, start=-90):
    out = []
    for k in range(n):
        a = start + k * (spread / n)
        out.append(f'<div class="ray" style="left:{cx}px;top:{cy - ln}px;width:{w}px;'
                   f'height:{ln}px;transform:rotate({a + 90}deg);opacity:.5"></div>')
    return "".join(out)


def shell(theme, body):
    return (f'<!doctype html><html lang="it"><head><meta charset="utf-8">'
            f'<link rel="stylesheet" href="pro.css"></head><body>'
            f'<div class="page {theme}"><div class="bg {theme}"></div>{body}'
            f'<div class="vig"></div></div></body></html>')


# ============================================ BONUS 1 — escena de farmacia
# (y de la balda, iconos que van encima, tamano)
GOODS = [
    (566, ["icon-medbox", "icon-bottles", "icon-syrup", "icon-blister", "icon-cream",
           "icon-medbox"], 68),
    (706, ["icon-suspension", "icon-elixir", "icon-confetto", "icon-dropper", "icon-gel",
           "icon-bottles"], 66),
    (846, ["icon-blister", "icon-mortar", "icon-thermometer", "icon-medbox", "icon-cream",
           "icon-elixir"], 66),
]


def shelves():
    out = []
    for y, names, sz in GOODS:
        row = "".join(f'<img src="art/{n}.png" style="width:{sz}px;height:{sz}px" alt="">'
                      for n in names)
        out.append(f'<div class="goods" style="top:{y - sz}px;height:{sz}px">{row}</div>')
        out.append(f'<div class="shelf" style="top:{y}px"></div>')
    return "\n".join(out)


B1 = shell("blu", f"""
<div class="hex"></div>
<div class="wall"></div>
{shelves()}
<div class="glow" style="width:600px;height:600px;top:700px;
  background:radial-gradient(closest-side,rgba(150,200,255,.42),rgba(120,180,255,0) 70%)"></div>
<div class="hero" style="width:392px;top:560px"><img src="art3d/avatar-lab-bust.png" alt=""></div>
<img class="onc" src="art/icon-medbox.png" style="width:72px;left:96px;top:930px">
<img class="onc" src="art/icon-bottles.png" style="width:66px;left:196px;top:938px">
<img class="onc" src="art/icon-blister.png" style="width:70px;right:104px;top:934px">
<img class="onc" src="art/icon-mortar.png" style="width:66px;right:200px;top:938px">
<div class="counter"></div>
{sparks([("icon-capsule", 60, 96, 372, -22), ("icon-tablet", 52, 646, 384, 16)])}
{dots([(8, 190, 402, .7), (6, 592, 396, .65)])}
<div class="top">
  <div class="mark"><b></b>Studio Facile<b></b></div>
  <div class="kicker">Bonus 01</div>
  <h1>Termini Chiave di<span class="plate">Farmacia Clinica</span></h1>
  <span class="az">Dalla A alla Z</span>
</div>
<div class="bottom" style="bottom:52px"><span class="pill">Studio Facile</span></div>""")

# ============================================ BONUS 2 — Schede di Ripasso
B2 = shell("mag", f"""
{WAVE.format(c="w1", t=560, d=D1)}
{WAVE.format(c="w2", t=820, d=D2)}
<div class="glow" style="width:620px;height:620px;top:500px;
  background:radial-gradient(closest-side,rgba(255,225,160,.62),rgba(255,190,120,0) 70%)"></div>
{rays(397, 760, 12, 190, 4)}
<div class="hero" style="width:430px;top:530px"><img src="art3d/hero-pills.png" alt=""></div>
{sparks([("icon-capsule", 88, 92, 596, -24), ("icon-tablet", 76, 630, 640, 18),
         ("icon-blister", 92, 62, 880, -10), ("icon-molecule", 96, 646, 900, 0)])}
{dots([(9, 168, 574, .85), (6, 640, 592, .8), (7, 118, 852, .7), (6, 690, 838, .7),
       (10, 560, 552, .6), (5, 250, 900, .6)])}
<div class="top">
  <div class="mark"><b></b>Studio Facile<b></b></div>
  <div class="kicker">Bonus 02</div>
  <h1>Schede di Ripasso<span class="plate">Rapido</span></h1>
  <span class="plate amber">Le 5 classi che escono<br>pi&ugrave; spesso all'esame</span>
</div>
<div class="bottom">
  <div class="cls">Antipertensivi<i>|</i>FANS<i>|</i>Antibiotici<br>
    Benzodiazepine<i>|</i>Oppioidi</div>
  <span class="pill">Studio Facile</span>
</div>""")

PAGES = [("PRO-bonus1-farmacia-clinica", B1), ("PRO-bonus2-schede-ripasso", B2)]


async def main():
    from playwright.async_api import async_playwright
    from PIL import Image, ImageDraw, ImageFont
    ims = []
    async with async_playwright() as pw:
        b = await pw.chromium.launch()
        pg = await b.new_page(viewport={"width": W, "height": H}, device_scale_factor=SCALE)
        for name, html in PAGES:
            f = os.path.join(ROOT, f"_p_{name}.html")
            open(f, "w", encoding="utf-8").write(html)
            await pg.goto("file:///" + f.replace("\\", "/"))
            await pg.wait_for_timeout(700)
            png = await pg.screenshot(clip={"x": 0, "y": 0, "width": W, "height": H})
            im = Image.open(io.BytesIO(png)).convert("RGB")
            im.save(os.path.join(OUT, name + ".png"))
            ims.append((name, im))
            print(name, im.size)
        await b.close()

    tw = 560
    th = int(tw * H / W)
    sh = Image.new("RGB", (tw * 2 + 30, th + 44), (238, 238, 242))
    fnt = ImageFont.truetype(os.path.join(ROOT, "fonts", "Poppins-SemiBold.ttf"), 18)
    d = ImageDraw.Draw(sh)
    for i, (n, im) in enumerate(ims):
        x = 10 + i * (tw + 10)
        sh.paste(im.resize((tw, th), Image.LANCZOS), (x, 34))
        d.text((x + 4, 8), n, font=fnt, fill=(30, 30, 40))
    sh.save(os.path.join(OUT, "_comparativa_pro.png"))
    print("hoja pro OK")


asyncio.run(main())
