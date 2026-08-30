# -*- coding: utf-8 -*-
"""3 propuestas de portada para cada bonus del Kit.
Salida: build-covers/opciones/*.png  + una hoja comparativa.
"""
import os, io, asyncio, math

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "opciones")
os.makedirs(OUT, exist_ok=True)
W, H, SCALE = 794, 1123, 3

HEAD = ('<div class="grid"></div><div class="halo"></div>'
        '<div class="blob" style="width:250px;height:250px;left:-80px;top:430px"></div>'
        '<div class="blob" style="width:280px;height:280px;right:-90px;top:640px"></div>'
        '<div class="blob" style="width:180px;height:180px;left:-40px;top:900px"></div>')

DECO = ('<img class="deco" src="art/icon-capsule.png" style="width:72px;left:48px;top:392px;transform:rotate(-20deg)">'
        '<img class="deco" src="art/icon-tablet.png" style="width:62px;right:52px;top:424px;transform:rotate(14deg)">'
        '<img class="deco" src="art/icon-molecule.png" style="width:86px;left:20px;top:672px;opacity:.85">'
        '<img class="deco" src="art/icon-molecule.png" style="width:74px;right:24px;top:918px;opacity:.75;transform:scaleX(-1)">')


def shell(theme, body):
    return (f'<!doctype html><html lang="it"><head><meta charset="utf-8">'
            f'<link rel="stylesheet" href="variants.css"></head><body>'
            f'<div class="page {theme}">{HEAD}{DECO}'
            f'<div class="cover">{body}</div></div></body></html>')


def head(badge, l1, l2, sub, plate=True, subplate=False):
    t2 = f'<span class="plate">{l2}</span>' if plate else f'<span class="gold">{l2}</span>'
    sb = (f'<div class="subplate">{sub}</div>' if subplate
          else f'<div class="sub">{sub}</div>')
    return (f'<div class="brandmark"><b></b>Studio Facile<b></b></div>'
            f'<div class="badge">{badge}</div>'
            f'<h1>{l1}{t2}</h1>{sb}')


def chips(items):
    cls = ["g", "m", "s", "p"]
    return ('<div class="chips">' + "".join(
        f'<span class="chip {cls[i % 4]}">{x}</span>' for i, x in enumerate(items)) + '</div>')


def ring(items, core, dotted=True):
    """items: [(kind, value, tone)] sobre la circunferencia."""
    out = [f'<div class="{"dots" if dotted else "solid"}"></div>']
    cx = cy = 300.0
    r = 238.0
    n = len(items)
    for k, (kind, val, tone) in enumerate(items):
        ang = math.radians(-90 + k * (360 / n))
        x, y = cx + r * math.cos(ang) - 62, cy + r * math.sin(ang) - 62
        inner = f'<img src="{val}" alt="">' if kind == "i" else val
        extra = " letter" if kind == "t" else ""
        out.append(f'<div class="node{extra} {tone}" style="left:{x:.0f}px;top:{y:.0f}px">{inner}</div>')
    return f'<div class="ring">{"".join(out)}{core}</div>'


def ring_lbl(items, core):
    out = ['<div class="solid"></div>']
    cx = cy = 300.0
    r = 244.0
    n = len(items)
    for k, (img, nm, tone) in enumerate(items):
        ang = math.radians(-90 + k * (360 / n))
        x, y = cx + r * math.cos(ang) - 66, cy + r * math.sin(ang) - 78
        out.append(f'<div class="nd {tone}" style="left:{x:.0f}px;top:{y:.0f}px">'
                   f'<div class="circ"><img src="{img}" alt=""></div>'
                   f'<div class="lb">{nm}</div></div>')
    return f'<div class="ring">{"".join(out)}{core}</div>'


def crew(pods):
    """pods: [(img, w, left, tag)] alineados abajo."""
    out = ['<div class="disc"></div>']
    for img, w, left, tag in pods:
        out.append(f'<div class="pod" style="left:{left}px;width:{w}px">'
                   f'<img src="{img}" style="width:{w}px" alt="">'
                   f'<div class="tag">{tag}</div></div>')
    return f'<div class="crew">{"".join(out)}</div>'


def lista(rows):
    out = []
    for img, nm, tone in rows:
        out.append(f'<div class="li"><div class="ic {tone}"><img src="{img}" alt=""></div>'
                   f'<div class="nm">{nm}</div></div>')
    return f'<div class="list">{"".join(out)}</div>'


# ============================================================ BONUS 1 (blu)
B1_BADGE, B1_L1, B1_L2 = "Bonus 01", "Termini Chiave di", "Farmacia Clinica"
B1_SUB = "Il glossario dalla A alla Z della pratica clinica"

B1_A = shell("b1", head(B1_BADGE, B1_L1, B1_L2, B1_SUB) + ring(
    [("i", "art/icon-book.png", "t3"), ("t", "A", "t5"), ("i", "art/icon-clipboard.png", "t2"),
     ("t", "Z", "t1"), ("i", "art/icon-magnifier.png", "t6"), ("i", "art/icon-molecule.png", "t3")],
    '<div class="core"><div class="az">A<i>&ndash;</i>Z</div>'
    '<div class="lb">Glossario</div></div>')
    + chips(["Definizioni brevi", "Esempi clinici", "Ordine alfabetico", "Consultazione rapida"]))

