# Farmacología Ilustrada — Estudia Sencillo

Landing page del Kit de Farmacología Ilustrada (8 módulos + 2 bonus, USD 13, checkout Hotmart).

## Estructura
- `index.html` — la landing completa (CSS y JS inline, sin build)
- `mockups/`, `amostras/`, `depoimentos/`, `personagens/` — imágenes WebP
- `original.html` — versión previa en morado (ignorada por git, solo referencia local)

## Paleta
| Uso | Color |
|---|---|
| Azul primario / hero | `#2645a0` |
| Azul oscuro | `#1c3479` / `#1b3277` |
| Amarillo de acento | `#f7cf49` |
| Naranja de botones | `#f97216` |
| Fondo | `#FFFFFF` |

## Medición
GTM (server-side vía Stape) + Microsoft Clarity ya instalados en el `<head>`.
La página empuja al `dataLayer`:
- `view_item` al cargar
- `begin_checkout` en cada clic al checkout, con `cta_id` para saber cuál de los 5 CTAs cierra

## Notas
- Todos los CTAs abren el checkout en la misma pestaña (mejor en mobile).
- La barra de compra sticky aparece al pasar el CTA del hero y se oculta cuando otro CTA está a la vista.
