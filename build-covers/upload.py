# -*- coding: utf-8 -*-
"""Sube los assets nuevos a Supabase Storage (bucket algoritmia-img, prefijo studiofacile/)."""
import os, re, sys, mimetypes, urllib.request

SITE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENV = r"C:\Users\lucag\Desktop\CLAUDE\creattia\.env.local"
PROJ = "czocbnyoenjbpxmcqobn"
BUCKET = "algoritmia-img"
PREFIX = "studiofacile/"

key = re.search(r'SUPABASE_SERVICE_ROLE_KEY="([^"]+)"', open(ENV, encoding="utf-8").read()).group(1)

FILES = [
    "mockups/hero-kit.webp", "mockups/combo-entregaveis.webp",
    "mockups/bonus-1.webp", "mockups/bonus-2.webp", "mockups/combo-amostras.webp",
    "amostras/vie-somministrazione.webp", "amostras/percorso-farmaco.webp",
    "amostras/distribuzione.webp", "amostras/nefrone.webp",
    "amostras/cinetica-x-dinamica.webp", "amostras/interazioni-warfarin.webp",
    "amostras/interazioni-ibuprofene.webp",
    "brand/icon-32.png", "brand/icon-48.png", "brand/icon-96.png",
    "brand/icon-192.png", "brand/icon-512.png", "brand/icon-512-maskable.png",
    "brand/apple-touch-icon.png", "brand/og-image.jpg", "brand/logo.jpg",
    "favicon.ico",
]

ok = fail = 0
for rel in FILES:
    p = os.path.join(SITE, rel.replace("/", os.sep))
    if not os.path.exists(p):
        print("FALTA", rel); fail += 1; continue
    data = open(p, "rb").read()
    ct = mimetypes.guess_type(p)[0] or "application/octet-stream"
    if p.endswith(".webp"): ct = "image/webp"
    if p.endswith(".ico"): ct = "image/x-icon"
    url = f"https://{PROJ}.supabase.co/storage/v1/object/{BUCKET}/{PREFIX}{rel}"
    req = urllib.request.Request(url, data=data, method="POST", headers={
        "apikey": key, "Authorization": f"Bearer {key}",
        "Content-Type": ct, "x-upsert": "true", "Cache-Control": "public, max-age=31536000",
    })
    try:
        with urllib.request.urlopen(req, timeout=120) as r:
            print(r.status, rel, len(data) // 1024, "KB"); ok += 1
    except Exception as e:
        body = e.read().decode("utf-8", "ignore")[:200] if hasattr(e, "read") else str(e)
        print("ERR", rel, body); fail += 1

print(f"\n{ok} subidos, {fail} con error")
