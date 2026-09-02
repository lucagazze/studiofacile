/* =========================================================
   Galleria anteprime — Studio Facile
   Un solo visore condiviso da index, biblioteca e prontuari.
   Uso:  <button class="btn-galleria" data-galleria="emergenza">…</button>
   ========================================================= */
(function () {
  'use strict';

  var BASE = '/anteprime/';

  var LIBRI = {
    emergenza: {
      titolo: 'Farmaci in Emergenza',
      pagine: [
        ['emergenza_01', 'I sette scenari dell’urgenza'],
        ['emergenza_02', 'Le vie: EV, IO, IM, endotracheale'],
        ['emergenza_03', 'Il carrello, cassetto per cassetto'],
        ['emergenza_04', 'Le diluizioni che uccidono'],
        ['emergenza_05', 'Scheda farmaco: Amiodarone'],
        ['emergenza_06', 'Scheda farmaco: Adrenalina'],
        ['emergenza_07', 'I venti numeri da sapere a memoria']
      ]
    },
    antibiotici: {
      titolo: 'Prontuario Illustrato — Antibiotici',
      pagine: [
        ['antibiotici_01', 'Quale antibiotico, quale infezione'],
        ['antibiotici_02', 'Gram positivi e Gram negativi'],
        ['antibiotici_03', 'Spettro stretto e spettro largo'],
        ['antibiotici_04', 'Leggere un antibiogramma'],
        ['antibiotici_05', 'Scheda farmaco: Amoxicillina'],
        ['antibiotici_06', 'I macrolidi'],
        ['antibiotici_07', 'Che cos’è la resistenza']
      ]
    },
    psicofarmaci: {
      titolo: 'Prontuario Illustrato — Psicofarmaci',
      pagine: [
        ['psicofarmaci_01', 'I neurotrasmettitori che contano'],
        ['psicofarmaci_02', 'Tolleranza e dipendenza'],
        ['psicofarmaci_03', 'Il recettore GABA-A'],
        ['psicofarmaci_04', 'La sospensione graduale'],
        ['psicofarmaci_05', 'Gli SSRI'],
        ['psicofarmaci_06', 'Le quattro vie dopaminergiche'],
        ['psicofarmaci_07', 'Le classi a confronto']
      ]
    },
    antinfiammatori: {
      titolo: 'Prontuario Illustrato — Antinfiammatori',
      pagine: [
        ['antinfiammatori_01', 'Che cos’è l’infiammazione'],
        ['antinfiammatori_02', 'La cascata dell’acido arachidonico'],
        ['antinfiammatori_03', 'COX-1 e COX-2'],
        ['antinfiammatori_04', 'Come nasce il dolore'],
        ['antinfiammatori_05', 'Come si classificano'],
        ['antinfiammatori_06', 'Scheda farmaco: Ibuprofene'],
        ['antinfiammatori_07', 'La sospensione graduale del cortisone']
      ]
    },
    laboratorio: {
      titolo: 'Leggere gli Esami di Laboratorio',
      pagine: [
        ['laboratorio_01', 'Come si legge un referto'],
        ['laboratorio_02', 'Il valore di riferimento non è un confine'],
        ['laboratorio_03', 'La variabilità preanalitica'],
        ['laboratorio_04', 'I valori critici'],
        ['laboratorio_05', 'Che cos’è l’emocromo'],
        ['laboratorio_06', 'Il rene in quattro numeri'],
        ['laboratorio_07', 'L’emostasi in una pagina']
      ]
    },
    farmacologia: {
      titolo: 'Farmacologia Illustrata',
      pagine: [
        ['farmacologia_01', 'Potenza non è efficacia'],
        ['farmacologia_02', 'Tutte le vie in una pagina'],
        ['farmacologia_03', 'ADME: il viaggio in quattro tappe'],
        ['farmacologia_04', 'Il percorso nel nefrone'],
        ['farmacologia_05', 'Recettori: chiave e serratura'],
        ['farmacologia_06', 'La curva dose-risposta'],
        ['farmacologia_07', 'Le interazioni in sei regole']
      ]
    },
    bonus1: {
      titolo: 'Bonus 1 — Termini Chiave di Farmacia Clinica',
      pagine: [
        ['bonus1_01', 'Come si legge una voce'],
        ['bonus1_02', 'Le voci della lettera A'],
        ['bonus1_03', 'Le voci della lettera C'],
        ['bonus1_04', 'Le coppie che si confondono'],
        ['bonus1_05', 'Abbreviazioni della prescrizione'],
        ['bonus1_06', 'Sigle e valori di laboratorio']
      ]
    },
    bonus2: {
      titolo: 'Bonus 2 — Schede di Ripasso Rapido',
      pagine: [
        ['bonus2_01', 'Come si studia una classe'],
        ['bonus2_02', 'La classe in una pagina: antipertensivi'],
        ['bonus2_03', 'Antipertensivi: ripasso lampo'],
        ['bonus2_04', 'La classe in una pagina: antibiotici'],
        ['bonus2_05', 'Le cinque classi a confronto'],
        ['bonus2_06', 'Le venti domande che tornano sempre']
      ]
    }
  };

  /* ---------- CSS ---------- */
  var CSS = [
    '.gal-ov{position:fixed;inset:0;background:rgba(16,24,40,.78);z-index:9999;display:none;',
      'align-items:center;justify-content:center;padding:16px}',
    '.gal-ov.on{display:flex}',
    '.gal-box{background:#fff;border-radius:16px;width:100%;max-width:640px;max-height:90vh;',
      'display:flex;flex-direction:column;overflow:hidden;box-shadow:0 24px 70px rgba(0,0,0,.35)}',
    '.gal-head{padding:16px 52px 16px 18px;border-bottom:1px solid #e1e8f4;position:relative;flex-shrink:0}',
    '.gal-tit{font-size:16px;font-weight:800;color:#1c3479;line-height:1.3}',
    '.gal-sub{display:block;font-size:13px;font-weight:500;color:#667085;margin-top:3px}',
    '.gal-x{position:absolute;right:12px;top:50%;transform:translateY(-50%);background:#f4f7fd;',
      'border:none;width:32px;height:32px;border-radius:50%;font-size:20px;line-height:1;',
      'cursor:pointer;color:#667085;font-family:inherit}',
    '.gal-x:hover{background:#e1e8f4}',
    '.gal-body{overflow-y:auto;padding:16px;background:#f4f7fd;-webkit-overflow-scrolling:touch}',
    '.gal-fig{margin:0 0 16px}',
    '.gal-fig:last-child{margin-bottom:0}',
    '.gal-fig img{width:100%;border-radius:8px;display:block;background:#fff;',
      'box-shadow:0 4px 20px rgba(16,24,40,.10)}',
    '.gal-cap{font-size:13px;font-weight:700;color:#1c3479;margin-top:8px;text-align:center}',
    '.gal-cap span{display:inline-block;background:#eff4fd;border-radius:999px;padding:4px 12px}',
    '.gal-foot{padding:14px 16px;border-top:1px solid #e1e8f4;flex-shrink:0}',
    '.gal-foot a{display:block;background:#f97216;color:#fff;font-size:15px;font-weight:800;',
      'text-align:center;padding:14px;border-radius:11px;box-shadow:0 6px 22px rgba(249,114,22,.42)}',
    '.gal-foot a:hover{background:#dd5f0a}'
  ].join('');

  /* ---------- markup ---------- */
  var ov, elTit, elBody, elFoot;
  var libro = null, lastFocus = null;

  function build() {
    var st = document.createElement('style');
    st.textContent = CSS;
    document.head.appendChild(st);

    ov = document.createElement('div');
    ov.className = 'gal-ov';
    ov.setAttribute('role', 'dialog');
    ov.setAttribute('aria-modal', 'true');
    ov.innerHTML =
      '<div class="gal-box">' +
        '<div class="gal-head">' +
          '<div class="gal-tit" id="galTit"></div>' +
          '<button class="gal-x" type="button" aria-label="Chiudi">&times;</button>' +
        '</div>' +
        '<div class="gal-body" id="galBody"></div>' +
        '<div class="gal-foot" id="galFoot"></div>' +
      '</div>';
    document.body.appendChild(ov);

    elTit = ov.querySelector('#galTit');
    elBody = ov.querySelector('#galBody');
    elFoot = ov.querySelector('#galFoot');

    ov.querySelector('.gal-x').addEventListener('click', close);
    ov.addEventListener('click', function (e) { if (e.target === ov) close(); });
  }

  /* CTA in fondo al modale, secondo la pagina in cui si trova */
  function ctaHtml(slug) {
    var kit = ['farmacologia', 'bonus1', 'bonus2'];
    if (kit.indexOf(slug) !== -1) {
      return '<a href="/" data-product="Kit Farmacologia Illustrata" data-price="15" data-goto-page="1">' +
             'SCOPRI IL KIT COMPLETO &middot; 15&euro;</a>';
    }
    var trio = ['emergenza', 'antibiotici', 'psicofarmaci'];
    var dove = trio.indexOf(slug) !== -1 ? '/trio-clinico' : '/collezione';
    var testo = trio.indexOf(slug) !== -1
      ? 'VEDI IL TRIO CLINICO &middot; 19,90&euro;'
      : 'VEDI LA COLLEZIONE &middot; 32,90&euro;';
    return '<a href="' + dove + '" data-goto-page="1">' + testo + '</a>';
  }

  function open(slug) {
    libro = LIBRI[slug];
    if (!libro) return;
    lastFocus = document.activeElement;

    elTit.innerHTML = '';
    elTit.appendChild(document.createTextNode('Anteprima: ' + libro.titolo));
    var sub = document.createElement('span');
    sub.className = 'gal-sub';
    sub.textContent = libro.pagine.length + ' pagine reali del volume';
    elTit.appendChild(sub);

    elBody.innerHTML = '';
    libro.pagine.forEach(function (pg, i) {
      var fig = document.createElement('figure');
      fig.className = 'gal-fig';
      var im = document.createElement('img');
      im.src = BASE + pg[0] + '.webp';
      im.alt = libro.titolo + ' \u2014 ' + pg[1];
      im.loading = i < 2 ? 'eager' : 'lazy';
      im.decoding = 'async';
      fig.appendChild(im);
      var cap = document.createElement('figcaption');
      cap.className = 'gal-cap';
      var sp = document.createElement('span');
      sp.textContent = (i + 1) + ' / ' + libro.pagine.length + ' \u00b7 ' + pg[1];
      cap.appendChild(sp);
      fig.appendChild(cap);
      elBody.appendChild(fig);
    });
    elBody.scrollTop = 0;

    elFoot.innerHTML = ctaHtml(slug);

    ov.classList.add('on');
    document.body.style.overflow = 'hidden';
    ov.querySelector('.gal-x').focus();

    if (typeof fbq === 'function') {
      fbq('track', 'ViewContent', {
        content_name: libro.titolo,
        content_category: 'Anteprima pagine',
        currency: 'EUR'
      });
    }
    window.dataLayer = window.dataLayer || [];
    window.dataLayer.push({ event: 'view_anteprima', item_name: libro.titolo });
  }

  function close() {
    ov.classList.remove('on');
    document.body.style.overflow = '';
    elBody.innerHTML = '';
    if (lastFocus && lastFocus.focus) lastFocus.focus();
  }

  document.addEventListener('keydown', function (e) {
    if (ov && ov.classList.contains('on') && e.key === 'Escape') close();
  });

  function init() {
    build();
    document.addEventListener('click', function (e) {
      var b = e.target.closest('[data-galleria]');
      if (!b) return;
      e.preventDefault();
      open(b.getAttribute('data-galleria'));
    });
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();

  window.Galleria = { apri: open, chiudi: close, libri: LIBRI };
})();
