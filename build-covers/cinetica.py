# -*- coding: utf-8 -*-
"""Rehace la pagina 'Cinetica vs Dinamica' en el estilo Studio Facile.
Recorta las 4 ilustraciones del PDF (fondo blanco -> alfa) y maqueta la pagina.
"""
import os, io, asyncio
from collections import deque

ROOT = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(ROOT)
ART = os.path.join(ROOT, "cut")
os.makedirs(ART, exist_ok=True)
PDF = r"C:\Users\lucag\Downloads\drive-download-20260830T155037Z-1-001\KIT COMPLETO\Farmacologia-Illustrata.pdf"
W, H, SCALE = 794, 1123, 3

# (nombre, x0, y0, x1, y1) en pixeles a 120 dpi
CROPS = [("archer", 210, 362, 478, 604),
         ("capsule-scared", 578, 368, 782, 604),
         ("capsule-strong", 214, 922, 410, 1156),
         ("doctor-happy", 606, 922, 800, 1156)]


def key_white(im, tol=26):
    """Floodfill desde los bordes: todo lo casi-blanco conectado pasa a alfa 0."""
    im = im.convert("RGBA")
    px = im.load()
    w, h = im.size
    seen = bytearray(w * h)
    q = deque()

    def near_white(p):
        # fondo = cualquier tono claro (blanco del circulo o el tinte del panel)
        return min(p[0], p[1], p[2]) > 182

    for x in range(w):
        for y in (0, h - 1):
            q.append((x, y))
    for y in range(h):
        for x in (0, w - 1):
            q.append((x, y))
    while q:
        x, y = q.popleft()
        i = y * w + x
        if seen[i]:
            continue
        seen[i] = 1
        if not near_white(px[x, y]):
            continue
        px[x, y] = (255, 255, 255, 0)
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nx, ny = x + dx, y + dy
            if 0 <= nx < w and 0 <= ny < h and not seen[ny * w + nx]:
                q.append((nx, ny))
    return im


def cut():
    import fitz
    from PIL import Image
    d = fitz.open(PDF)
    pix = d[40].get_pixmap(dpi=300)
    page = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
    k = 300 / 120
    for name, x0, y0, x1, y1 in CROPS:
        box = tuple(int(v * k) for v in (x0, y0, x1, y1))
        im = key_white(page.crop(box))
        im = im.crop(im.getbbox())
        im.save(os.path.join(ART, name + ".png"))
        print("cut", name, im.size)


CSS = """
@font-face{font-family:'Poppins';src:url('fonts/Poppins-Regular.ttf');font-weight:400}
@font-face{font-family:'Poppins';src:url('fonts/Poppins-Medium.ttf');font-weight:500}
@font-face{font-family:'Poppins';src:url('fonts/Poppins-SemiBold.ttf');font-weight:600}
@font-face{font-family:'Poppins';src:url('fonts/Poppins-Bold.ttf');font-weight:700}
@font-face{font-family:'Poppins';src:url('fonts/Poppins-ExtraBold.ttf');font-weight:800}
:root{--paper:#f8f6f1;--plum:#562a5f;--teal:#2f897d;--ink:#2a2b3d;--soft:#585755;
  --lav:#f0e6fa;--lav2:#c9a8ea;--mint:#e4f5ec;--mint2:#8fd3b8;--eb:#9470a4;--sky:#e4eefb;--sky2:#9dc2ee;--blu:#24499b}
*{margin:0;padding:0;box-sizing:border-box}
html,body{background:#c9ccd8}
.page{position:relative;width:794px;height:1123px;overflow:hidden;background:var(--paper);
  font-family:'Poppins',sans-serif;color:var(--ink);padding:34px 40px 30px}
.deco{position:absolute;z-index:1;opacity:.9}
.eyebrow{display:flex;align-items:center;gap:9px;font-size:10.5px;font-weight:800;
  letter-spacing:2.8px;text-transform:uppercase;color:var(--eb)}
.eyebrow b{width:16px;height:3px;border-radius:2px;background:var(--lav2)}
h1{margin-top:6px;font-size:56px;font-weight:800;letter-spacing:-1.4px;line-height:1;
  color:var(--plum)}
h1 i{font-style:normal;color:var(--lav2)}
h1 em{font-style:normal;color:var(--teal)}
.panel{position:relative;z-index:2;margin-top:18px;border-radius:34px;padding:20px 26px 18px;
  text-align:center}
.panel.a{background:var(--sky)}
.panel.b{background:var(--mint)}
.panel h2{font-size:29px;font-weight:800;letter-spacing:-.4px}
.panel.a h2{color:var(--blu)} .panel.b h2{color:var(--teal)}
.rule{display:flex;align-items:center;justify-content:center;gap:14px;margin-top:6px;
  font-size:14px;font-weight:600;color:var(--soft)}
.rule s{flex:0 0 92px;height:2px;background:rgba(0,0,0,.14);border-radius:2px}
.q{margin:14px auto 0;max-width:560px;background:#fff;border-radius:999px;padding:11px 26px;
  font-size:17.5px;font-weight:800;color:var(--ink)}
.scene{position:relative;display:flex;align-items:center;justify-content:center;
  margin-top:12px}
.fig{position:relative;z-index:2;display:flex;flex-direction:column;align-items:center;
  width:250px}
.disc{width:206px;height:206px;border-radius:50%;background:#fff;display:flex;
  align-items:center;justify-content:center;overflow:hidden;
  box-shadow:0 12px 26px rgba(28,29,46,.13)}
.disc img{max-width:178px;max-height:178px;object-fit:contain}
.disc.av img{max-width:none;max-height:none;width:100%;height:100%;object-fit:cover;
  object-position:50% 10%}
.tag{margin-top:9px;padding:5px 16px;border-radius:999px;background:#fff;font-size:12.5px;
  font-weight:800;color:var(--ink);box-shadow:0 5px 12px rgba(28,29,46,.10)}
.arrow{position:absolute;z-index:3;left:50%;top:76px;transform:translateX(-50%);
  display:flex;flex-direction:column;align-items:center}
.arrow span{font-size:15px;font-weight:800;color:var(--blu);margin-bottom:5px}
.panel.b .arrow span{color:var(--teal)}
.arrow svg{width:186px;height:26px}
.foot{margin:16px auto 0;max-width:640px;background:#fff;border-radius:999px;padding:11px 24px;
  font-size:15.5px;font-weight:800;color:var(--ink)}
.panel.a .foot{box-shadow:inset 0 0 0 2px var(--sky2)}
.panel.b .foot{box-shadow:inset 0 0 0 2px var(--mint2)}
"""


