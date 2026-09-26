# -*- coding: utf-8 -*-
"""
Quello che la traduzione automatica non poteva decidere, su fr/physique.html.

    python -u _arregla_physique.py

_traduci_landing.py traduce i NODI DI TESTO e basta: e' scritto apposta
cosi', perche' prezzi, nomi dei libri e link del checkout sono decisioni,
non traduzioni. Qui si prendono quelle decisioni.

TRE COSE, E LA PRIMA E' LA PIU' IMPORTANTE.

1. I DUE BONUS NON ESISTONO IN FRANCESE. La landing italiana regala «Le
   Parole della Fisica» e «Ripasso Rapido di Fisica»: in francese quei due
   libri non sono mai stati fatti. Una pagina che li promette vende
   qualcosa che non si puo' consegnare, e il primo che compra se ne
   accorge il giorno stesso. La sezione va via tutta.

   Costa: la versione italiana vende CON i bonus, e senza l'offerta e'
   piu' debole. Farli e' la prossima cosa che conviene, non un dettaglio.

2. IL SYLLABUS E' ITALIANO. «le sette unita' del Syllabus ministeriale di
   Fisica del semestre filtro 2026» e' il programma del MUR. In Francia
   non esiste: il libro copre le basi che la UE3 Biophysique da' per
   acquisite, ed e' quello che la pagina deve dire.

3. GLI ATTRIBUTI NON SONO NODI DI TESTO. title, meta description, og: e
   alt sono rimasti in italiano, e sono esattamente cio' che si legge su
   Google e quando si condivide il link.

Il link del checkout resta da sistemare: punta ancora al kit italiano
perche' il prodotto francese non esiste. Lo si vede in fondo, nel
riepilogo.
"""
import io
import os
import re
import sys

QUI = os.path.dirname(os.path.abspath(__file__))
P = os.path.join(QUI, "fr", "physique.html")

# ------------------------------------------------------------ attributi
ATTRIBUTI = {
    "85 pagine illustrate, 7 parti e 67 capitoli con i conti verificati, "
    "più 2 bonus. Per liceo, test d'ingresso e semestre filtro. 19,90€.":
        "85 pages illustrées, 7 parties et 67 chapitres, chaque calcul "
        "vérifié. Du lycée à la première année "
        "de santé. 19,90€.",
    "85 pagine illustrate con i conti verificati + 2 bonus.":
        "85 pages illustrées, chaque calcul vérifié.",
    "Fisica Illustrata: la fisica spiegata con i disegni | Studio Facile":
        "Physique Illustrée : la physique expliquée en dessins | "
        "Studio Facile",
    "Fisica Illustrata": "Physique Illustrée",
}

# ------------------------------------------------------- frasi da rifare
FRASI = {
    "le sette parti seguono, nello stesso ordine, le sette unità del "
    "Syllabus ministeriale di Fisica del semestre filtro 2026, voce per voce":
        "les sept parties suivent l’ordre où l’on rencontre "
        "ces notions : des outils de base jusqu’aux rayonnements",
    "Syllabus ministeriale di Fisica del semestre filtro 2026":
        "bases de physique attendues en première année de santé",
}


def main():
    h = io.open(P, encoding="utf-8").read()
    antes = len(h)

    # --- 1. via la sezione dei bonus ---------------------------------
    i = h.find("Mais Ce N'est Pas Tout")
    if i > 0:
        ini = h.rfind("<section", 0, i)
        fin = h.find("</section>", i) + len("</section>")
        h = h[:ini] + ("<!-- La sezione dei due bonus e' stata tolta: "
                       "«Le Parole della Fisica» e «Ripasso Rapido» non "
                       "esistono in francese. Quando saranno fatti, si "
                       "rimette. -->\n") + h[fin:]
        print("  tolta la sezione dei bonus (%d caratteri)" % (fin - ini))
    else:
        print("  la sezione dei bonus non c'e' gia' piu'")

    # --- 2. attributi e frasi ----------------------------------------
    n = 0
    for a, b in list(ATTRIBUTI.items()) + list(FRASI.items()):
        if a in h:
            h = h.replace(a, b)
            n += 1
    print("  %d attributi e frasi sistemati" % n)

    # --- 3. le briciole di bonus rimaste nel testo --------------------
    # Solo nel TESTO: le classi CSS che si chiamano .bonus-* non si
    # toccano, cambiarle romperebbe il foglio di stile senza guadagnare
    # niente.
    fuori = 0
    for pat in (r"\s*et les 2 bonus offerts", r"\s*\+ 2 bonus",
                r",? ?avec Le Parole della Fisica et Ripasso Rapido di "
                r"Fisica en cadeau", r"\s*plus 2 bonus"):
        h, k = re.subn(pat, "", h)
        fuori += k
    print("  %d menzioni di bonus tolte dal testo" % fuori)

    io.open(P, "w", encoding="utf-8").write(h)
    print("  %s  (%d -> %d caratteri)" % (P, antes, len(h)))

    # --- 4. cosa resta da decidere a mano -----------------------------
    print("\n  DA SISTEMARE A MANO (sono decisioni, non traduzioni):")
    for m in sorted(set(re.findall(r'https://checkout[^"\']+', h))):
        print("   checkout ->", m)
    resta = [k for k in ("semestre filtro", "Syllabus", "Fisica Illustrata",
                         "Parole della Fisica", "Ripasso Rapido")
             if k in h]
    print("   parole italiane ancora nel file:", resta or "nessuna")


if __name__ == "__main__":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
    main()
