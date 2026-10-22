# -*- coding: utf-8 -*-
"""
Landing de «Nursing Fundamentals Made Visual» (EE. UU., NCLEX-PN) en https://nursing.studiofacilebook.com
— 22/10/2026 (BRIEF_OFERTAS_2310.md #10), copia de landing_acupuncture_us.py (motor landing_kit.py en inglés,
USD 27 sin tachado). Índice real del PDF (Nursing-US struttura.py, 52 páginas), bonus «Practical Nursing Practice
Tests» y «Nursing Terms Made Visual». Ayuda de estudio: no habilita, no garantiza aprobar, sin afiliación NCSBN.
Sin reseñas, autor ni cifras inventadas. Píxel «Nursing US» 1508189954693679. Fotos: foto_nur_us.py.

  python -u scripts/landing_nursing_us.py --asset
  python -u scripts/landing_nursing_us.py
"""
import io
import os
import re
import shutil
import sys

import landing_kit as K
import landing_us as U

PIXEL = "1508189954693679"   # «Nursing US» (único píxel de la página; mismo que el checkout)
CHECKOUT = "https://nursing.studiofacilebook.com/checkout"
CARPETA = "nursing"
B1, B2 = "Practical Nursing Practice Tests", "Nursing Terms Made Visual"
TIT = "Nursing Fundamentals Made Visual"
PDF = r"C:\Users\lucag\Desktop\CLAUDE\Infoproductos\Nursing-US\Nursing Fundamentals Made Visual.pdf"
N_PAG = 52

ASSET = dict(
    proyecto="Nursing-US",
    pdf=PDF,
    lang="en", b1_tit=B1, b2_tit=B2,
    anteprime=[18, 23, 3, 36, 29, 41, 15, 49],
    collage=[4, 10, 14, 21, 26, 31, 39, 47],
    og=("#26745a", "#1f2547"),
    questo=("Words you will finally", "understand",
            ["SBAR", "Standard precautions", "Donning", "Doffing", "Orthostatic", "Braden scale", "Fowler",
             "Sims", "PRN", "STAT", "Subcutaneous", "Intradermal", "Delirium", "Delegation", "Clinical judgment"]),
)

ANTE_TIT = ["Putting on and taking off PPE", "Blood pressure", "The LPN and LVN role",
            "The rights of medication administration", "Positioning in bed", "Injection basics", "Hand hygiene",
            "Setting priorities"]
PARTI = [
    ("I", "The Practical Nurse", 3, 8, [
        "The LPN and LVN role", "The nursing process", "Therapeutic communication", "Documentation and SBAR",
        "Legal and ethical basics", "Delegation and teamwork"]),
    ("II", "Patient Safety", 9, 13, [
        "Patient identification", "Preventing falls", "Restraints and alternatives", "Fire and electrical safety",
        "Body mechanics"]),
    ("III", "Infection Control", 14, 19, [
        "The chain of infection", "Hand hygiene", "Standard precautions", "Transmission-based precautions",
        "Putting on and taking off PPE", "Sharps and sterile technique"]),
    ("IV", "Vital Signs and Data Collection", 20, 27, [
        "Body temperature", "Pulse and heart rate", "Respirations and breathing", "Blood pressure",
        "Pulse oximetry and oxygen", "Pain assessment", "Head-to-toe data collection", "Practice: Parts 1 to 4"]),
    ("V", "Basic Care and Comfort", 28, 35, [
        "Hygiene and the bed bath", "Positioning in bed", "Transfers and walking aids", "Preventing pressure injuries",
        "Nutrition and safe feeding", "Intake and output", "Urinary elimination and catheter care", "Basic wound care"]),
    ("VI", "Medication Administration", 36, 42, [
        "The rights of medication administration", "Reading a medication order", "Dosage calculation basics",
        "Routes of administration", "Giving oral medications", "Injection basics", "Preventing medication errors"]),
    ("VII", "Special Care", 43, 46, [
        "Caring for older adults", "Mental health basics", "End-of-life care", "Emergencies and BLS"]),
    ("VIII", "The NCLEX-PN", 47, 50, [
        "The NCLEX-PN test plan", "How NCLEX questions work", "Setting priorities", "Practice: Parts 5 to 8"]),
]
CHIUSURA = [("Answers explained", 51), ("The book on one page", 52)]


