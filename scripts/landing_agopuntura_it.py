# -*- coding: utf-8 -*-
"""
Genera it/agopuntura.html — la landing di «L'Agopuntura Illustrata» (17/10/2026, BRIEF_OFERTAS_1710.md #6).

Motore: landing_kit.py (senza autore, senza numeri di studenti, senza testimonianze).
Sommario = indice vero del libro (Infoproductos\\Agopuntura-IT\\pages.py, 75 pagine, 9 parti).
Bonus: Le Tavole dei Meridiani e Le Domande dell'Agopuntura (copertine in Agopuntura-IT\\bonus).
Niente plazo. In Italia l'agopuntura è atto medico (FNOMCeO): libro di studio e di cultura, NON abilita, non insegna a
praticare sugli altri, nessuna promessa di cura, «non sostituisce il medico». Pixel «Agopuntura IT» (1406685284468306),
lo stesso del checkout. Foto «per chi è»: fotogrammi Mixkit (Free License).

  python -u scripts/landing_agopuntura_it.py --asset
  python -u scripts/landing_agopuntura_it.py
"""
import sys

import landing_kit as K

PIXEL = "1406685284468306"   # «Agopuntura IT»
CHECKOUT = "https://www.studiofacilebook.com/it/agopuntura/cassa"
B1, B2 = "Le Tavole dei Meridiani", "Le Domande dell'Agopuntura"

ASSET = dict(
    proyecto="Agopuntura-IT",
    pdf=r"C:\Users\lucag\Desktop\CLAUDE\Infoproductos\Agopuntura-IT\L'Agopuntura Illustrata.pdf",
    lang="it", b1_tit=B1, b2_tit=B2,
    anteprime=[17, 31, 9, 47, 38, 5, 60, 52],
    collage=[8, 14, 21, 24, 35, 43, 56, 65],
    og=("#2f7a6e", "#1f5a52"),
    questo=("Meridiani, punti e misure da imparare", "a memoria",
            ["LU 7", "LI 4", "ST 36", "SP 6", "PC 6", "GV 20", "CV 12", "cun", "yin e yang", "qi", "zang-fu",
             "cinque movimenti", "Taiyin", "Yangming", "Shaoyang", "vaso governatore", "vaso concezione",
             "punti shu", "yuan e luo", "moxa", "coppette", "reperi"]),
)

