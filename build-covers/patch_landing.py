# -*- coding: utf-8 -*-
"""Solo imagenes: cambia src / width / height y cache-bust de iconos.
NO toca ningun texto de la landing.
"""
import io, os

SITE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IDX = os.path.join(SITE, "index.html")
B = "https://czocbnyoenjbpxmcqobn.supabase.co/storage/v1/object/public/algoritmia-img/studiofacile/"

s = io.open(IDX, encoding="utf-8").read()
orig = s
miss = []


def rep(old, new):
    global s
    if old not in s:
        miss.append(old[:100])
        return
    s = s.replace(old, new)


# ---------------------------------------------- iconos / og (cache-bust v4)
s = s.replace(B + "brand/og-image.jpg", B + "brand/og-image.jpg?v=4")
s = s.replace(B + "favicon.ico", B + "favicon.ico?v=4")
for n in ("32", "48", "192", "512"):
    s = s.replace(B + f"brand/icon-{n}.png", B + f"brand/icon-{n}.png?v=4")
s = s.replace(B + "brand/apple-touch-icon.png", B + "brand/apple-touch-icon.png?v=4")

# ---------------------------------------------- mockups
s = s.replace(B + "mockups/57.webp?v=2", B + "mockups/hero-kit.webp?v=4")
s = s.replace(B + "mockup-combo-amostras.webp?v=1", B + "mockups/combo-amostras.webp?v=4")
s = s.replace(B + "mockup-bonus.webp?v=2", B + "mockups/bonus-1.webp?v=4")
s = s.replace(B + "mockup-bonus-2.webp?v=2", B + "mockups/bonus-2.webp?v=4")
s = s.replace(B + "mockup-combo-entregaveis.webp", B + "mockups/combo-entregaveis.webp?v=4")
s = s.replace(B + "amostras/cinetica-x-dinamica.webp?v=2",
              B + "amostras/cinetica-x-dinamica.webp?v=4")

# dimensiones intrinsecas de los archivos nuevos (el resto del markup queda igual)
rep('alt="Guida Dalla A alla Z" width="700" height="991"',
    'alt="Guida Dalla A alla Z" width="720" height="1000"')
rep('alt="Schede di Ripasso Rapido" width="700" height="992"',
    'alt="Schede di Ripasso Rapido" width="720" height="1000"')
rep('alt="Kit completo: 8 Moduli + 2 Bonus" class="db-mockup" width="1100" height="723"',
    'alt="Kit completo: 8 Moduli + 2 Bonus" class="db-mockup" width="1200" height="886"')
rep('alt="Kit di Farmacologia Illustrata: mockup con pagine di esempio" width="900" height="1560"',
    'alt="Kit di Farmacologia Illustrata: mockup con pagine di esempio" width="1100" height="1620"')

# ---------------------------------------------- anteprime (mismos 4 slots, alt igual)
CAR = [("23", "vie-somministrazione"), ("29", "percorso-farmaco"),
       ("32", "distribuzione"), ("33", "interazioni-warfarin")]
for old, new in CAR:
    rep(f'src="{B}amostras/{old}.webp?v=2"', f'src="{B}amostras/{new}.webp?v=4"')
s = s.replace('class="testimonial-item amostra-item" role="listitem"><img src="'
              + B + 'amostras/', 'class="testimonial-item amostra-item" role="listitem"><img src="'
              + B + 'amostras/')
s = s.replace('width="820" height="1098" loading="lazy" decoding="async"></article>',
              'width="1405" height="1874" loading="lazy" decoding="async"></article>')

# la imagen de la seccion "soluzione" y la del bloque de mappa mental
s = s.replace('alt="Farmacologia Illustrata: mappa visiva di farmacocinetica e farmacodinamica, facile da memorizzare" width="820" height="1098"',
              'alt="Farmacologia Illustrata: mappa visiva di farmacocinetica e farmacodinamica, facile da memorizzare" width="1405" height="1874"')
s = s.replace('alt="Esempio di mappa mentale illustrata" width="820" height="1098"',
              'alt="Esempio di mappa mentale illustrata" width="1405" height="1874"')

io.open(IDX, "w", encoding="utf-8", newline="").write(s)
print("index.html:", "cambiado" if s != orig else "SIN CAMBIOS")
if miss:
    print("NO ENCONTRADO:")
    for m in miss:
        print("  !", m)

# ---------------------------------------------- manifest: solo iconos
MAN = os.path.join(SITE, "site.webmanifest")
m = io.open(MAN, encoding="utf-8").read()
m0 = m
m = m.replace(B + "brand/icon-192.png", B + "brand/icon-192.png?v=4")
m = m.replace(B + "brand/icon-512.png", B + "brand/icon-512.png?v=4")
io.open(MAN, "w", encoding="utf-8", newline="").write(m)
print("site.webmanifest:", "cambiado" if m != m0 else "SIN CAMBIOS")