def C_():
    n_top = sum(len(x[4]) for x in PARTI)
    return dict(
        lang="en", slug="nursing", slug_img="nursing-us", content_id="nursing-fundamentals-made-visual",
        og_locale="en_US", url="https://nursing.studiofacilebook.com",
        dest=os.path.join(K.SITO, CARPETA, "index.html"),
        titolo=TIT,
        checkout=CHECKOUT, pixel=PIXEL,
        prezzo=27, tot=None, val_b1=0, val_b2=0,
        b1=B1, b2=B2,
        n_pag=N_PAG,
        h1="The Easiest Way to Understand Nursing Fundamentals <mark>Explained with Pictures</mark>",
        sub=f"Safety, infection control, PPE, vital signs, basic care, medication administration, dosage calculation basics and the NCLEX-PN test plan: here every topic fits on one page, drawn and explained. {N_PAG} illustrated pages, with 40 practice questions explained.",
        cta_hero="I WANT TO UNDERSTAND NURSING FUNDAMENTALS",
        stats=[("One topic per page", "a drawing that explains it and the key idea in the box"),
               (f"{N_PAG} illustrated pages", "8 parts, from safety to the NCLEX-PN"),
               ("40 practice questions", "with every answer explained")],
        verbo_pagine="You Will Learn",
        anteprime_sub="One topic per page, with a big drawing, four short boxes and the key idea at the bottom. Take a look inside:",
        anteprime=[("nursing-us_%02d" % (i + 1), t) for i, t in enumerate(ANTE_TIT)],
        problema=dict(
            h2="It Is Not That Nursing Fundamentals Are Hard. It Is That Nobody Showed Them to You in Pictures.",
            prima=["Donning and doffing order, droplet or airborne, Fowler or Sims, PRN or STAT... you have read it ten times, but it does not stick.",
                   "...and <strong>every textbook gives you hundreds of pages of dense text</strong>."],
            img="nursing-us_01", alt=ANTE_TIT[0],
            dopo=["Here, a skill fits on <strong>one page</strong>: the big drawing shows it, four boxes explain it.",
                  "And the box at the bottom tells you <strong>the one idea to keep</strong>."],
            chiusa="First you see it. Then you remember it."),
        confronto=dict(
            h2="Stop drowning in textbook pages:",
            bad=["Walls of dense text", "Steps and orders that blur together",
                 "Facts you forget the day after"],
            bad_alt="A heavy nursing textbook",
            good=["Every topic drawn", "Safety, care and medications explained simply",
                  "You remember it because you saw it"],
            img="nursing-us_02", alt=ANTE_TIT[1]),
        sommario_h2=f"Take a look at the 8 parts and {n_top} topics",
        sommario_sub=f"The practical nurse, safety, infection control, vital signs, basic care, medications, special care and the NCLEX-PN: {N_PAG} pages, all illustrated",
        parti=PARTI,
        chiusura=CHIUSURA,
        chiusura_tit="Answers and Final Review",
        descr={
            "I": "The LPN and LVN role and scope of practice, the nursing process, therapeutic communication, documentation and SBAR, legal and ethical basics, delegation and teamwork.",
            "II": "Two patient identifiers, fall prevention, restraints and their alternatives, RACE and PASS for fire safety, and body mechanics.",
            "III": "The chain of infection, hand hygiene, standard precautions, contact, droplet and airborne precautions, putting on and taking off PPE, sharps and sterile technique.",
            "IV": "Temperature, pulse, respirations, blood pressure, pulse oximetry and oxygen, pain and head-to-toe data collection, with adult reference ranges and 20 practice questions.",
            "V": "Hygiene and the bed bath, positioning, transfers and walking aids, pressure injuries, safe feeding, intake and output, catheter care and basic wound care.",
            "VI": "The rights of medication administration, reading an order, dosage calculation basics, routes, oral medications, injection basics and preventing medication errors.",
            "VII": "Older adults and delirium, mental health basics, end-of-life care, and emergencies and BLS.",
            "VIII": "The NCLEX-PN test plan by client needs, how adaptive and Next Generation questions work, priority rules, and 20 more practice questions.",
        },
        moduli_nota="At the end: every practice answer explained and the whole book on one page.",
        soluzione=dict(
            prima=["Instead of rereading pages and pages of text the night before a test...",
                   "...you see <strong>each skill drawn step by step</strong>: what to do, in which order and why."],
            img="nursing-us_03", alt=ANTE_TIT[2],
            dopo=["And the fundamentals become <strong>pictures you can recall</strong> in the skills lab, in clinicals and on test day."],
            riassunto=f"It is not &ldquo;just another PDF&rdquo;. It is <strong>8 parts and {n_top} illustrated topics</strong>, with <strong>40 practice questions and the answers explained</strong>, plus <strong>the whole book on one page</strong>."),
        bonus_testi=[
            ("<strong>Ten short tests by topic, sixty original questions</strong>, from the nurse's role to safety, care, medications and priorities, <strong>with every answer explained</strong> and a score sheet.",
             "It comes with the book."),
            ("<strong>Prefixes, suffixes, body directions and positions</strong>, the abbreviations you will read on orders and <strong>the official do-not-use list</strong>, explained with drawings.",
             "It comes with the book."),
        ],
        consegna=f"{TIT} and the two free books arrive by email as PDFs. One payment, no subscription.",
        perchi=[
            ("nursing-us-student.webp", "Nursing student studying an illustrated book at a kitchen table",
             "You are in a PN or LVN program",
             "Review each topic in minutes before class, the skills lab or clinicals."),
            ("nursing-us-career.webp", "Man reading an illustrated book on a sofa",
             "You are thinking about nursing",
             "See what practical nurses really learn, one clear page at a time."),
            ("nursing-us-exam.webp", "Student reviewing practice questions in an illustrated book",
             "You are getting ready for the NCLEX-PN",
             "The fundamentals, the test plan and practice questions with every answer explained."),
        ],
        recap=[f"{TIT}: {N_PAG} illustrated pages in 8 parts",
               "40 practice questions with the answers explained and the whole book on one page",
               f"Bonus 1: &ldquo;{B1}&rdquo;, 60 questions in 10 tests (free)",
               f"Bonus 2: &ldquo;{B2}&rdquo;, word parts, abbreviations and the do-not-use list (free)",
               "PDFs by email, to read on your phone or print",
               "30-day guarantee"],
        finale=["You do not have to memorize the PPE order by repeating it in your head.",
                "You do not have to get lost in a thousand-page textbook.",
                "And you definitely do not have to <strong>study nursing fundamentals without pictures</strong>."],
        faq=[
            ("Is it for beginners?",
             "Yes. It starts with the role of the practical nurse and goes topic by topic, one page at a time, with simple words and big drawings."),
            ("What does it cover?",
             "The LPN and LVN role, the nursing process, communication, documentation, safety, infection control and PPE, vital signs, basic care, the principles of medication administration with dosage calculation basics, special care, BLS, and the NCLEX-PN test plan, plus 40 practice questions."),
            ("Will it get me through the NCLEX-PN?",
             "No book can guarantee that. It helps you understand and review the fundamentals; your nursing program and steady practice prepare you. It is not affiliated with or endorsed by the NCSBN."),
            ("Will it give me a license or a certification?",
             "No. Licenses are issued by each state board of nursing. The book is a study aid."),
            ("Does it replace my program or facility procedures?",
             "No. Always follow your instructors, your facility's policies and procedures and your state's scope of practice. Dosage examples are generic exercises, not prescriptions."),
            ("Are the practice questions real exam questions?",
             "No. They were written for this book. No official exam questions are included."),
            ("How do I get it?", "By email, right after you buy: three PDFs you can read on your phone, tablet or computer."),
            ("Is it a subscription?", "No. One payment of $27, and the three PDFs are yours."),
            ("Can I print it?", "Yes, as many times as you want, for yourself."),
            ("What if I don't like it?", "You have 30 days: if a file does not open, if the content is not what this page describes, if you were charged twice or the download never arrived, write to us and we refund you."),
        ],
        schema_descr=f"{N_PAG} illustrated pages of nursing fundamentals for practical nursing students: safety, infection control, vital signs, basic care, medication administration and NCLEX-PN prep. With two free books.",
        meta_title=f"{TIT}: safety, vital signs, basic care and medications explained with drawings | Studio Facile",
        meta_descr=f"Nursing fundamentals for LPN and LVN students explained with pictures: safety, PPE, vital signs, basic care, medication administration and the NCLEX-PN test plan. {N_PAG} illustrated pages, practice tests and nursing terms. $27, 30-day guarantee.",
        og_descr="Understand nursing fundamentals the easy way: one topic per page, explained with pictures.",
        footer_nota="Independent study material for practical nursing students. It does not replace a nursing program, instructors, facility policies or the scope of practice set by your state board of nursing, it does not license anyone and it cannot guarantee passing the NCLEX-PN. NCLEX-PN is a registered trademark of the NCSBN; this material is not affiliated with or endorsed by the NCSBN. Infection control follows CDC guidance; the do-not-use list follows The Joint Commission. The practice questions are original.",
    )


