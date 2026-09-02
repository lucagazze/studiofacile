/* =========================================================
   Scelta del combo — Studio Facile
   Un volume che sta nel Trio e nella Collezione fa scegliere;
   uno che sta solo nella Collezione ci va dritto.

   Uso:  <button data-combo="emergenza">VEDI I COMBO</button>
   ========================================================= */
(function () {
  'use strict';

  var COMBO = {
    trio: {
      nome: 'Trio Clinico',
      sotto: '3 prontuari · 250 pagine illustrate',
      dettaglio: 'Emergenza, Antibiotici e Psicofarmaci',
      prezzo: '20,70€',
      avolume: '6,90€ a volume',
      img: '/mockups/books/mockup-trio-tablets.webp',
      link: '/trio-clinico'
    },
    collezione: {
      nome: 'Collezione Completa',
      sotto: '5 prontuari · 386 pagine illustrate',
      dettaglio: 'Tutti e cinque i prontuari clinici',
      prezzo: '32,50€',
      avolume: '6,50€ a volume',
      img: '/mockups/books/mockup-bundle-tablets.webp',
      link: '/collezione'
    }
  };

  // in quali combo si trova ogni volume
  var DOVE = {
    emergenza:       { titolo: 'Farmaci in Emergenza',                  combo: ['trio', 'collezione'] },
    antibiotici:     { titolo: 'Prontuario Illustrato — Antibiotici',   combo: ['trio', 'collezione'] },
    psicofarmaci:    { titolo: 'Prontuario Illustrato — Psicofarmaci',  combo: ['trio', 'collezione'] },
    antinfiammatori: { titolo: 'Prontuario Illustrato — Antinfiammatori', combo: ['collezione'] },
    laboratorio:     { titolo: 'Leggere gli Esami di Laboratorio',      combo: ['collezione'] }
  };

  var CSS = [
    '.cb-ov{position:fixed;inset:0;background:rgba(16,24,40,.78);z-index:9998;display:none;',
      'align-items:center;justify-content:center;padding:16px}',
    '.cb-ov.on{display:flex}',
    '.cb-box{background:#fff;border-radius:16px;width:100%;max-width:560px;max-height:90vh;',
      'display:flex;flex-direction:column;overflow:hidden;box-shadow:0 24px 70px rgba(0,0,0,.35)}',
    '.cb-head{padding:16px 52px 16px 18px;border-bottom:1px solid #e1e8f4;position:relative;flex-shrink:0}',
    '.cb-tit{font-size:16px;font-weight:800;color:#1c3479;line-height:1.3}',
    '.cb-sub{display:block;font-size:13px;font-weight:500;color:#667085;margin-top:3px}',
    '.cb-x{position:absolute;right:12px;top:50%;transform:translateY(-50%);background:#f4f7fd;',
      'border:none;width:32px;height:32px;border-radius:50%;font-size:20px;line-height:1;',
      'cursor:pointer;color:#667085;font-family:inherit}',
    '.cb-x:hover{background:#e1e8f4}',
    '.cb-body{overflow-y:auto;padding:16px;background:#f4f7fd;display:grid;gap:14px}',
    '.cb-card{display:block;background:#fff;border:2px solid #e1e8f4;border-radius:14px;',
      'padding:14px;color:#101828;transition:border-color .18s,transform .15s,box-shadow .18s}',
    '.cb-card:hover{border-color:#2645a0;transform:translateY(-2px);box-shadow:0 10px 26px rgba(16,24,40,.12)}',
    '.cb-card.best{border-color:#f97216}',
    '.cb-top{display:flex;gap:12px;align-items:center}',
    '.cb-shot{flex:0 0 auto;width:96px;height:60px;border-radius:8px;overflow:hidden;',
      'background:linear-gradient(160deg,#eff4fd,#dfe8fa);display:flex;align-items:center;justify-content:center}',
    '.cb-shot img{max-width:100%;max-height:100%;width:auto;height:auto;object-fit:contain;display:block}',
    '.cb-info{min-width:0;flex:1;display:block}',
    '.cb-nome{display:block;font-size:16px;font-weight:800;color:#1c3479;line-height:1.25}',
    '.cb-sotto{display:block;font-size:12.5px;color:#667085;margin-top:3px;line-height:1.35}',
    '.cb-det{display:block;font-size:12.5px;color:#667085;margin-top:1px;line-height:1.35}',
    '.cb-prezzo{text-align:right;flex:0 0 auto;display:block}',
    '.cb-p{display:block;font-size:22px;font-weight:900;color:#1c3479;line-height:1.1}',
    '.cb-av{display:block;font-size:11px;color:#98a3ad;white-space:nowrap;margin-top:2px}',
    '.cb-go{display:block;margin-top:12px;background:#f97216;color:#fff;font-size:14.5px;',
      'font-weight:800;text-align:center;padding:12px;border-radius:10px}',
    '.cb-card:not(.best) .cb-go{background:#2645a0}',
    '.cb-nota{font-size:12.5px;color:#667085;text-align:center;padding:0 16px 14px;margin:0;background:#f4f7fd}',
    '@media(max-width:480px){',
      '.cb-top{flex-wrap:wrap}.cb-prezzo{text-align:left;width:100%;margin-top:4px}',
      '.cb-av{display:inline;margin-left:8px}}'
  ].join('');

  var ov, elTit, elBody, lastFocus = null;

  function build() {
    var st = document.createElement('style');
    st.textContent = CSS;
    document.head.appendChild(st);

    ov = document.createElement('div');
    ov.className = 'cb-ov';
    ov.setAttribute('role', 'dialog');
    ov.setAttribute('aria-modal', 'true');
    ov.innerHTML =
      '<div class="cb-box">' +
        '<div class="cb-head">' +
          '<div class="cb-tit" id="cbTit"></div>' +
          '<button class="cb-x" type="button" aria-label="Chiudi">&times;</button>' +
        '</div>' +
        '<div class="cb-body" id="cbBody"></div>' +
        '<p class="cb-nota">Questo volume fa parte dei combo qui sopra.</p>' +
      '</div>';
    document.body.appendChild(ov);

    elTit = ov.querySelector('#cbTit');
    elBody = ov.querySelector('#cbBody');
    ov.querySelector('.cb-x').addEventListener('click', close);
    ov.addEventListener('click', function (e) { if (e.target === ov) close(); });
  }

  function card(key, best) {
    var c = COMBO[key];
    var a = document.createElement('a');
    a.className = 'cb-card' + (best ? ' best' : '');
    a.href = c.link;
    a.setAttribute('data-product', c.nome);
    a.innerHTML =
      '<span class="cb-top">' +
        '<span class="cb-shot"><img src="' + c.img + '" alt="" loading="lazy"></span>' +
        '<span class="cb-info">' +
          '<span class="cb-nome">' + c.nome + '</span>' +
          '<span class="cb-sotto">' + c.sotto + '</span>' +
          '<span class="cb-det">' + c.dettaglio + '</span>' +
        '</span>' +
        '<span class="cb-prezzo"><span class="cb-p">' + c.prezzo + '</span>' +
        '<span class="cb-av">' + c.avolume + '</span></span>' +
      '</span>' +
      '<span class="cb-go">VEDI ' + c.nome.toUpperCase() + '</span>';
    a.addEventListener('click', function () {
      window.dataLayer = window.dataLayer || [];
      window.dataLayer.push({ event: 'select_item', item_name: c.nome, value: parseFloat(c.prezzo), currency: 'EUR' });
    });
    return a;
  }

  function open(slug) {
    var d = DOVE[slug];
    if (!d) return;

    // se sta in un solo combo, non ha senso far scegliere
    if (d.combo.length === 1) {
      window.location.href = COMBO[d.combo[0]].link;
      return;
    }

    lastFocus = document.activeElement;
    elTit.innerHTML = '';
    elTit.appendChild(document.createTextNode('Dove trovi ' + d.titolo));
    var sub = document.createElement('span');
    sub.className = 'cb-sub';
    sub.textContent = 'Questo volume è incluso in ' + d.combo.length + ' combo. Scegli quello che ti serve.';
    elTit.appendChild(sub);

    elBody.innerHTML = '';
    d.combo.forEach(function (k) {
      elBody.appendChild(card(k, k === 'collezione'));
    });

    ov.classList.add('on');
    document.body.style.overflow = 'hidden';
    ov.querySelector('.cb-x').focus();

    window.dataLayer = window.dataLayer || [];
    window.dataLayer.push({ event: 'view_combo_scelta', item_name: d.titolo });
  }

  function close() {
    ov.classList.remove('on');
    document.body.style.overflow = '';
    if (lastFocus && lastFocus.focus) lastFocus.focus();
  }

  document.addEventListener('keydown', function (e) {
    if (ov && ov.classList.contains('on') && e.key === 'Escape') close();
  });

  function init() {
    build();
    document.addEventListener('click', function (e) {
      var b = e.target.closest('[data-combo]');
      if (!b) return;
      e.preventDefault();
      open(b.getAttribute('data-combo'));
    });
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();

  window.ComboScelta = { apri: open, chiudi: close };
})();