def arrow(color):
    return (f'<svg viewBox="0 0 120 24" fill="none"><path d="M2 12h96" stroke="{color}" '
            f'stroke-width="5" stroke-linecap="round"/>'
            f'<path d="M92 3l22 9-22 9z" fill="{color}"/></svg>')


def build_html():
    return f"""<!doctype html><html lang="it"><head><meta charset="utf-8">
<style>{CSS}</style></head><body><div class="page">
<img class="deco" src="art/icon-capsule.png" style="width:56px;left:-6px;top:250px;transform:rotate(-24deg)">
<img class="deco" src="art/icon-tablet.png" style="width:48px;right:2px;top:300px;transform:rotate(16deg)">
<img class="deco" src="art/icon-molecule.png" style="width:70px;right:-6px;top:150px;opacity:.7">
<img class="deco" src="art/icon-molecule.png" style="width:62px;left:-10px;top:604px;opacity:.65">
<img class="deco" src="art/icon-capsule.png" style="width:50px;right:6px;top:660px;transform:rotate(30deg)">
<img class="deco" src="art/icon-tablet.png" style="width:46px;left:4px;top:1010px;transform:rotate(-12deg)">
<img class="deco" src="art/icon-molecule.png" style="width:64px;right:-4px;top:1000px;opacity:.7">
<img class="deco" src="art/icon-capsule.png" style="width:52px;left:2px;top:430px;transform:rotate(38deg)">
<img class="deco" src="art/icon-tablet.png" style="width:44px;right:8px;top:470px;transform:rotate(-18deg)">
<img class="deco" src="art/icon-capsule.png" style="width:50px;left:0px;top:880px;transform:rotate(-40deg)">
<img class="deco" src="art/icon-tablet.png" style="width:42px;right:4px;top:840px;transform:rotate(22deg)">

<div class="eyebrow"><b></b>Capitolo 8 &middot; Farmacocinetica vs Farmacodinamica</div>
<h1>Cinetica <i>vs</i> <em>Dinamica</em></h1>

<div class="panel a">
  <h2>FARMACOCINETICA</h2>
  <div class="rule"><s></s>farmaco + movimento<s></s></div>
  <div class="q">Che cosa fa il corpo al farmaco.</div>
  <div class="scene">
    <div class="fig"><div class="disc av"><img src="cut/av-point.png" alt=""></div>
      <div class="tag">organismo</div></div>
    <div class="fig"><div class="disc"><img src="cut/capsule-scared.png" alt=""></div>
      <div class="tag">farmaco</div></div>
    <div class="arrow"><span>Azione</span>{arrow('#24499b')}</div>
  </div>
  <div class="foot">Assorbimento + Distribuzione + Metabolismo + Escrezione (ADME)</div>
</div>

<div class="panel b">
  <h2>FARMACODINAMICA</h2>
  <div class="rule"><s></s>farmaco + effetto<s></s></div>
  <div class="q">Che cosa fa il farmaco al corpo.</div>
  <div class="scene">
    <div class="fig"><div class="disc"><img src="cut/capsule-strong.png" alt=""></div>
      <div class="tag">farmaco</div></div>
    <div class="fig"><div class="disc av"><img src="cut/av-wave.png" alt=""></div>
      <div class="tag">organismo in risposta</div></div>
    <div class="arrow"><span>Azione</span>{arrow('#2f897d')}</div>
  </div>
  <div class="foot">Effetto terapeutico, effetto farmacologico e reazione avversa</div>
</div>
</div></body></html>"""


async def render():
    from playwright.async_api import async_playwright
    from PIL import Image
    f = os.path.join(ROOT, "_cinetica.html")
    open(f, "w", encoding="utf-8").write(build_html())
    async with async_playwright() as pw:
        b = await pw.chromium.launch()
        pg = await b.new_page(viewport={"width": W, "height": H}, device_scale_factor=SCALE)
        await pg.goto("file:///" + f.replace("\\", "/"))
        await pg.wait_for_timeout(700)
        png = await pg.screenshot(clip={"x": 0, "y": 0, "width": W, "height": H})
        im = Image.open(io.BytesIO(png)).convert("RGB")
        im = im.resize((1405, 1874), Image.LANCZOS)
        out = os.path.join(SITE, "amostras", "cinetica-x-dinamica.webp")
        im.save(out, "WEBP", quality=90, method=6)
        im.save(os.path.join(ROOT, "opciones", "cinetica-x-dinamica.png"))
        print("OK", im.size, os.path.getsize(out) // 1024, "KB")
        await b.close()


if __name__ == "__main__":
    if not os.path.exists(os.path.join(ART, "capsule-scared.png")):
        cut()
    asyncio.run(render())