LEGAL = dict(
    carpeta=CARPETA, nombre_libro={"main": TIT},
    css_extra=":root{--navy:#1f2547;--navy-d:#141933;--tinta:#1f2547;--rojo:#26745a;--rojo-d:#1d5c47}",
    legal=dict(
        what="""<p>Illustrated study material about nursing fundamentals for practical nursing students in the
United States, delivered as downloadable PDF files. Nothing is shipped physically.</p>
<div class="caja"><p><strong>This is study material, not a course, a license or a guarantee.</strong>
It does not replace a nursing program, your instructors or your facility's policies and procedures, it does not
license anyone and it cannot guarantee passing the NCLEX-PN. It is not affiliated with or endorsed by the NCSBN.
The practice questions were written for this material; they are not official exam questions.</p></div>""",
        liability="""<p>We take care that the content is accurate and based on recognized sources (CDC, The Joint
Commission, and the NCSBN test plan as a concept). Even so, the material is educational: always follow your program,
your facility's procedures and your state's scope of practice. Dosage examples are generic exercises, not
prescriptions. To the extent allowed by law, our liability is limited to what you paid.</p>""",
        support_faq="""<h2>The most common questions</h2>
<h3>&ldquo;The email never arrived&rdquo;</h3>
<p>Check spam and promotions, and search for <em>info@studiofacilebook.com</em>.
If it is not there, write to us with the email address you used and we resend it.</p>
<h3>&ldquo;Can I print it?&rdquo;</h3>
<p>Yes, as many times as you want, for yourself.</p>
<h3>&ldquo;Does it give me a license or certification?&rdquo;</h3>
<p>No. It is independent study material about nursing fundamentals.</p>"""),
)


