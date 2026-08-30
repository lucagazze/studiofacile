# -*- coding: utf-8 -*-
"""Favicon / iconos / og-image de Studio Facile a partir del avatar nuevo.
Nada de fondos oscuros ni transparencias: todo sobre crema (#f8f6f1).
"""
import os, io, asyncio
from PIL import Image

ROOT = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(ROOT)
BRAND = os.path.join(SITE, "brand")
os.makedirs(BRAND, exist_ok=True)

SRC = r"C:\Users\lucag\Downloads\ChatGPT Image 29 ago 2026, 04_38_46 p.m..png"
CREAM = (248, 246, 241)

# ------------------------------------------------------------------ iconos
src = Image.open(SRC).convert("RGB")

# recorte del circulo: bbox de lo que no es blanco puro
gray = src.convert("L")
mask = gray.point(lambda v: 255 if v < 250 else 0)
bbox = mask.getbbox()
disc = src.crop(bbox)
side = max(disc.size)
sq = Image.new("RGB", (side, side), (255, 255, 255))
sq.paste(disc, ((side - disc.width) // 2, (side - disc.height) // 2))

# zoom suave hacia la cara para que se lea a 32 px
z = 1.10
zs = int(side / z)
off = (side - zs) // 2
face = sq.crop((off, off - int(side * .035), off + zs, off + zs - int(side * .035)))

# fondo crema (el disco original es crema, el borde es blanco -> lo unificamos)
def on_cream(im, size, disc=True):
    """Escala, recorta en circulo (para matar las esquinas blancas) y apoya en crema."""
    from PIL import ImageDraw
    ss = size * 4
    base = im.resize((ss, ss), Image.LANCZOS)
    out = Image.new("RGB", (ss, ss), CREAM)
    if disc:
        m = Image.new("L", (ss, ss), 0)
        ImageDraw.Draw(m).ellipse([0, 0, ss - 1, ss - 1], fill=255)
        out.paste(base, (0, 0), m)
    else:
        out.paste(base, (0, 0))
    return out.resize((size, size), Image.LANCZOS)

for size in (32, 48, 96, 192, 512):
    on_cream(face, size).save(os.path.join(BRAND, f"icon-{size}.png"))

on_cream(face, 180).save(os.path.join(BRAND, "apple-touch-icon.png"))

# maskable: contenido al 62 % sobre crema, para que Android pueda recortar
mk = Image.new("RGB", (512, 512), CREAM)
inner = on_cream(face, 318)
from PIL import ImageDraw as _D
_m = Image.new("L", (318, 318), 0); _D.Draw(_m).ellipse([0, 0, 317, 317], fill=255)
mk.paste(inner, (97, 97), _m)
mk.save(os.path.join(BRAND, "icon-512-maskable.png"))

# logo cuadrado
on_cream(face, 1024).save(os.path.join(BRAND, "logo.jpg"), "JPEG", quality=92)

# favicon multi-tamano
ico = on_cream(face, 256)
ico.save(os.path.join(SITE, "favicon.ico"), sizes=[(16, 16), (32, 32), (48, 48), (64, 64)])
print("iconos OK")

# ------------------------------------------------------------------ og
OG_HTML = """<!doctype html><html><head><meta charset="utf-8"><style>
@font-face{font-family:'Poppins';src:url('fonts/Poppins-Medium.ttf');font-weight:500}
@font-face{font-family:'Poppins';src:url('fonts/Poppins-SemiBold.ttf');font-weight:600}
@font-face{font-family:'Poppins';src:url('fonts/Poppins-Bold.ttf');font-weight:700}
@font-face{font-family:'Poppins';src:url('fonts/Poppins-ExtraBold.ttf');font-weight:800}
*{margin:0;padding:0;box-sizing:border-box}
body{width:1200px;height:630px;background:#f8f6f1;font-family:'Poppins',sans-serif;
  position:relative;overflow:hidden}
.b{position:absolute;border-radius:50%;z-index:0}
.txt{position:absolute;left:64px;top:118px;width:600px;z-index:3}
.eb{display:flex;align-items:center;gap:9px;font-size:14px;font-weight:700;
  letter-spacing:5px;text-transform:uppercase;color:#9470a4}
.eb b{width:9px;height:9px;border-radius:50%;background:#c9a8ea}
h1{margin-top:16px;font-size:64px;font-weight:800;line-height:.98;color:#562a5f;
  letter-spacing:-2px}
h1 span{display:block;color:#2f897d}
p{margin-top:20px;font-size:22px;font-weight:600;color:#585755;line-height:1.35}
.chips{margin-top:26px;display:flex;gap:9px;flex-wrap:wrap}
.chip{padding:9px 18px;border-radius:999px;font-size:14px;font-weight:700;color:#2a1733}
.mock{position:absolute;right:-30px;top:44px;width:640px;z-index:2}
.mock img{width:100%;display:block}
</style></head><body>
<div class="b" style="width:300px;height:300px;background:#e4f5ec;left:-90px;top:330px"></div>
<div class="b" style="width:220px;height:220px;background:#f0e6fa;left:470px;top:-70px"></div>
<div class="txt">
  <div class="eb"><b></b>Studio Facile</div>
  <h1>Farmacologia<span>illustrata</span></h1>
  <p>9 moduli illustrati + le interazioni<br>farmacologiche + 2 bonus</p>
  <div class="chips">
    <span class="chip" style="background:#dbc0eb">Fondamenti</span>
    <span class="chip" style="background:#b6e6d0">Farmacocinetica</span>
    <span class="chip" style="background:#b9def8">Interazioni</span>
  </div>
</div>
<div class="mock"><img src="../mockups/hero-kit.webp" alt=""></div>
</body></html>"""


async def main():
    from playwright.async_api import async_playwright
    async with async_playwright() as pw:
        b = await pw.chromium.launch()
        pg = await b.new_page(viewport={"width": 1200, "height": 630}, device_scale_factor=2)
        f = os.path.join(ROOT, "_og.html")
        open(f, "w", encoding="utf-8").write(OG_HTML)
        await pg.goto("file:///" + f.replace("\\", "/"))
        await pg.wait_for_timeout(800)
        png = await pg.screenshot(clip={"x": 0, "y": 0, "width": 1200, "height": 630})
        im = Image.open(io.BytesIO(png)).convert("RGB").resize((1200, 630), Image.LANCZOS)
        im.save(os.path.join(BRAND, "og-image.jpg"), "JPEG", quality=90)
        print("og OK", im.size)
        await b.close()


asyncio.run(main())
