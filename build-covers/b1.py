# -*- coding: utf-8 -*-
"""3 versiones de la portada del Bonus 1 (Termini Chiave di Farmacia Clinica)."""
import os, io, asyncio

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "opciones")
os.makedirs(OUT, exist_ok=True)
W, H, SCALE = 794, 1123, 3

HEAD = """
  <div class="mark"><b></b>Studio Facile<b></b></div>
  <div class="kicker">Bonus 01</div>
  <h1>Termini Chiave di<span class="plate">Farmacia Clinica</span></h1>
  <span class="az">Dalla A alla Z</span>"""


def shell(body):
    return (f'<!doctype html><html lang="it"><head><meta charset="utf-8">'
            f'<link rel="stylesheet" href="pro.css"></head><body>'
            f'<div class="page blu"><div class="bg blu"></div><div class="hex"></div>{body}'
            f'<div class="vig"></div></div></body></html>')


def shelves(rows, left=70, right=70):
    out = []
    for y, names, sz in rows:
        row = "".join(f'<img src="art/{n}.png" style="width:{sz}px;height:{sz}px" alt="">'
                      for n in names)
        out.append(f'<div class="goods" style="top:{y - sz}px;height:{sz}px;'
                   f'left:{left}px;right:{right}px">{row}</div>')
        out.append(f'<div class="shelf" style="top:{y}px;left:{left}px;right:{right}px"></div>')
    return "\n".join(out)


def onc(items):
    return "".join(f'<img class="onc" src="art/{n}.png" style="width:{w}px;{side}:{x}px;'
                   f'top:{y}px">' for n, w, side, x, y in items)


# ------------------------------------------------- A: farmacia, personaje al centro
ROWS_A = [
    (548, ["icon-medbox", "icon-bottles", "icon-syrup", "icon-blister", "icon-cream",
           "icon-medbox"], 64),
    (668, ["icon-suspension", "icon-elixir", "icon-confetto", "icon-dropper", "icon-gel",
           "icon-bottles"], 62),
    (788, ["icon-blister", "icon-mortar", "icon-thermometer", "icon-medbox", "icon-cream",
           "icon-elixir"], 62),
]

A = shell(f"""
<div class="wall"></div>
{shelves(ROWS_A)}
<div class="glow" style="width:600px;height:600px;top:640px;
  background:radial-gradient(closest-side,rgba(150,200,255,.42),rgba(120,180,255,0) 70%)"></div>
<div class="hero" style="width:344px;top:566px"><img src="art3d/avatar-lab-bust.png" alt=""></div>
{onc([("icon-medbox", 78, "left", 78, 935), ("icon-bottles", 70, "left", 186, 943),
      ("icon-blister", 76, "right", 84, 937), ("icon-mortar", 70, "right", 190, 943)])}
<div class="counter"></div>
<div class="top">{HEAD}</div>
<div class="bottom" style="bottom:48px"><span class="pill">Studio Facile</span></div>""")

# ------------------------------------------------- B: personaje a la derecha + discos
def disc(img, size, x, y, iw, cap):
    return (f'<div class="chip3" style="width:{size}px;height:{size}px;left:{x}px;top:{y}px">'
            f'<img src="art/{img}.png" style="width:{iw}px;height:{iw}px" alt="">'
            f'<span class="cap">{cap}</span></div>')


B = shell(f"""
<div class="glow" style="width:620px;height:620px;top:660px;left:66%;
  background:radial-gradient(closest-side,rgba(150,200,255,.46),rgba(120,180,255,0) 70%)"></div>
{disc("icon-mortar", 132, 54, 452, 100, "Preparazione")}
{disc("icon-bottles", 122, 42, 622, 92, "Forme e dosi")}
{disc("icon-clipboard", 122, 96, 782, 92, "Posologia")}
<img class="spark" src="art/icon-molecule.png" style="width:84px;left:212px;top:470px;opacity:.8">
<img class="spark" src="art/icon-capsule.png" style="width:58px;left:236px;top:806px;transform:rotate(-24deg)">
<div class="hero" style="width:392px;top:500px;left:auto;right:-6px;transform:none">
  <img src="art3d/avatar-lab-bust.png" alt=""></div>
<div class="counter"></div>
{onc([("icon-medbox", 76, "left", 88, 937), ("icon-bottles", 70, "left", 194, 943)])}
<div class="top">{HEAD}</div>
<div class="bottom" style="bottom:48px;text-align:left;padding-left:56px">
  <span class="pill">Studio Facile</span></div>""")

# ------------------------------------------------- C: vitrina, sin personaje
ROWS_C = [
    (520, ["icon-medbox", "icon-bottles", "icon-syrup", "icon-blister", "icon-cream",
           "icon-elixir", "icon-medbox"], 60),
    (650, ["icon-suspension", "icon-polvere", "icon-confetto", "icon-dropper", "icon-gel",
           "icon-ointment", "icon-bottles"], 58),
    (780, ["icon-blister", "icon-mortar", "icon-thermometer", "icon-syrup", "icon-medbox",
           "icon-cream", "icon-elixir"], 58),
]

C = shell(f"""
<div class="wall" style="top:412px;height:414px"></div>
{shelves(ROWS_C, 66, 66)}
<div class="glow" style="width:520px;height:520px;top:640px;
  background:radial-gradient(closest-side,rgba(160,205,255,.55),rgba(120,180,255,0) 70%)"></div>
<div class="azdisc">
  <div class="t">A<i>&ndash;</i>Z</div>
  <div class="s">Glossario</div>
  <div class="n">120+ termini</div>
</div>
<div class="counter"></div>
{onc([("icon-mortar", 80, "left", 78, 933), ("icon-medbox", 76, "right", 82, 937),
      ("icon-blister", 70, "left", 190, 943), ("icon-bottles", 70, "right", 190, 943)])}
<div class="top">{HEAD}</div>
<div class="bottom" style="bottom:48px"><span class="pill">Studio Facile</span></div>""")

PAGES = [("B1-A-farmacia", A), ("B1-B-farmacista", B), ("B1-C-vetrina", C)]


async def main():
    from playwright.async_api import async_playwright
    from PIL import Image, ImageDraw, ImageFont
    ims = []
    async with async_playwright() as pw:
        b = await pw.chromium.launch()
        pg = await b.new_page(viewport={"width": W, "height": H}, device_scale_factor=SCALE)
        for name, html in PAGES:
            f = os.path.join(ROOT, f"_b1_{name}.html")
            open(f, "w", encoding="utf-8").write(html)
            await pg.goto("file:///" + f.replace("\\", "/"))
            await pg.wait_for_timeout(700)
            png = await pg.screenshot(clip={"x": 0, "y": 0, "width": W, "height": H})
            im = Image.open(io.BytesIO(png)).convert("RGB")
            im.save(os.path.join(OUT, name + ".png"))
            ims.append((name, im))
            print(name)
        await b.close()

    tw = 480
    th = int(tw * H / W)
    sh = Image.new("RGB", (tw * 3 + 40, th + 44), (238, 238, 242))
    fnt = ImageFont.truetype(os.path.join(ROOT, "fonts", "Poppins-SemiBold.ttf"), 20)
    d = ImageDraw.Draw(sh)
    for i, (n, im) in enumerate(ims):
        x = 10 + i * (tw + 10)
        sh.paste(im.resize((tw, th), Image.LANCZOS), (x, 34))
        d.text((x + 4, 8), n, font=fnt, fill=(30, 30, 40))
    sh.save(os.path.join(OUT, "_b1_opciones.png"))
    print("hoja OK")


asyncio.run(main())