def _sin_preventa(d):
    t = os.path.join(d, "terms.html")
    s = io.open(t, encoding="utf-8").read()
    s = re.sub(r"\s*<li>If a title is sold before it is finished[^<]*</li>", "", s)
    io.open(t, "w", encoding="utf-8", newline="\n").write(s)
    r = os.path.join(d, "refund-policy.html")
    s = io.open(r, encoding="utf-8").read()
    s = re.sub(r"<h2>Pre-sale titles</h2>\s*<p>.*?</p>\s*", "", s, flags=re.S)
    io.open(r, "w", encoding="utf-8", newline="\n").write(s)


def main():
    if "--asset" in sys.argv:
        import asset_1110
        asset_1110.corre("nursing-us", ASSET)
        return
    C = C_()
    d = os.path.join(K.SITO, CARPETA)
    os.makedirs(d, exist_ok=True)
    K.genera(C)
    h = io.open(C["dest"], encoding="utf-8").read()
    h = h.replace("currency: 'USD', value: 19.90,", "currency: 'USD', value: %s," % C["prezzo"])
    io.open(C["dest"], "w", encoding="utf-8", newline="\n").write(h)
    ids = set(re.findall(r"fbq\('init',\s*'(\d+)'\)", h)) | set(re.findall(r"tr\?id=(\d+)", h))
    if h.count("fbq('init'") != 1 or ids != {PIXEL}:
        raise SystemExit(f"pixel: esperaba solo {PIXEL}, hay {ids}")
    U.legales(LEGAL)
    _sin_preventa(d)
    shutil.copy(os.path.join(K.SITO, "foodsafety", "vercel.json"), os.path.join(d, "vercel.json"))
    for f in ("galleria.js", "site.webmanifest"):
        shutil.copy(os.path.join(K.SITO, f), os.path.join(d, f))
    g = os.path.join(d, "galleria.js")
    s = io.open(g, encoding="utf-8").read()
    io.open(g, "w", encoding="utf-8", newline="\n").write(s.replace("currency: 'EUR'", "currency: 'USD'"))
    gi = os.path.join(d, ".gitignore")
    if not os.path.exists(gi):
        open(gi, "w").write(".vercel\n")


if __name__ == "__main__":
    main()
