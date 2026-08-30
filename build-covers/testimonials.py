# -*- coding: utf-8 -*-
"""Tarjetas de opinion en italiano.
El texto es la traduccion fiel de los depoimentos reales del sitio en portugues
(farmaciamapeada.com.br). No se inventa ni el contenido ni los nombres:
donde el nombre estaba tapado en la captura original, se indica la fuente.
Salida: depoimentos/it-XX.webp (340x420 @3x)
"""
import os, io, asyncio

ROOT = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(ROOT)
OUT = os.path.join(SITE, "depoimentos")
os.makedirs(OUT, exist_ok=True)
W, H, SCALE = 340, 420, 3

# (texto italiano, nombre, contexto)
T = [
    ("Materiale perfetto, rende molto pi&ugrave; semplice capire la materia.",
     "Daniela", "Materiali per il download"),
    ("Il materiale &egrave; ben spiegato, mi sta piacendo molto. Credo che mi aiuter&agrave; "
     "a ripassare: sono molto soddisfatta.", "Sandra", "Materiali per il download"),
    ("Materiale eccellente. Didattica ottima, resa ancora pi&ugrave; semplice "
     "dalle illustrazioni.", "Fl&aacute;via", "Materiali per il download"),
    ("Sono molto soddisfatto dei contenuti: i materiali sono di qualit&agrave; eccellente.",
     "Sander", "Materiali per il download"),
    ("Materiale impeccabile e facile da capire. Bellissimo!",
     "Marcella", "Materiali per il download"),
    ("Sto adorando il materiale: molto didattico e ben spiegato.",
     "Regis", "Materiali per il download"),
    ("L&rsquo;ho usato il semestre scorso e lo user&ograve; molto anche in questo. "
     "Lo adoro: contenuto facile da capire.", "Maria", "Materiali per il download"),
    ("Materiale eccellente. L&rsquo;investimento &egrave; valso la pena.",
     "Sebasti&atilde;o", "Materiali per il download"),
    ("Materiali molto buoni. Nessuna scusa per non studiare.",
     "Julliane", "Materiali per il download"),
    ("Ottimo materiale, complimenti! Il contenuto &egrave; meraviglioso.",
     "Marcelo", "Messaggio su WhatsApp"),
    ("Sono al primo anno di Farmacia e i riassunti mi stanno aiutando moltissimo.",
     "Studente di Farmacia", "Messaggio su WhatsApp"),
    ("Non avevo mai comprato da Instagram, volevo solo una conferma. Il materiale mi &egrave; "
     "piaciuto moltissimo, complimenti!", "Commento", "Instagram"),
    ("Materiale eccellente: ho comprato il PDF e l&rsquo;ho fatto stampare in copisteria.",
     "Commento", "Instagram"),
]

CSS = """
@font-face{font-family:'Poppins';src:url('fonts/Poppins-Regular.ttf');font-weight:400}
@font-face{font-family:'Poppins';src:url('fonts/Poppins-Medium.ttf');font-weight:500}
@font-face{font-family:'Poppins';src:url('fonts/Poppins-SemiBold.ttf');font-weight:600}
@font-face{font-family:'Poppins';src:url('fonts/Poppins-Bold.ttf');font-weight:700}
@font-face{font-family:'Poppins';src:url('fonts/Poppins-ExtraBold.ttf');font-weight:800}
*{margin:0;padding:0;box-sizing:border-box}
html,body{background:#e9e9ee}
.card{position:relative;width:340px;height:420px;background:#fff;border-radius:26px;
  font-family:'Poppins',sans-serif;padding:30px 28px;display:flex;flex-direction:column;
  box-shadow:0 12px 30px rgba(28,29,46,.10);overflow:hidden}
.card:before{content:"";position:absolute;left:0;right:0;top:0;height:7px;
  background:linear-gradient(90deg,#dbc0eb,#b6e6d0,#b9def8,#fec7a9)}
.q{position:absolute;right:22px;top:22px;font-size:74px;line-height:1;font-weight:800;
  color:#f0e6fa}
.stars{position:relative;font-size:17px;letter-spacing:2px;color:#f5a623;margin-top:6px}
.txt{position:relative;margin-top:16px;flex:1;font-size:16.5px;line-height:1.52;
  font-weight:500;color:#2a2b3d}
.who{position:relative;display:flex;align-items:center;gap:12px;padding-top:16px;
  border-top:2px solid #f1eef7}
.av{flex:0 0 44px;width:44px;height:44px;border-radius:50%;display:flex;align-items:center;
  justify-content:center;font-size:18px;font-weight:800;color:#4a2a63;background:#f0e6fa}
.nm{font-size:15.5px;font-weight:800;color:#562a5f;line-height:1.2}
.nm span{display:block;margin-top:2px;font-size:11.5px;font-weight:600;color:#8b8794;
  letter-spacing:.2px}
"""

TONES = ["#f0e6fa", "#e4f5ec", "#e6f1fc", "#fde9dd", "#fdeaee"]


def page(txt, nm, ctx, i):
    ini = nm[0] if nm not in ("Commento",) else "&ldquo;"
    tone = TONES[i % len(TONES)]
    return f"""<!doctype html><html lang="it"><head><meta charset="utf-8">
<style>{CSS}</style></head><body>
<div class="card">
  <div class="q">&rdquo;</div>
  <div class="stars">&#9733;&#9733;&#9733;&#9733;&#9733;</div>
  <div class="txt">&ldquo;{txt}&rdquo;</div>
  <div class="who">
    <div class="av" style="background:{tone}">{ini}</div>
    <div class="nm">{nm}<span>{ctx}</span></div>
  </div>
</div></body></html>"""


async def main():
    from playwright.async_api import async_playwright
    from PIL import Image, ImageDraw, ImageFont
    ims = []
    async with async_playwright() as pw:
        b = await pw.chromium.launch()
        pg = await b.new_page(viewport={"width": W, "height": H}, device_scale_factor=SCALE)
        for i, (txt, nm, ctx) in enumerate(T, 1):
            f = os.path.join(ROOT, f"_t{i:02d}.html")
            open(f, "w", encoding="utf-8").write(page(txt, nm, ctx, i))
            await pg.goto("file:///" + f.replace("\\", "/"))
            await pg.wait_for_timeout(400)
            png = await pg.screenshot(clip={"x": 0, "y": 0, "width": W, "height": H})
            im = Image.open(io.BytesIO(png)).convert("RGB")
            p = os.path.join(OUT, f"it-{i:02d}.webp")
            im.save(p, "WEBP", quality=92, method=6)
            ims.append(im)
            print(f"it-{i:02d}", im.size, os.path.getsize(p) // 1024, "KB")
        await b.close()

    cols, tw = 5, 300
    th = int(tw * H / W)
    rows = (len(ims) + cols - 1) // cols
    sh = Image.new("RGB", (cols * (tw + 10) + 10, rows * (th + 10) + 10), (233, 233, 238))
    for i, im in enumerate(ims):
        sh.paste(im.resize((tw, th), Image.LANCZOS),
                 (10 + (i % cols) * (tw + 10), 10 + (i // cols) * (th + 10)))
    sh.save(os.path.join(ROOT, "opciones", "_testimonianze.png"))
    print("hoja OK")


asyncio.run(main())
