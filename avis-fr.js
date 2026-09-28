/* =========================================================
   Avis social proof — Studio Facile, landings FRANÇAISES
   Même cartouche que la version italienne (avvisi.js), en
   haut à gauche, avec le rythme discret d'origine.

   CE NE SONT PAS DE FAUSSES NOTIFICATIONS D'ACHAT.
   La version italienne le dit dès sa première ligne : tous
   les messages sont vérifiables. Ce sont des faits du
   catalogue — ce que contient une offre, son prix, le
   nombre d'étudiants déjà annoncé sur la page — et pas
   «X vient d'acheter» avec un prénom et une ville tirés
   d'une liste. Un compteur de ventes inventé sur un produit
   qui n'a pas encore été vendu se voit, et il coûte la
   confiance au moment exact où le visiteur décide.

   POUR METTRE À JOUR : changer AVIS. Le jour où le checkout
   expose les ventes réelles, remplacer le tableau par les
   données de l'API : la structure est
   { img, nom, prod, meta, lien }.
   ========================================================= */
(function () {
  'use strict';

  var AVIS = [
    {
      img: '/mockups/fr-chimie/hero.webp',
      nom: 'Kit Chimie Illustrée',
      prod: '80 pages illustrées + 2 bonus',
      meta: '19,90 € · paiement unique',
      lien: '/fr/chimie'
    },
    {
      img: '/mockups/fr/combo-pharmacologie.webp',
      nom: 'Kit Pharmacologie Illustrée',
      prod: 'La pharmacologie expliquée en dessins',
      meta: 'Avec deux prontuaires en bonus',
      lien: '/fr/pharmacologie'
    },
    {
      img: '/mockups/ecg-fr/hero.webp',
      nom: 'Lire l’ECG',
      prod: 'La méthode en huit étapes',
      meta: 'Accès à vie, sans abonnement',
      lien: '/fr/ecg'
    },
    {
      img: '/mockups/fr-chimie/hero.webp',
      nom: '+11 978 étudiants et professionnels',
      prod: 'Utilisent les supports Studio Facile',
      meta: 'Garantie 30 jours',
      lien: '/fr/chimie'
    }
  ];

  // Rythme discret : arrive tard, reste peu, revient rarement puis s'arrête.
  var PREMIER_DELAI = 14000;
  var DUREE         = 6000;
  var PAUSE         = 30000;
  var MAX_FOIS      = 4;

  if (!AVIS.length) return;
  try { if (sessionStorage.getItem('sf_avis_off') === '1') return; } catch (e) {}
  if (window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;

  // La feuille de style des landings définit déjà .sp-toast : on ne la
  // réécrit pas, on s'y branche. Si un jour une page n'a pas ce CSS, le
  // cartouche reste invisible plutôt que de s'afficher de travers.
  var toast, elImg, elNom, elProd, elMeta, i = 0, fois = 0, tShow, tHide;

  function build() {
    toast = document.createElement('a');
    toast.className = 'sp-toast';
    toast.setAttribute('role', 'status');
    toast.setAttribute('aria-live', 'polite');
    toast.innerHTML =
      '<button class="sp-close" type="button" aria-label="Fermer">&times;</button>' +
      '<span class="sp-mini"><img alt="" width="66" height="42"></span>' +
      '<span class="sp-txt">' +
        '<span class="sp-name"></span>' +
        '<span class="sp-prod"></span>' +
        '<span class="sp-meta"><span class="ok">&#10003;</span><span class="sp-metatxt"></span></span>' +
      '</span>';
    document.body.appendChild(toast);

    elImg = toast.querySelector('.sp-mini img');
    elNom = toast.querySelector('.sp-name');
    elProd = toast.querySelector('.sp-prod');
    elMeta = toast.querySelector('.sp-metatxt');

    toast.querySelector('.sp-close').addEventListener('click', function (e) {
      e.preventDefault();
      e.stopPropagation();
      stop();
      try { sessionStorage.setItem('sf_avis_off', '1'); } catch (err) {}
    });

    toast.addEventListener('click', function () {
      window.dataLayer = window.dataLayer || [];
      window.dataLayer.push({
        event: 'select_promotion',
        promotion_name: 'avis_' + elNom.textContent.slice(0, 40)
      });
    });
  }

  function montre() {
    if (fois >= MAX_FOIS) return;
    var a = AVIS[i % AVIS.length];
    i++; fois++;
    elImg.src = a.img;
    elNom.textContent = a.nom;
    elProd.textContent = a.prod;
    elMeta.textContent = a.meta;
    toast.href = a.lien;
    toast.classList.add('show');
    tHide = setTimeout(cache, DUREE);
  }

  function cache() {
    toast.classList.remove('show');
    if (fois < MAX_FOIS) tShow = setTimeout(montre, PAUSE);
  }

  function stop() {
    clearTimeout(tShow);
    clearTimeout(tHide);
    if (toast) toast.classList.remove('show');
    fois = MAX_FOIS;
  }

  function demarre() {
    build();
    tShow = setTimeout(montre, PREMIER_DELAI);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', demarre);
  } else {
    demarre();
  }
})();