C = dict(
    lang="it", slug="agopuntura", slug_img="agopuntura-it", content_id="agopuntura-it", og_locale="it_IT",
    titolo="L'Agopuntura Illustrata",
    checkout=CHECKOUT, pixel=PIXEL,
    prezzo=19.90, tot=91.00, val_b1=17.90, val_b2=14.90,   # tot = il «Totale» del checkout (barrato 58,20 + bonus)
    b1=B1, b2=B2,
    n_pag=75,
    h1="Il Modo Più Facile per Studiare l'Agopuntura <mark>Con Ogni Meridiano e Ogni Punto Disegnato!</mark>",
    sub="I 12 meridiani, il vaso governatore e il vaso concezione, i punti con la localizzazione in cun, yin e yang, i cinque movimenti, la storia e che cosa dice la ricerca: sui manuali sono pagine fitte di sigle. Qui ogni argomento sta in una pagina sola, con il disegno. 75 pagine illustrate.",
    cta_hero="VOGLIO STUDIARLA CON I DISEGNI",
    stats=[("Un argomento per pagina", "il disegno ti mostra dove, il testo fa da didascalia"),
           ("75 pagine illustrate", "9 parti, dalle basi della medicina cinese alla ricerca"),
           ("Fonti serie", "standard OMS 2008 dei punti, Cochrane, NCCIH e OMS")],
    verbo_pagine="Studierai",
    anteprime_sub="Un argomento per pagina, il disegno che ti mostra il percorso e i riquadri con quello che serve sapere:",
    anteprime=[("agopuntura-it_01", "Il cun proporzionale"),
               ("agopuntura-it_02", "Il meridiano del Pericardio"),
               ("agopuntura-it_03", "I cinque movimenti"),
               ("agopuntura-it_04", "I punti di gamba e piede"),
               ("agopuntura-it_05", "Il vaso governatore"),
               ("agopuntura-it_06", "Duemila anni di storia"),
               ("agopuntura-it_07", "Digitopressione: le regole"),
               ("agopuntura-it_08", "Gli aghi")],
    problema=dict(
        h2="Non È Che Non Ti Entra. È Che Nessuno Te l'Ha Mai Fatto Vedere.",
        prima=["Hai letto tre volte «PC 6: 2 cun sopra la piega del polso, fra i tendini». Chiudi il manuale...",
               "...e <strong>non sai più dove cade, né quanto è lungo un cun</strong>. Erano solo sigle in fila."],
        img="agopuntura-it_01", alt="Il cun proporzionale disegnato sul corpo",
        dopo=["Qui il cun è <strong>disegnato sul corpo</strong>: dalla piega del gomito alla piega del polso sono 12 cun, su chiunque.",
              "E sotto c'è quello che non si dimentica: <strong>il cun non è una misura in centimetri, ma una parte del corpo di quella persona</strong>."],
        chiusa="Prima vedi dove. Poi lo ricordi da solo."),
    confronto=dict(
        h2="Smetti di imparare a memoria sigle che non riesci a immaginare:",
        bad=["Pagine e pagine di sigle e numeri", "Percorsi dei meridiani senza un disegno",
             "Davanti a una tavola, non sai da dove cominciare"],
        bad_alt="Una lista di sigle di punti e meridiani da imparare a memoria",
        good=["Ogni meridiano disegnato", "Un argomento per pagina, con i punti chiave in una tabella",
              "Lo ricordi perché l'hai visto"],
        img="agopuntura-it_02", alt="Il meridiano del Pericardio disegnato con i suoi punti"),
    sommario_h2="Dai un'occhiata alle 9 parti e ai 58 capitoli",
    sommario_sub="Le basi della medicina tradizionale cinese, il corpo e le misure, i 14 meridiani, i punti, gli strumenti, la digitopressione, la ricerca e la legge: 75 pagine, tutte illustrate",
    parti=[
        ("1", "Le basi della MTC", 4, 12,
         ["Duemila anni di storia in Cina", "L'agopuntura arriva in Occidente", "Qi, sangue e liquidi", "Yin e yang",
          "I cinque movimenti", "Organi e visceri: gli zang-fu", "Le cause degli squilibri", "I quattro metodi d'esame"]),
        ("2", "Orientarsi sul corpo", 13, 19,
         ["Il sistema dei meridiani", "Nomi, codici e sigle", "Il giro del qi nei meridiani", "Il cun proporzionale",
          "Il cun delle dita", "I punti di repere"]),
        ("3", "I 12 meridiani", 20, 35,
         ["Polmone (LU)", "Intestino crasso (LI)", "Stomaco (ST) · testa e tronco", "Stomaco (ST) · gamba e piede",
          "Milza (SP)", "Cuore (HT)", "Intestino tenue (SI)", "Vescica (BL) · testa e schiena",
          "Vescica (BL) · gamba e piede", "Rene (KI)", "Pericardio (PC)", "Triplice riscaldatore (TE)",
          "Vescicola biliare (GB) · testa e tronco", "Vescicola biliare (GB) · gamba e piede", "Fegato (LR)"]),
        ("4", "I vasi straordinari", 36, 39,
         ["Gli otto vasi straordinari", "Il vaso governatore (GV)", "Il vaso concezione (CV)"]),
        ("5", "I punti più usati", 40, 50,
         ["I cinque punti shu antichi", "Punti yuan e punti luo", "Shu del dorso e mu del davanti", "Gli otto punti hui",
          "I punti più usati: testa e viso", "I punti più usati: braccio e mano", "I punti più usati: gamba e piede",
          "I punti più usati: tronco e schiena", "I punti fuori dai meridiani", "Punti e zone che chiedono cautela"]),
        ("6", "Gli strumenti", 51, 58,
         ["Gli aghi", "Come lavora il medico agopuntore", "Sicurezza ed effetti indesiderati",
          "Elettroagopuntura e auricoloterapia", "La moxibustione", "La coppettazione", "Tuina e gua sha"]),
        ("7", "Digitopressione", 59, 65,
         ["Digitopressione: le regole", "Quando non farla", "Mani e polsi", "Testa, viso e nuca", "Gambe e piedi",
          "Una routine di cinque minuti"]),
        ("8", "Ricerca e legge", 66, 69,
         ["Come si studia l'agopuntura", "Che cosa dicono le revisioni", "L'agopuntura in Italia"]),
    ],
    chiusura=[("Domande di pratica 1-20", 71), ("Domande di pratica 21-40", 72), ("Soluzioni spiegate 1-20", 73),
              ("Soluzioni spiegate 21-40", 74), ("Il ripasso", 75)],
    chiusura_tit="Esercitati",
    descr={
        "1": "Duemila anni di storia, l'arrivo in Occidente, qi, yin e yang, i cinque movimenti, gli organi zang-fu, le cause degli squilibri e i quattro metodi d'esame della tradizione.",
        "2": "Il sistema dei meridiani, i nomi e i codici OMS dei punti, il giro del qi, il cun proporzionale, il cun delle dita e i punti di repere.",
        "3": "I 12 meridiani principali uno per uno: percorso disegnato, coppia, ore della tradizione e punti chiave con la localizzazione secondo lo standard OMS 2008.",
        "4": "Gli otto vasi straordinari, il vaso governatore e il vaso concezione, con il percorso e i punti.",
        "5": "Le categorie dei testi classici (shu antichi, yuan, luo, shu del dorso, mu, hui) e i punti più citati zona per zona, con i punti e le zone che chiedono cautela.",
        "6": "Aghi, moxa, coppette, elettroagopuntura, orecchio, tuina e gua sha spiegati come concetto: come lavora il medico agopuntore, sicurezza ed effetti indesiderati.",
        "7": "La digitopressione come auto-massaggio leggero per adulti in buona salute: le regole, quando non farla e una routine di cinque minuti.",
        "8": "Come si studia l'agopuntura, che cosa dicono le revisioni (Cochrane, NCCIH) e che cosa dice la legge italiana.",
    },
    moduli_nota="In fondo al libro, 40 domande di pratica con le soluzioni spiegate e il ripasso in una pagina.",
    soluzione=dict(
        prima=["Invece di perderti fra sigle e numeri sulla tavola dei meridiani...",
               "...apri la pagina e trovi <strong>ST 36: 3 cun sotto il ginocchio, un dito a lato della cresta della tibia</strong>, con il disegno."],
        img="agopuntura-it_04", alt="I punti più usati di gamba e piede disegnati",
        dopo=["E i meridiani, le misure in cun, i cinque movimenti, la storia e la ricerca diventano <strong>disegni e tabelle che si leggono a colpo d'occhio</strong>. Smetti di rileggere e cominci a capire."],
        riassunto="Non è &ldquo;l'ennesimo manuale&rdquo;. Sono <strong>9 parti e 58 capitoli illustrati</strong>, e in fondo <strong>40 domande di pratica con le soluzioni spiegate e il ripasso</strong>."),
    sfoglia=[[], []],
    bonus_testi=[
        ("Le tavole <strong>da stampare e appendere</strong>: i 12 meridiani principali, il vaso governatore e il vaso concezione, ognuno con il percorso e i punti principali, più la tavola del cun.", ""),
        ("Le domande di studio <strong>con le risposte spiegate</strong>, per ripassare basi, meridiani, punti, storia e ricerca.", ""),
    ],
    consegna="L'Agopuntura Illustrata ti arriva via email in PDF, e via email ricevi anche i due volumi in regalo. Pagamento unico, senza rate né costi nascosti.",
    perchi=[
        ("agopuntura-it-studio.webp", "Ragazzo che studia a un tavolo con libri e quaderni",
         "Studi medicina o una professione sanitaria",
         "I meridiani, i punti e le misure in cun, un argomento per pagina, per capire che cos'è l'agopuntura di cui senti parlare."),
        ("agopuntura-it-giardino.webp", "Ragazza che scrive su un quaderno seduta su una panchina in un giardino",
         "Ti appassiona la medicina tradizionale cinese",
         "Yin e yang, i cinque movimenti, la storia e i testi classici spiegati con i disegni, senza perderti fra le sigle."),
        ("agopuntura-it-lanterne.webp", "Lanterne rosse accese fra le canne di bambù",
         "Vuoi sapere che cosa c'è di vero",
         "Che cosa dicono le revisioni Cochrane e NCCIH, dove ci sono segnali e dove no, e che cosa dice la legge italiana."),
    ],
    recap=["L'Agopuntura Illustrata: 75 pagine illustrate in 9 parti, dalle basi della medicina cinese alla ricerca",
           "40 domande di pratica con le soluzioni spiegate e il ripasso",
           "Bonus 1: &ldquo;Le Tavole dei Meridiani&rdquo; (valore 17,90€)",
           "Bonus 2: &ldquo;Le Domande dell'Agopuntura&rdquo; (valore 14,90€)",
           "PDF via email, da leggere sul telefono o stampare",
           "Garanzia di 30 giorni"],
    finale=["Non devi rileggere la stessa riga sperando che stavolta il punto ti resti in mente.",
            "Non devi imparare a memoria sigle e percorsi che non riesci a immaginare.",
            "E di sicuro <strong>non devi più perderti davanti a una tavola dei meridiani</strong>."],
    faq=[
        ("Come riceverò il materiale?", "Dopo l'acquisto ricevi un'email con L'Agopuntura Illustrata in PDF ad alta risoluzione, da leggere sul telefono o stampare. Via email ricevi anche i due volumi in regalo, Le Tavole dei Meridiani e Le Domande dell'Agopuntura."),
        ("Il pagamento è mensile o unico?", "Pagamento unico di 19,90€. Nessuna rata, nessun abbonamento."),
        ("Mi abilita a fare l'agopuntura?", "No. È un libro di studio e di cultura: non è un corso, non rilascia attestati e non abilita a nulla. In Italia l'agopuntura è un atto medico, riservato al medico e all'odontoiatra con formazione specifica: il libro non insegna a praticarla sugli altri, come la moxibustione e la coppettazione."),
        ("L'agopuntura cura i disturbi?", "Il libro non promette cure e non sostituisce il medico, la diagnosi né le terapie. Riporta che cosa dicono le revisioni (Cochrane, NCCIH, OMS): dove ci sono segnali e dove no. Per qualunque disturbo rivolgiti al medico, e non sospendere mai le cure prescritte."),
        ("E la digitopressione?", "Il libro la descrive come auto-massaggio leggero di punti sicuri, per adulti in buona salute, con le regole e i casi in cui non farla. Non è una terapia: se un disturbo è nuovo, forte o non passa, vai dal medico."),
        ("A chi serve?", "A chi studia medicina o una professione sanitaria e vuole capire l'agopuntura, a chi è appassionato di medicina tradizionale cinese e a chi vuole sapere che cosa c'è di vero. Guarda il sommario qui sopra per vedere gli argomenti."),
        ("Su quali fonti si basa?", "Sullo standard OMS del 2008 per la localizzazione dei punti, sulle linee guida OMS su formazione e sicurezza, sulle schede del NCCIH e sulle revisioni Cochrane, e per l'Italia sulle linee guida FNOMCeO e sull'Accordo Stato-Regioni del 7 febbraio 2013."),
        ("Ci sono domande per allenarsi?", "Sì. In fondo al libro ci sono 40 domande di pratica con le soluzioni spiegate. Sono scritte da noi per ripassare, non sono domande ufficiali di un corso o di un esame."),
        ("Posso stampare il materiale?", "Sì, per uso personale e senza limiti. I PDF sono in alta risoluzione."),
        ("E se non mi piace?", "Hai 30 giorni: se un file non si apre, se il contenuto non è quello descritto, se qualcosa non ti arriva o se ti è stato addebitato due volte, scrivici e ti restituiamo la spesa."),
    ],
    schema_descr="75 pagine illustrate sull'agopuntura e la medicina tradizionale cinese: basi, meridiani, punti con la localizzazione in cun, strumenti come concetto, digitopressione, ricerca e legge italiana. Con due volumi in regalo. Libro di studio e di cultura: non abilita e non sostituisce il medico.",
    meta_title="L'Agopuntura Illustrata: meridiani e punti spiegati con i disegni | Studio Facile",
    meta_descr="I 14 meridiani, i punti in cun, yin e yang, i cinque movimenti, la storia e la ricerca in 75 pagine illustrate, più 2 volumi in regalo. A 19,90€, garanzia 30 giorni.",
    og_descr="L'agopuntura spiegata con i disegni, un argomento per pagina: dalle basi della medicina cinese ai meridiani e alla ricerca.",
    footer_nota="Libro illustrato di studio e di cultura sull'agopuntura e la medicina tradizionale cinese. Non è un corso: non rilascia attestati e non abilita a nulla. In Italia l'agopuntura è un atto medico, riservato al medico e all'odontoiatra con formazione specifica: il libro non insegna a praticarla sugli altri. Non promette cure e non sostituisce il medico. Le domande di pratica sono scritte per questo libro e non sono domande ufficiali. Studio Facile non è affiliato a enti, scuole o autorità.",
)

if __name__ == "__main__":
    if "--asset" in sys.argv:
        import asset_1110
        asset_1110.corre(C["slug_img"], ASSET)
    else:
        import io
        import os
        import re
        K.genera(C)
        h = io.open(os.path.join(K.SITO, "it", "agopuntura.html"), encoding="utf-8").read()
        ids = set(re.findall(r"fbq\('init',\s*'(\d+)'\)", h)) | set(re.findall(r"tr\?id=(\d+)", h))
        bad = [w for w in ("ti abilita", "abilitante", "guarisce", "cura il", "curare il", "attestato valido", "diventa agopuntore")
               if w in h.lower()]
        print("pixel:", ids, "| frasi vietate:", bad)
