# -*- coding: utf-8 -*-
"""Pone el cartel de compra reciente en las landings que no lo tienen.

    python _poner_toast.py analisi farmaci

El mecanismo ya existe en la home: CSS `.sp-toast`, un bloque HTML y un
script que rota una lista de compradores. Las dos landings nuevas se
generaron con el CSS pero SIN el bloque ni el script, así que la clase
estaba definida y no la usaba nadie.

LOS NOMBRES Y LOS TIEMPOS SON LOS DE LA HOME, con los productos
cambiados. No se inventan cifras de ventas ni se dice «17 personas están
viendo esto»: eso ya es otra cosa. Esto muestra compras plausibles del
producto de ESA página, que es lo que el visitante entendería igual si
mirara el pie de un checkout.

EL PRODUCTO TIENE QUE SER EL DE LA PAGINA. Copiar el de la home —«Kit
Completo · 28 Capitoli»— en la landing de análisis sería un cartel que
anuncia la compra de otra cosa, y el que lo lee con atención lo nota.
"""
import io
import re
import sys

BLOQUE = """<div class="sp-toast" id="spToast" role="status" aria-live="polite">
    <button class="sp-close" id="spClose" aria-label="Chiudi">&times;</button>
    <span class="sp-mini"><img id="spShot" src="%(img)s" alt=""></span>
    <div class="sp-txt">
      <span class="sp-name" id="spName">Chiara da Milano</span>
      <span class="sp-prod" id="spProd">%(prod1)s</span>
      <span class="sp-meta"><span class="ok">&#10004; Accesso confermato</span> \
&middot; <span id="spTime">fa 4 minuti</span>
    </div>
  </div>
"""

SCRIPT = """
  <!-- cartel de compra reciente (social proof toast) -->
  <script>
    (function(){
      var buyers = [
        { name: "Chiara da Milano", prod: "%(prod1)s", time: "fa 4 minuti" },
        { name: "Marco da Roma", prod: "%(prod2)s", time: "fa 12 minuti" },
        { name: "Martina da Bologna", prod: "%(prod1)s", time: "fa 18 minuti" },
        { name: "Lorenzo da Napoli", prod: "%(prod2)s", time: "fa 25 minuti" },
        { name: "Sofia da Torino", prod: "%(prod3)s", time: "fa 31 minuti" },
        { name: "Matteo da Firenze", prod: "%(prod2)s", time: "fa 39 minuti" },
        { name: "Camilla da Padova", prod: "%(prod1)s", time: "fa 44 minuti" },
        { name: "Alessandro da Pisa", prod: "%(prod2)s", time: "fa 52 minuti" }
      ];
      var idx = 0;
      var toast = document.getElementById('spToast');
      var spName = document.getElementById('spName');
      var spProd = document.getElementById('spProd');
      var spTime = document.getElementById('spTime');
      var spShot = document.getElementById('spShot');
      var spClose = document.getElementById('spClose');
      var KIT_IMG = "%(img)s";

      if (!toast) return;
      if (spShot) spShot.src = KIT_IMG;

      function showNext() {
        var b = buyers[idx];
        if (spName) spName.textContent = b.name;
        if (spProd) spProd.textContent = b.prod;
        if (spTime) spTime.textContent = b.time;
        if (spShot && spShot.src !== KIT_IMG) spShot.src = KIT_IMG;
        toast.classList.add('show');

        setTimeout(function() {
          toast.classList.remove('show');
        }, 6000);

        idx = (idx + 1) %% buyers.length;
      }

      if (spClose) {
        spClose.addEventListener('click', function(e) {
          e.stopPropagation();
          toast.classList.remove('show');
        });
      }

      setTimeout(function() {
        showNext();
        setInterval(showNext, 18000);
      }, 6000);
    })();
  </script>
"""

CDN = ("https://czocbnyoenjbpxmcqobn.supabase.co/storage/v1/object/public/"
       "algoritmia-img/studiofacile/mockups/%s/hero.webp")

PAGINAS = {
    "analisi": {
        "img": CDN % "analisi",
        "prod1": "Ha acquistato il Kit Analisi del Sangue",
        "prod2": "Kit Analisi &middot; 51 pagine + 2 Bonus",
        "prod3": "Ha sbloccato il Kit Analisi del Sangue",
    },
    "farmaci": {
        "img": CDN % "farmaci",
        "prod1": "Ha acquistato il Kit Le Medicine Che Prendi",
        "prod2": "Kit Medicine &middot; 46 pagine + 2 Bonus",
        "prod3": "Ha sbloccato il Kit Le Medicine Che Prendi",
    },
    "radiografie": {
        "img": CDN % "radiografie",
        "prod1": "Ha acquistato il Kit Radiografie Illustrate",
        "prod2": "Kit Radiografie &middot; 58 pagine + 2 Bonus",
        "prod3": "Ha sbloccato il Kit Radiografie Illustrate",
    },
    "emogas": {
        "img": CDN % "emogas",
        "prod1": "Ha acquistato il Kit Emogas ed Elettroliti",
        "prod2": "Kit Emogas &middot; 45 pagine + 2 Bonus",
        "prod3": "Ha sbloccato il Kit Emogas ed Elettroliti",
    },
}


def main():
    for nombre in (sys.argv[1:] or list(PAGINAS)):
        f = nombre + ".html"
        d = PAGINAS[nombre]
        h = io.open(f, encoding="utf-8").read()
        if "spToast" in h:
            print(f"  {f}: ya lo tiene")
            continue
        if ".sp-toast{" not in h:
            print(f"  {f}: NO tiene el CSS, hay que copiarlo también")
            continue
        # El bloque va donde está en la home: justo antes del banner de la
        # oferta, que es lo primero del body después de la barra.
        m = re.search(r"\n(\s*)<!-- BANNER DE LA OFERTA -->", h)
        if not m:
            print(f"  {f}: no encuentro dónde insertarlo")
            continue
        h = h[:m.start()] + "\n  " + (BLOQUE % d).rstrip() + h[m.start():]
        # El script, al final, antes de cerrar el body.
        i = h.rfind("</body>")
        h = h[:i] + (SCRIPT % d) + "\n" + h[i:]
        io.open(f, "w", encoding="utf-8").write(h)
        print(f"  {f}: puesto")


if __name__ == "__main__":
    main()
