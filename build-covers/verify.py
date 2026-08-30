# -*- coding: utf-8 -*-
"""QA de la landing: imagenes rotas, scroll horizontal y capturas 390/768/1280."""
import os, asyncio, sys

SITE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SHOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "_qa")
os.makedirs(SHOT, exist_ok=True)
TARGET = sys.argv[1] if len(sys.argv) > 1 else "index.html"


async def main():
    from playwright.async_api import async_playwright
    async with async_playwright() as pw:
        b = await pw.chromium.launch()
        for w, h in ((390, 844), (768, 1024), (1280, 900)):
            pg = await b.new_page(viewport={"width": w, "height": h})
            errs = []
            pg.on("console", lambda m: errs.append(m.text) if m.type == "error" else None)
            await pg.goto("file:///" + os.path.join(SITE, TARGET).replace("\\", "/"),
                          wait_until="networkidle")
            await pg.wait_for_timeout(1500)
            await pg.evaluate("""async () => {
              for (const img of document.images) { try { await img.decode(); } catch(e){} }
              window.scrollTo(0, document.body.scrollHeight);
            }""")
            await pg.wait_for_timeout(1200)
            broken = await pg.evaluate(
                "[...document.images].filter(i=>!i.complete||i.naturalWidth===0).map(i=>i.currentSrc||i.src)")
            over = await pg.evaluate(
                "document.documentElement.scrollWidth - document.documentElement.clientWidth")
            wide = await pg.evaluate("""() => {
              const w = document.documentElement.clientWidth, out = [];
              document.querySelectorAll('*').forEach(e=>{
                const r = e.getBoundingClientRect();
                if (r.width > 0 && (r.right > w + 2 || r.left < -2))
                  out.push(e.tagName + '.' + (e.className||'').toString().slice(0,40));
              });
              return [...new Set(out)].slice(0, 10);
            }""")
            print(f"--- {TARGET} @{w}px  overflow={over}px  broken={len(broken)}")
            for x in broken[:8]:
                print("   BROKEN", x)
            if over > 0:
                for x in wide:
                    print("   WIDE", x)
            for e in errs[:5]:
                print("   CONSOLE", e[:140])
            await pg.screenshot(path=os.path.join(SHOT, f"{TARGET}-{w}.png"), full_page=(w == 1280))
            await pg.close()
        await b.close()


asyncio.run(main())
