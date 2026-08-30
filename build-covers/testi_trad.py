# -*- coding: utf-8 -*-
"""Capturas originales (reales, en portugues) + traduccion al italiano debajo,
al estilo del 'Vedi traduzione' de Instagram.
Salida: depoimentos/trad-XX.webp
"""
import os, io, asyncio

ROOT = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(ROOT)
SRC = r"C:\Users\lucag\AppData\Local\Temp\claude\c--Users-lucag--claude\e3da63f2-bcd8-476c-8cf6-ca58f137297a\scratchpad\dep"
OUT = os.path.join(SITE, "depoimentos")
os.makedirs(OUT, exist_ok=True)
W, H, SCALE = 800, 1200, 2

# traduccion literal de cada mensaje de la captura
TRAD = {
    1: ["Ottimo materiale 💖",
        "Buongiorno! Ma figurati!! È solo che non avevo mai comprato da Instagram, "
        "volevo solo una conferma!! Il materiale mi è piaciuto moltissimo, complimenti 👏",
        "L'ho adorato, il materiale è fatto molto bene, ne è valsa l'attesa 👏 "
        "complimenti per l'impegno, andrai lontano 🙏"],
    2: ["E i tuoi schemi sono ottimi: sono al primo anno di Farmacia e mi stanno aiutando molto",
        "Daniela — Materiale perfetto, rende molto più semplice capire la materia.",
        "Marcelo — Ottimo materiale! Complimenti!!!",
        "Jesilene — Materiale molto buono, contenuto ben spiegato e facile da capire.",
        "Sebastião — Materiale eccellente, l'investimento è valso la pena.",
        "Sandra — Grazie mille. Userò questo materiale in questo semestre. Fatto molto bene.",
        "Julliane — Materiali molto buoni. Nessuna scusa per non studiare. 😌"],
    3: ["Sandra — Il materiale è ben spiegato, mi sta piacendo molto, credo che mi aiuterà "
        "a ripassare: sono molto soddisfatta.",
        "Maria — L'ho adorato",
        "Lucas — Ottimo materiale",
        "Flávia — Materiale eccellente. Didattica ottima, resa ancora più semplice "
        "dalle illustrazioni.",
        "Sander — Sono molto soddisfatto dei contenuti, i materiali sono di qualità eccellente.",
        "Rayane — Perfetto! Complimenti!",
        "Lorena — Ho adorato il materiale",
        "Marcella — Materiale impeccabile e facile da capire!! Bellissimo!!"],
    4: ["Regis — Sto adorando il mio materiale. Molto didattico e ben spiegato",
        "Anelise — Il team è super disponibile!!",
        "Maria — L'ho usato il semestre scorso e lo userò molto anche in questo, "
        "lo sto adorando: contenuto facile da capire."],
    5: ["Buongiorno!!! Tranquillo, grazie per avermi contattata. Sto studiando i contenuti e "
        "finora li ho trovati super interessanti e ben spiegati, dettagliati, diretti: "
        "questo aiuta a capire!!!!! Continua a fare altri contenuti, aiuta tantissimo "
        "chi studia e sta iniziando adesso, come me 🙏",
        "Mi è piaciuto molto il contenuto 🎉"],
    6: ["Buongiorno... grazie mille... ho ricevuto il materiale... ottimo... complimenti... "
        "materiale molto facile da capire.",
        "Ciao, grazie mille, ho adorato i riassunti, mi aiuteranno moltissimo."],
    7: ["Ho adorato la tua pagina!!! Complimenti! Ho appena comprato il corso!!!! "
        "Ho ricevuto, tanta gratitudine per te 👏",
        "Buon pomeriggio, sei riuscita ad accedere al materiale?",
        "Buon pomeriggio — Sì, ci sono riuscita. Grazie mille ❤️",
        "Contenuti meravigliosi ❤️"],
    8: ["Tutto a posto, grazie mille ❤️ *ps. il materiale mi è già piaciuto tantissimo",
        "Che lavoro impeccabile, davvero",
        "Buonasera Dottore. Io e mia moglie abbiamo comprato uno dei suoi materiali, "
        "davvero top 👏"],
    9: ["Volevo solo dirti che sto adorando il contenuto ❤️ Molto facile da capire 🙏 "
        "Complimenti 👏",
        "Wow, ho appena visto il materiale ed è incredibile, complimenti, continua così "
        "e andrai lontano 🤩",
        "Di sicuro mi aiuterà molto a imparare questa materia 😘"],
    10: ["Materiale eccellente, complimenti per il tuo lavoro 👏 E il contenuto è meraviglioso 👏",
         "Grazie!!!! 💗 il materiale è meraviglioso! complimenti",
         "Materiale fantastico!!! Complimenti!!!"],
    11: ["Ho trovato il vostro lavoro davvero top 💛",
         "Grazie, sono già riuscita a scaricare tutto il materiale. L'ho adorato 😍👏",
         "Il tuo materiale vale ogni centesimo!"],
    12: ["L'ho comprato e lo consiglio tantissimo. 🤍🧠",
         "L'ho comprato e lo consiglio, eccellente!",
         "Grazie, che Dio ti benedica. Materiale incredibile. 😍",
         "L'ho appena comprato, meraviglioso",
         "Ho adorato il contenuto, l'ho comprato e lo consiglio"],
    13: ["Materiale eccellente, ho comprato il PDF e l'ho fatto stampare in copisteria",
         "L'ho già comprato e lo consiglio molto",
         "@lorene_silva1 che bello saperlo Lorene, sono felicissimo di questo riscontro, "
         "grazie per la fiducia!",
         "Sono io che ringrazio, per aver reso l'apprendimento più semplice e con tanta cura!!! "
         "Compratelo ragazzi, ci semplificherà davvero la vita!!!!"],
}

