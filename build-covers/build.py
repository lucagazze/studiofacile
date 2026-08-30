# -*- coding: utf-8 -*-
"""Portadas de los 2 bonus del Kit Farmacologia Illustrata.
Render A4 (794x1123 CSS, scale 3) con Playwright -> PNG 300dpi + PDF de 1 pagina.
"""
import os, io, asyncio, math

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "out")
os.makedirs(OUT, exist_ok=True)
W, H, SCALE = 794, 1123, 3


def shell(body, theme=""):
    return f"""<!doctype html><html lang="it"><head><meta charset="utf-8">
<link rel="stylesheet" href="cover.css"></head><body>
<div class="page {theme}"><div class="grid"></div><div class="halo"></div>{body}</div>
</body></html>"""


# --------------------------------------------------------------- bonus 1
def ring_nodes():
    """6 nodos sobre la circunferencia del anillo (600x600, radio 236)."""
    items = [("i", "art/icon-book.png", "t1"), ("t", "A", "t4"),
             ("i", "art/icon-clipboard.png", "t2"), ("t", "Z", "t3"),
             ("i", "art/icon-magnifier.png", "t2"), ("i", "art/icon-molecule.png", "t1")]
    out = []
    cx = cy = 300.0
    r = 238.0
    for k, (kind, val, tone) in enumerate(items):
        ang = math.radians(-90 + k * 60)
        x = cx + r * math.cos(ang) - 62
        y = cy + r * math.sin(ang) - 62
        if kind == "i":
            out.append(f'<div class="node {tone}" style="left:{x:.0f}px;top:{y:.0f}px">'
                       f'<img src="{val}" alt=""></div>')
        else:
            out.append(f'<div class="node letter {tone}" style="left:{x:.0f}px;'
                       f'top:{y:.0f}px">{val}</div>')
    return "".join(out)


BONUS1 = shell(f"""
<div class="blob" style="width:236px;height:236px;left:-56px;top:424px"></div>
<div class="blob" style="width:262px;height:262px;right:-70px;top:648px"></div>
<div class="blob" style="width:168px;height:168px;left:-18px;top:900px"></div>
<img class="deco" src="art/icon-capsule.png" style="width:74px;left:52px;top:398px;transform:rotate(-20deg)">
<img class="deco" src="art/icon-tablet.png"  style="width:64px;right:56px;top:430px;transform:rotate(14deg)">
<img class="deco" src="art/icon-molecule.png" style="width:88px;left:22px;top:668px;opacity:.75">
<img class="deco" src="art/icon-molecule.png" style="width:76px;right:26px;top:912px;opacity:.6;transform:scaleX(-1)">
<img class="deco" src="art/icon-capsule.png" style="width:62px;left:96px;top:942px;transform:rotate(28deg)">
<div class="cover">
  <div class="brandmark"><b></b>Studio Facile<b></b></div>
  <div class="badge">Bonus 01</div>
  <h1>Termini Chiave di<span>Farmacia Clinica</span></h1>
  <div class="sub">Il glossario dalla A alla Z della pratica clinica</div>
  <div class="ring">
    <div class="dots"></div>
    {ring_nodes()}
    <div class="core">
      <div class="az">A<i>&ndash;</i>Z</div>
      <div class="lb">Glossario</div>
    </div>
  </div>
  <div class="chips">
    <span class="chip g">Definizioni brevi</span>
    <span class="chip m">Esempi clinici</span>
    <span class="chip s">Ordine alfabetico</span>
    <span class="chip p">Consultazione rapida</span>
  </div>
</div>""", "b1")


# --------------------------------------------------------------- bonus 2
CLASSI = [("art/icon-bloodflow.png", "Antipertensivi", "t1"),
          ("art/icon-headache.png", "FANS", "t2"),
          ("art/icon-microscope.png", "Antibiotici", "t3"),
          ("art/icon-brain.png", "Benzodiazepine", "t4"),
          ("art/icon-capsule.png", "Oppioidi", "t5")]


def ring5():
    out = []
    cx = cy = 310.0
    r = 244.0
    for k, (img, nm, tone) in enumerate(CLASSI):
        ang = math.radians(-90 + k * 72)
        x = cx + r * math.cos(ang) - 66
        y = cy + r * math.sin(ang) - 78
        out.append(f'<div class="nd {tone}" style="left:{x:.0f}px;top:{y:.0f}px">'
                   f'<div class="circ"><img src="{img}" alt=""></div>'
                   f'<div class="lb">{nm}</div></div>')
    return "".join(out)


BONUS2 = shell(f"""
<div class="blob" style="width:270px;height:270px;left:-96px;top:392px"></div>
<div class="blob" style="width:236px;height:236px;right:-78px;top:452px"></div>
<div class="blob" style="width:190px;height:190px;left:-58px;top:822px"></div>
<img class="deco" src="art/icon-molecule.png" style="width:88px;left:28px;top:346px;opacity:.7">
<img class="deco" src="art/icon-molecule.png" style="width:76px;right:26px;top:380px;opacity:.6;transform:scaleX(-1)">
<img class="deco" src="art/icon-tablet.png" style="width:58px;left:78px;top:962px;transform:rotate(-12deg)">
<img class="deco" src="art/icon-capsule.png" style="width:64px;right:76px;top:952px;transform:rotate(22deg)">
<div class="cover">
  <div class="brandmark"><b></b>Studio Facile<b></b></div>
  <div class="badge">Bonus 02</div>
  <h1>Schede di Ripasso<span>Rapido</span></h1>
  <div class="sub">Le 5 classi che escono pi&ugrave; spesso all'esame</div>
  <div class="ring5">
    <div class="band"></div>
    {ring5()}
    <div class="core">
      <div class="big">5</div>
      <div class="k1">Classi</div>
      <div class="k2">Essenziali</div>
    </div>
  </div>
  <div class="chips">
    <span class="chip g">Meccanismo d'azione</span>
    <span class="chip m">Effetti avversi</span>
    <span class="chip s">Interazioni</span>
    <span class="chip p">Da stampare</span>
  </div>
</div>""", "b2")

PAGES = [("bonus-1-farmacia-clinica-a-z", BONUS1),
         ("bonus-2-schede-ripasso-rapido", BONUS2)]


async def main():
    from playwright.async_api import async_playwright
    from PIL import Image
    async with async_playwright() as pw:
        b = await pw.chromium.launch()
        pg = await b.new_page(viewport={"width": W, "height": H}, device_scale_factor=SCALE)
        for name, html in PAGES:
            f = os.path.join(ROOT, f"_{name}.html")
            open(f, "w", encoding="utf-8").write(html)
            await pg.goto("file:///" + f.replace("\\", "/"))
            await pg.wait_for_timeout(600)
            png = await pg.screenshot(clip={"x": 0, "y": 0, "width": W, "height": H})
            im = Image.open(io.BytesIO(png)).convert("RGB")
            im.save(os.path.join(OUT, name + ".png"))
            print(name, im.size)
        await b.close()


asyncio.run(main())
