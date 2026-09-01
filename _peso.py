# -*- coding: utf-8 -*-
"""Misura quello che la pagina scarica davvero, non quello che c'è su disco."""
import asyncio, os, urllib.parse
from playwright.async_api import async_playwright

PAGINA = "file:///C:/Users/lucag/Desktop/studiofacile/index.html"


async def main():
    async with async_playwright() as pw:
        br = await pw.chromium.launch()
        pg = await br.new_page(viewport={"width": 1280, "height": 900})
        visti = {}

        def su_risposta(r):
            u = r.url
            if u.startswith("file:"):
                p = urllib.parse.unquote(u[8:])
                if os.path.exists(p):
                    visti[u] = os.path.getsize(p)
            else:
                visti.setdefault(u, 0)

        pg.on("response", su_risposta)
        await pg.goto(PAGINA)
        await pg.wait_for_timeout(2500)
        # scorre tutta la pagina: le immagini lazy si caricano solo così
        for f in range(1, 12):
            await pg.evaluate(f"window.scrollTo(0, document.body.scrollHeight*{f}/11)")
            await pg.wait_for_timeout(700)
        await pg.wait_for_timeout(2500)

        locali = {u: s for u, s in visti.items() if u.startswith("file:")}
        remoti = [u for u in visti if not u.startswith("file:")]
        tot = sum(locali.values())
        print(f"  risorse locali: {len(locali)}   peso: {tot/1e6:.2f} MB")
        print(f"  risorse remote: {len(remoti)} (CDN, non misurabili da file://)")
        for u, s in sorted(locali.items(), key=lambda x: -x[1])[:14]:
            print(f"    {s//1024:>5} KB  {os.path.basename(urllib.parse.unquote(u))[:56]}")
        for u in remoti[:8]:
            print(f"    remoto     {u[:78]}")
        await br.close()


asyncio.run(main())
