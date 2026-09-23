# -*- coding: utf-8 -*-
"""
La landing italiana di farmacologia, in francese.

Si traducono SOLO i nodi di testo visibili: markup, classi, script e link
restano identici, così la pagina non cambia di una virgola nell'aspetto.
I prezzi, i nomi dei libri e il link del checkout si sistemano dopo, a mano:
sono decisioni, non traduzioni.

  python _traduci_landing.py index.html fr/pharmacologie.html
"""
import html, json, os, re, sys, time, urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed

MODELLO = os.environ.get("MODELLO_TXT", "gemini-3-flash-preview")
KEY = re.search(r"GEMINI_API_KEY=(\S+)",
                open(os.path.expanduser(r"~\.nano-banana\.env"), encoding="utf-8").read()).group(1).strip('"')

ISTRUZIONI = """Tu traduis les textes d'une page de vente italienne vers le français.

Règles:
- Français de France, ton direct et concret, vocabulaire pharmaceutique exact.
- Tu reçois un objet JSON {"1": "texte", "2": "texte"...}. Tu rends le MÊME objet, mêmes clés,
  avec les textes traduits. Rien d'autre.
- Tu gardes la casse (MAJUSCULES restent en majuscules), la ponctuation et les emoji.
- Tu gardes la longueur : c'est une maquette, un texte 30% plus long casse le bouton.
- Tu ne traduis pas : les noms propres, les marques, les chiffres, les prix, «Studio Facile».
- Les prénoms des témoignages restent tels quels ; les villes italiennes deviennent des villes
  françaises plausibles (Milano → Lyon, Roma → Paris, Napoli → Marseille, Torino → Toulouse…).
- FANS → AINS."""


def chiama(payload, intento=1):
    req = urllib.request.Request(
        f"https://generativelanguage.googleapis.com/v1beta/models/{MODELLO}:generateContent",
        data=json.dumps(payload).encode(), method="POST",
        headers={"x-goog-api-key": KEY, "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=300) as r:
            d = json.load(r)
        return "".join(p.get("text", "") for p in d["candidates"][0]["content"]["parts"])
    except Exception:
        if intento < 6:
            time.sleep(5 * intento)
            return chiama(payload, intento + 1)
        raise


def traduci(lote):
    out = chiama({"contents": [{"parts": [{"text": ISTRUZIONI + "\n\nJSON:\n"
                                           + json.dumps(lote, ensure_ascii=False)}]}],
                  "generationConfig": {"temperature": 0.2, "responseMimeType": "application/json"}})
    fr = json.loads(out)
    assert set(fr) == set(lote), "clés différentes"
    return fr


if __name__ == "__main__":
    entrada, salida = sys.argv[1], sys.argv[2]
    s = open(entrada, encoding="utf-8").read()
    cache = salida + ".cache.json"
    fatti = json.load(open(cache, encoding="utf-8")) if os.path.exists(cache) else {}

    # nodi di testo dentro al body, saltando script e style
    cuerpo_i = s.find("<body")
    trozos, pos = [], cuerpo_i
    for m in re.finditer(r">([^<>]+)<", s[cuerpo_i:]):
        t = m.group(1)
        if t.strip() and not t.strip().startswith(("{", "//", "var ", "function")) and len(t.strip()) > 2:
            trozos.append((cuerpo_i + m.start(1), cuerpo_i + m.end(1), t))
    dentro_script = [(m.start(), m.end()) for m in re.finditer(r"<(script|style)\b.*?</\1>", s, re.S)]
    trozos = [t for t in trozos if not any(a < t[0] < b for a, b in dentro_script)]
    unicos = sorted({t[2].strip() for t in trozos})
    faltan = [t for t in unicos if t not in fatti]
    print(f"textos: {len(unicos)} · a traducir: {len(faltan)}", flush=True)

    LOTE = 25
    lotes = [{str(i + j): t for j, t in enumerate(faltan[i:i + LOTE])} for i in range(0, len(faltan), LOTE)]
    with ThreadPoolExecutor(4) as ex:
        futuri = {ex.submit(traduci, l): l for l in lotes}
        for f in as_completed(futuri):
            try:
                fr = f.result()
            except Exception as e:
                print("ERR lote:", str(e)[:60], flush=True); continue
            for k, v in fr.items():
                fatti[futuri[f][k]] = v
            json.dump(fatti, open(cache, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
            print("ok lote ·", len(fatti), flush=True)

    fuera = []
    for a, b, t in reversed(trozos):
        fr = fatti.get(t.strip())
        if fr:
            s = s[:a] + t.replace(t.strip(), fr) + s[b:]
        else:
            fuera.append(t.strip()[:40])
    s = s.replace('<html lang="it"', '<html lang="fr"', 1)
    open(salida, "w", encoding="utf-8").write(s)
    print(f"escrito {salida} · sin traducir: {len(fuera)}")
    if fuera: print("  quedaron en italiano:", fuera[:10])