B1_B = shell("b1", head(B1_BADGE, B1_L1, B1_L2, "Dalla A alla Z, i termini che devi<br>padroneggiare nella pratica", subplate=True)
             + crew([("art/icon-mortar.png", 252, 0, "Preparazione"),
                     ("art/icon-bottles.png", 300, 197, "Forme e dosi"),
                     ("art/icon-book.png", 252, 442, "Glossario")])
             + '<div class="foot">Oltre 120 termini spiegati in una riga<small>Studio Facile</small></div>')

B1_C = shell("b1", head(B1_BADGE, B1_L1, B1_L2, B1_SUB)
             + '<div class="tiles">'
               '<div class="tile big">A&ndash;Z<small>Glossario</small></div>'
               '<div class="tile">B</div><div class="tile">C</div>'
               '<div class="tile"><img src="art/icon-book.png" alt=""></div>'
               '<div class="tile">D</div>'
               '<div class="tile">E</div><div class="tile">F</div>'
               '<div class="tile"><img src="art/icon-clipboard.png" alt=""></div>'
               '<div class="tile">G</div><div class="tile">H</div>'
               '<div class="tile"><img src="art/icon-magnifier.png" alt=""></div>'
               '<div class="tile">Z</div></div>'
             + chips(["Definizioni brevi", "Esempi clinici", "Consultazione rapida"]))

# ============================================================ BONUS 2 (magenta)
B2_BADGE, B2_L1, B2_L2 = "Bonus 02", "Schede di Ripasso", "Rapido"
B2_SUB = "Le 5 classi che escono pi&ugrave; spesso all'esame"
CLASSI = [("art/icon-bloodflow.png", "Antipertensivi", "t1"),
          ("art/icon-headache.png", "FANS", "t2"),
          ("art/icon-microscope.png", "Antibiotici", "t3"),
          ("art/icon-brain.png", "Benzodiazepine", "t4"),
          ("art/icon-capsule.png", "Oppioidi", "t5")]

B2_A = shell("b2", head(B2_BADGE, B2_L1, B2_L2, B2_SUB) + ring_lbl(
    CLASSI, '<div class="core"><div class="big">5</div><div class="k1">Classi</div>'
            '<div class="lb">Essenziali</div></div>')
    + chips(["Meccanismo d'azione", "Effetti avversi", "Interazioni", "Da stampare"]))

B2_B = shell("b2", head(B2_BADGE, B2_L1, B2_L2, B2_SUB, subplate=True)
             + lista(CLASSI)
             + '<div class="foot">Una scheda per classe, pronta da stampare'
               '<small>Studio Facile</small></div>')


def deck():
    fan = [(4, 96, -11, 1), (140, 62, -6, 2), (276, 44, 0, 3), (412, 62, 6, 2), (548, 96, 11, 1)]
    tones = ["var(--sky)", "var(--lav)", "var(--gold)", "var(--rose)", "var(--mint)"]
    out = []
    for (img, nm, _t), (x, y, rot, z), bg in zip(CLASSI, fan, tones):
        out.append(f'<div class="card" style="left:{x}px;top:{y}px;width:138px;height:300px;'
                   f'transform:rotate({rot}deg);z-index:{z}">'
                   f'<div class="top" style="background:{bg}">Scheda</div>'
                   f'<img src="{img}" alt=""><div class="nm">{nm}</div></div>')
    return f'<div class="deck">{"".join(out)}</div>'


B2_C = shell("b2", head(B2_BADGE, B2_L1, B2_L2, B2_SUB)
             + deck()
             + '<div class="foot">Antipertensivi &middot; FANS &middot; Antibiotici<br>'
               'Benzodiazepine &middot; Oppioidi<small>5 schede pronte da stampare</small></div>')

PAGES = [("bonus1-opcion-A-anillo", B1_A), ("bonus1-opcion-B-personaggi", B1_B),
         ("bonus1-opcion-C-alfabeto", B1_C),
         ("bonus2-opcion-A-anillo", B2_A), ("bonus2-opcion-B-lista", B2_B),
         ("bonus2-opcion-C-schede", B2_C)]


async def main():
    from playwright.async_api import async_playwright
    from PIL import Image
    async with async_playwright() as pw:
        b = await pw.chromium.launch()
        pg = await b.new_page(viewport={"width": W, "height": H}, device_scale_factor=SCALE)
        ims = []
        for name, html in PAGES:
            f = os.path.join(ROOT, f"_v_{name}.html")
            open(f, "w", encoding="utf-8").write(html)
            await pg.goto("file:///" + f.replace("\\", "/"))
            await pg.wait_for_timeout(600)
            png = await pg.screenshot(clip={"x": 0, "y": 0, "width": W, "height": H})
            im = Image.open(io.BytesIO(png)).convert("RGB")
            im.save(os.path.join(OUT, name + ".png"))
            ims.append((name, im))
            print(name, im.size)
        await b.close()

    # hoja comparativa 3 x 2
    from PIL import Image as I, ImageDraw, ImageFont
    tw = 500
    th = int(tw * H / W)
    sheet = I.new("RGB", (tw * 3 + 40, (th + 34) * 2 + 20), (238, 238, 242))
    fnt = ImageFont.truetype(os.path.join(ROOT, "fonts", "Poppins-SemiBold.ttf"), 18)
    d = ImageDraw.Draw(sheet)
    for i, (name, im) in enumerate(ims):
        x = (i % 3) * (tw + 10) + 10
        y = (i // 3) * (th + 34) + 34
        sheet.paste(im.resize((tw, th), I.LANCZOS), (x, y))
        d.text((x + 4, y - 26), name, font=fnt, fill=(30, 30, 40))
    sheet.save(os.path.join(OUT, "_comparativa.png"))
    print("hoja comparativa OK")


asyncio.run(main())
