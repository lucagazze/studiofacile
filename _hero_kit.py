# -*- coding: utf-8 -*-
"""El hero de kit: tres tabletas, con la geometría del que ya funciona.

    python _hero_kit.py analisi farmaci

LAS MEDIDAS NO SON A OJO. Salen de medir `hero-kit-v2 (6).webp`, el que
Luca aprobó, columna por columna sobre su canal alfa:

    lienzo        1200 x 892
    central       637 x 890, empieza en x=281 — ocupa todo el alto
    laterales     487 x 680, o sea el 76 % del alto de la central
    izquierda     pegada al borde, tapada desde x=281
    derecha       arranca en x=713, tapada hasta x=918

De ahí sale la sensación que le gusta: la central manda y las otras dos
se asoman apenas. Cuando las laterales se ven enteras —como salió el
primer intento— las tres compiten y no se entiende cuál es el libro.

Las tapas se toman de `Ebooks/`, que es la fuente: la página 1 de cada
PDF es su portada de verdad, así que la imagen del sitio no puede
quedar desincronizada del archivo que recibe el comprador.
"""
import io
import os
import sys

import fitz
from PIL import Image, ImageDraw, ImageFilter

EBOOKS = (r"C:\Users\lucag\Desktop\CLAUDE\Infoproductos\Studio Facile"
          r"\Ebooks")
AQUI = os.path.dirname(os.path.abspath(__file__))

W, H = 1200, 892
CEN = (281, 1, 637, 890)          # x, y, ancho, alto
LAT_W, LAT_H = 487, 680
LAT_Y = (H - LAT_H) // 2
MARCO, RADIO = (26, 30, 38), 26
S = 2                              # se trabaja al doble y se reduce

KITS = {
    "analisi": ["Capire le tue analisi del sangue.pdf",
                "Il Diario dei Tuoi Valori.pdf",
                "Le Domande da Fare al Medico.pdf"],
    "farmaci": ["Capire le medicine che prendi.pdf",
                "La Tua Tabella dei Farmaci.pdf",
                "Il Foglietto Illustrativo Tradotto.pdf"],
    "emogas":  ["Emogas ed Elettroliti Illustrati.pdf",
                "Leggere gli Esami di Laboratorio.pdf",
                "Farmaci in Emergenza.pdf"],
}


def tapa(nombre):
    """La página 1 del PDF, que es la portada real del libro."""
    d = fitz.open(os.path.join(EBOOKS, nombre))
    im = Image.open(io.BytesIO(d[0].get_pixmap(dpi=200).tobytes("png")))
    d.close()
    return im.convert("RGB")


def tableta(img, an, al):
    """La tapa dentro de un marco oscuro de esquinas redondeadas."""
    an, al = an * S, al * S
    b = max(6, round(an * 0.022))          # el bisel
    dentro = img.resize((an - b * 2, al - b * 2), Image.LANCZOS)
    t = Image.new("RGBA", (an, al), (0, 0, 0, 0))
    dd = ImageDraw.Draw(t)
    dd.rounded_rectangle([0, 0, an - 1, al - 1], RADIO * S, fill=MARCO)
    m = Image.new("L", dentro.size, 0)
    ImageDraw.Draw(m).rounded_rectangle(
        [0, 0, dentro.width - 1, dentro.height - 1], RADIO * S - b, fill=255)
    t.paste(dentro, (b, b), m)
    return t


def sombra(t, desenfoque=16):
    s = Image.new("RGBA", t.size, (0, 0, 0, 0))
    ImageDraw.Draw(s).rounded_rectangle(
        [0, 0, t.width - 1, t.height - 1], RADIO * S, fill=(0, 0, 0, 115))
    return s.filter(ImageFilter.GaussianBlur(desenfoque * S))


def hero(kit):
    pdfs = KITS[kit]
    centro, izq, der = [tapa(p) for p in pdfs]
    out = Image.new("RGBA", (W * S, H * S), (0, 0, 0, 0))
    # Primero las laterales, para que la central quede delante.
    for img, x in ((izq, 0), (der, W - LAT_W)):
        t = tableta(img, LAT_W, LAT_H)
        out.alpha_composite(sombra(t), (x * S, (LAT_Y + 8) * S))
        out.alpha_composite(t, (x * S, LAT_Y * S))
    t = tableta(centro, CEN[2], CEN[3])
    out.alpha_composite(sombra(t, 22), (CEN[0] * S, (CEN[1] + 10) * S))
    out.alpha_composite(t, (CEN[0] * S, CEN[1] * S))
    out = out.resize((W, H), Image.LANCZOS)
    dest = os.path.join(AQUI, "mockups", kit, "hero.webp")
    out.save(dest, "WEBP", quality=92, method=6)
    print(f"  {kit}: {out.size} · {os.path.getsize(dest)/1024:.0f} KB")
    return out


if __name__ == "__main__":
    for k in (sys.argv[1:] or list(KITS)):
        hero(k)
