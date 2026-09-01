# -*- coding: utf-8 -*-
"""
Rimpicciolisce le immagini alla misura in cui vengono davvero mostrate.

Servire un file da 1405 px in uno spazio da 319 px non aggiunge nitidezza:
aggiunge byte. Si tiene il doppio della larghezza mostrata, che è quanto
serve a uno schermo ad alta densità, e non di più.

Le copie originali restano in `_originali/`, così la riduzione si può
rifare o annullare.
"""
import os, shutil

from PIL import Image

BASE = os.path.dirname(os.path.abspath(__file__))
ORIG = os.path.join(BASE, "_originali")

# file -> larghezza mostrata sul sito (misurata nel browser)
MOSTRATO = {
    "Img-Leandro.webp": 266,
    "amostras/p57-warfarin.webp": 319,
    "amostras/p37-recettori.webp": 319,
    "amostras/p47-ipersensibilita.webp": 319,
    "amostras/p48-metabolizzatori.webp": 319,
    "amostras/p52-interazione.webp": 319,
    "amostras/p41-curva-dose.webp": 386,
    "amostras/p23-adme.webp": 600,
    "depoimentos/testimonio-1.webp": 319,
    "depoimentos/testimonio-2.webp": 319,
    "depoimentos/testimonio-3.webp": 319,
    "depoimentos/testimonio-4.webp": 319,
    "depoimentos/testimonio-5.webp": 319,
    "depoimentos/testimonio-6.webp": 319,
    "depoimentos/testimonio-7.webp": 319,
    "depoimentos/testimonio-8.webp": 319,
    "depoimentos/testimonio-9.webp": 319,
    "personagens/estudante.webp": 315,
    "personagens/recem-formado.webp": 315,
    "personagens/profissional.webp": 315,
}

DENSITA = 2          # schermi ad alta densità
MARGINE = 1.1        # un filo di margine per riquadri che crescono


def ottimizza():
    os.makedirs(ORIG, exist_ok=True)
    prima = dopo = 0
    for rel, largh in MOSTRATO.items():
        f = os.path.join(BASE, rel)
        if not os.path.exists(f):
            print(f"  manca: {rel}")
            continue
        salva = os.path.join(ORIG, rel.replace("/", "_"))
        if not os.path.exists(salva):
            shutil.copy2(f, salva)

        im = Image.open(salva)
        obiettivo = int(largh * DENSITA * MARGINE)
        prima += os.path.getsize(salva)
        if im.width <= obiettivo:
            dopo += os.path.getsize(f)
            print(f"  {rel:<38} già piccola")
            continue
        modo = "RGBA" if im.mode in ("RGBA", "LA", "P") and "A" in im.getbands() else "RGB"
        o = im.convert(modo).resize(
            (obiettivo, round(obiettivo * im.height / im.width)), Image.LANCZOS)
        o.save(f, "WEBP", quality=84, method=6)
        dopo += os.path.getsize(f)
        print(f"  {rel:<38} {im.width:>5} -> {obiettivo:<5} "
              f"{os.path.getsize(salva)//1024:>4} -> {os.path.getsize(f)//1024:>4} KB")
    print(f"\n  totale: {prima/1e6:.2f} MB -> {dopo/1e6:.2f} MB "
          f"({(1-dopo/prima)*100:.0f}% in meno)")


if __name__ == "__main__":
    ottimizza()