FILES = {i: f"d{i}.webp" for i in range(1, 14)}

CSS = """
@font-face{font-family:'Poppins';src:url('fonts/Poppins-Regular.ttf');font-weight:400}
@font-face{font-family:'Poppins';src:url('fonts/Poppins-Medium.ttf');font-weight:500}
@font-face{font-family:'Poppins';src:url('fonts/Poppins-SemiBold.ttf');font-weight:600}
@font-face{font-family:'Poppins';src:url('fonts/Poppins-Bold.ttf');font-weight:700}
*{margin:0;padding:0;box-sizing:border-box}
html,body{background:#e9e9ee}
.card{position:relative;width:800px;height:1200px;background:#fff;border-radius:26px;
  overflow:hidden;font-family:'Poppins',sans-serif;display:flex;flex-direction:column;
  box-shadow:0 12px 30px rgba(28,29,46,.10)}
.shot{width:100%;height:800px;background:#fff;display:flex;align-items:center;
  justify-content:center;overflow:hidden}
.shot img{width:100%;height:100%;object-fit:contain;display:block}
.trad{flex:1;background:#f7f5fb;border-top:2px solid #ece7f4;padding:20px 28px 22px;
  display:flex;flex-direction:column}
.lbl{display:flex;align-items:center;gap:9px;font-size:13px;font-weight:700;
  letter-spacing:1.6px;text-transform:uppercase;color:#8b6fa5}
.lbl b{width:16px;height:3px;border-radius:2px;background:#c9a8ea}
.lst{margin-top:12px;display:flex;flex-direction:column;gap:7px;overflow:hidden}
.lst p{position:relative;padding-left:16px;color:#33344a;line-height:1.4;font-weight:500}
.lst p:before{content:"";position:absolute;left:0;top:.55em;width:6px;height:6px;
  border-radius:50%;background:#c9a8ea}
"""


def card(img, lines, fs):
    body = "".join(f"<p>{l}</p>" for l in lines)
    return f"""<!doctype html><html lang="it"><head><meta charset="utf-8">
<style>{CSS}.lst p{{font-size:{fs}px}}</style></head><body>
<div class="card">
  <div class="shot"><img src="shots/{img}" alt=""></div>
  <div class="trad">
    <div class="lbl"><b></b>Traduzione in italiano</div>
    <div class="lst">{body}</div>
  </div>
</div></body></html>"""


async def main():
    from playwright.async_api import async_playwright
    from PIL import Image
    import shutil
    sh = os.path.join(ROOT, "shots")
    os.makedirs(sh, exist_ok=True)
    for i, f in FILES.items():
        shutil.copy(os.path.join(SRC, f), os.path.join(sh, f))

    ims = []
    async with async_playwright() as pw:
        b = await pw.chromium.launch()
        pg = await b.new_page(viewport={"width": W, "height": H}, device_scale_factor=SCALE)
        for i in sorted(FILES):
            lines = TRAD[i]
            n = sum(len(x) for x in lines)
            fs = 17 if n < 220 else 15.5 if n < 380 else 14 if n < 520 else 12.6
            f = os.path.join(ROOT, f"_tr{i:02d}.html")
            open(f, "w", encoding="utf-8").write(card(FILES[i], lines, fs))
            await pg.goto("file:///" + f.replace("\\", "/"))
            await pg.wait_for_timeout(400)
            png = await pg.screenshot(clip={"x": 0, "y": 0, "width": W, "height": H})
            im = Image.open(io.BytesIO(png)).convert("RGB")
            p = os.path.join(OUT, f"trad-{i:02d}.webp")
            im.save(p, "WEBP", quality=90, method=6)
            ims.append(im)
            print(f"trad-{i:02d}", im.size, os.path.getsize(p) // 1024, "KB", f"fs={fs}")
        await b.close()

    cols, tw = 5, 300
    th = int(tw * H / W)
    rows = (len(ims) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * (tw + 10) + 10, rows * (th + 10) + 10), (233, 233, 238))
    for i, im in enumerate(ims):
        sheet.paste(im.resize((tw, th), Image.LANCZOS),
                    (10 + (i % cols) * (tw + 10), 10 + (i // cols) * (th + 10)))
    sheet.save(os.path.join(ROOT, "opciones", "_testimonianze_trad.png"))
    print("hoja OK")


asyncio.run(main())
