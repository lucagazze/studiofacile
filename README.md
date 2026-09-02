# Farmacologia Illustrata — Studio Facile

Landing page del Kit di Farmacologia Illustrata (8 moduli + 2 bonus, 15€ / EUR, checkout Hotmart).
Todos los textos en italiano.

## Estructura
- `index.html` — la landing completa (CSS y JS inline, sin build)
- `mockups/`, `amostras/`, `depoimentos/`, `personagens/` — imágenes WebP
- `original.html` — versión previa en español y morado (ignorada por git, solo referencia local)

## Paleta
| Uso | Color |
|---|---|
| Azul primario / hero | `#2645a0` |
| Azul oscuro | `#1c3479` / `#1b3277` |
| Amarillo de acento | `#f7cf49` |
| Naranja de botones | `#f97216` |
| Fondo | `#FFFFFF` |

## Medición
GTM (server-side vía Stape) + Microsoft Clarity en el `<head>`.
La página empuja al `dataLayer`:
- `view_item` al cargar
- `begin_checkout` en cada clic al checkout, con `cta_id` para saber cuál de los 5 CTAs cierra

## PENDIENTE antes de publicar
Estos datos siguen apuntando al proyecto en español y hay que reemplazarlos:

- **Imágenes**: todos los mockups, páginas de muestra y testimonios están en español.
  El texto dice "100% in italiano" pero las imágenes lo desmienten.
- **Checkout**: `pay.hotmart.com/S95440624D` es el producto en español.
- **GTM**: contenedor de `api.farmaciamapeada.com.br` (proyecto ES).
- **Clarity**: project id `wcui1pae9q` (proyecto ES).
- **canonical / og:url**: apuntan a `es.farmaciamapeada.com.br/farmacologia/`.
- **Favicon**: `estudiasencillo.com.mx`.
- **Claim "96,3%"**: sin fuente citada. Riesgo de rechazo en Meta.
