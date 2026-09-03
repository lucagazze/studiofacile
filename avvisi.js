/* =========================================================
   Avvisi social proof — Studio Facile (biblioteca)
   Stesso cartellino dell'index: in alto a sinistra.

   TUTTI I MESSAGGI QUI SOTTO SONO VERIFICABILI.
   Per aggiornarli basta cambiare AVVISI e VENDITE_KIT.
   Se un giorno colleghi le vendite reali del checkout,
   sostituisci l'array AVVISI con i dati dell'API:
   la struttura e' { img, nome, prod, meta, link }.
   ========================================================= */
(function () {
  'use strict';

  // Vendite reali del Kit Completo (pannello del checkout). Aggiornalo ogni tanto.
  var VENDITE_KIT = 110;

  var AVVISI = [
    {
      img: '/avvisi/kit.webp',
      nome: VENDITE_KIT.toLocaleString('it-IT') + ' studenti hanno preso il Kit',
      prod: 'Kit Completo · 28 Capitoli + 2 Bonus',
      meta: 'Il combo più scelto',
      link: '/'
    },
    {
      img: '/avvisi/collezione.webp',
      nome: 'Collezione Completa',
      prod: '5 prontuari clinici · 386 pagine illustrate',
      meta: '27,50€ · un solo acquisto',
      link: '/collezione'
    },
    {
      img: '/avvisi/trio.webp',
      nome: 'Trio Clinico',
      prod: 'Emergenza, Antibiotici e Psicofarmaci',
      meta: '16,70€ · 250 pagine',
      link: '/trio-clinico'
    },
    {
      img: '/avvisi/kit.webp',
      nome: '+11.978 studenti e professionisti',
      prod: 'Usano i materiali di Studio Facile',
      meta: 'Accesso a vita, pagamento unico',
      link: '/'
    }
  ];

  // Ritmo discreto: compare tardi, resta poco, torna di rado e poi smette.
  var PRIMO_RITARDO = 14000;
  var DURATA        = 6000;
  var PAUSA         = 30000;
  var MAX_VOLTE     = 4;

  if (!AVVISI.length) return;
  try { if (sessionStorage.getItem('sf_avvisi_off') === '1') return; } catch (e) {}

  var CSS = [
    '.sp-toast{position:fixed;left:14px;top:14px;z-index:900;',
      'display:flex;align-items:center;gap:12px;',
      'background:#fff;border:1px solid #e4e9ee;border-radius:12px;',
      'padding:10px 14px 10px 10px;max-width:330px;color:#12191f;text-align:left;',
      'box-shadow:0 10px 30px rgba(18,25,31,.22);',
      'opacity:0;visibility:hidden;transform:translateY(-16px) scale(.97);',
      'transition:opacity .45s ease, transform .45s cubic-bezier(.2,.8,.3,1), visibility .45s}',
    '.sp-toast.show{opacity:1;visibility:visible;transform:translateY(0) scale(1)}',
    '.sp-mini{position:relative;flex:0 0 auto;width:66px;height:42px;border-radius:6px;overflow:hidden;',
      'background:#fff;border:1px solid #e4e9ee;box-shadow:0 2px 8px rgba(18,25,31,.14)}',
    '.sp-mini img{width:100%;height:100%;object-fit:contain;display:block;margin:0}',
    '.sp-txt{min-width:0;line-height:1.4}',
    '.sp-name{font-size:13.5px;font-weight:700;color:#12191f;display:block}',
    '.sp-prod{font-size:12px;color:#5b6874;display:block;margin-top:1px;',
      'white-space:nowrap;overflow:hidden;text-overflow:ellipsis}',
    '.sp-meta{font-size:10.5px;color:#98a3ad;display:flex;align-items:center;gap:5px;margin-top:3px}',
    '.sp-meta .ok{color:#28a745;font-weight:700}',
    '.sp-close{position:absolute;top:-10px;right:-10px;width:26px;height:26px;padding:0;line-height:1;',
      'display:flex;align-items:center;justify-content:center;border:1px solid #e0e6eb;border-radius:50%;',
      'background:#fff;color:#8a949e;font-size:16px;font-weight:600;font-family:inherit;cursor:pointer;',
      'box-shadow:0 2px 8px rgba(18,25,31,.14);transition:background .18s,color .18s,transform .18s,border-color .18s}',
    '.sp-close:hover{border-color:#cbd5e1;color:#12191f;transform:scale(1.08)}',
    '.sp-close:active{transform:scale(.96)}',
    '@media (max-width:560px){.sp-toast{left:8px;right:8px;top:10px;max-width:none}}',
    '@media (prefers-reduced-motion:reduce){.sp-toast{transition:none}}'
  ].join('');

  var toast, elImg, elNome, elProd, elMeta, i = 0, volte = 0, tShow, tHide;

  function build() {
    var st = document.createElement('style');
    st.textContent = CSS;
    document.head.appendChild(st);

    toast = document.createElement('a');
    toast.className = 'sp-toast';
    toast.setAttribute('role', 'status');
    toast.setAttribute('aria-live', 'polite');
    toast.innerHTML =
      '<button class="sp-close" type="button" aria-label="Chiudi">&times;</button>' +
      '<span class="sp-mini"><img alt="" width="66" height="42"></span>' +
      '<span class="sp-txt">' +
        '<span class="sp-name"></span>' +
        '<span class="sp-prod"></span>' +
        '<span class="sp-meta"><span class="ok">&#10003;</span><span class="sp-metatxt"></span></span>' +
      '</span>';
    document.body.appendChild(toast);

    elImg = toast.querySelector('.sp-mini img');
    elNome = toast.querySelector('.sp-name');
    elProd = toast.querySelector('.sp-prod');
    elMeta = toast.querySelector('.sp-metatxt');

    toast.querySelector('.sp-close').addEventListener('click', function (e) {
      e.preventDefault();
      e.stopPropagation();
      stop();
      try { sessionStorage.setItem('sf_avvisi_off', '1'); } catch (err) {}
    });

    toast.addEventListener('click', function () {
      window.dataLayer = window.dataLayer || [];
      window.dataLayer.push({
        event: 'select_promotion',
        promotion_name: 'avviso_' + elNome.textContent.slice(0, 40)
      });
    });
  }

  function mostra() {
    if (volte >= MAX_VOLTE) return;
    var a = AVVISI[i % AVVISI.length];
    i++; volte++;
    elImg.src = a.img;
    elNome.textContent = a.nome;
    elProd.textContent = a.prod;
    elMeta.textContent = a.meta;
    toast.href = a.link;
    toast.classList.add('show');
    tHide = setTimeout(nascondi, DURATA);
  }

  function nascondi() {
    toast.classList.remove('show');
    if (volte < MAX_VOLTE) tShow = setTimeout(mostra, PAUSA);
  }

  function stop() {
    clearTimeout(tShow);
    clearTimeout(tHide);
    volte = MAX_VOLTE;
    if (toast) toast.classList.remove('show');
  }

  // la barra promo e' sticky in cima: il cartellino si mette sotto
  function posiziona() {
    var promo = document.querySelector('.promo');
    var h = promo ? Math.round(promo.getBoundingClientRect().height) : 0;
    toast.style.top = (h + 12) + 'px';
  }

  function init() {
    build();
    posiziona();
    window.addEventListener('resize', posiziona);
    tShow = setTimeout(mostra, PRIMO_RITARDO);
    // se apri l'anteprima, il cartellino si toglie di mezzo
    document.addEventListener('click', function (e) {
      if (e.target.closest('[data-galleria]')) {
        clearTimeout(tHide);
        toast.classList.remove('show');
        if (volte < MAX_VOLTE) tShow = setTimeout(mostra, PAUSA);
      }
    });
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();

  window.Avvisi = { stop: stop, dati: AVVISI };
})();
