# ADR 0005 — Dos oros: --color-gold para el filete, --color-gold-ink para el texto

Fecha: 2026-07-31
Estado: Aceptado
Depende de: ADR 0004 (regla de contraste del Sistema 2)

## Contexto

El ADR 0004 dejó la regla —cualquier texto que el espectador tenga que leer va a
4,5:1 o mejor sobre su fondo real— y dos defectos anotados sin corregir. Los dos
eran el mismo choque de especificidad: un párrafo con clase suelta al que
`.stMarkdown p` le roba color, tamaño y familia.

**`mono_caption()`** salía en Inter 15px #141A24. Debería ser JetBrains Mono 13px
`--color-ink-muted`. No era monoespaciada, ni pequeña, ni apagada: no hacía nada de
lo que existe para hacer. Aquí no hay decisión que tomar, solo el arreglo: el
contraste ya pasaba (5,51:1).

**`highlight_block()`** es el caso interesante. Su eyebrow salía en Inter 15px
#141A24, o sea que **el bloque dorado no tenía oro en el texto**: lo único dorado
que se veía era el filete izquierdo de 3px. Y arreglar la especificidad sin más
habría publicado un texto a 2,54:1, peor que el `--color-ink-soft` que el ADR 0004
acababa de retirar precisamente por ilegible.

Medidas sobre los dos fondos del Sistema 2:

| Color | Sobre #F6F2EA (página) | Sobre #FBF8F2 (panel) |
|---|---|---|
| `--color-gold` #B89968 | 2,41:1 | 2,54:1 |
| `--chart-cat-2` #AF843A | 3,04:1 | 3,20:1 |
| **`--color-gold-ink` #816A46** | **4,61:1** | **4,85:1** |

Antes de inventar un token se comprobó si servía `--chart-cat-2` (#AF843A), el oro
ya validado para gráficos en la S28: reutilizar habría sido mejor que crear. Se
queda en 3,20:1 y no llega.

## Decisión

### 1. El oro se parte en dos tokens

Se añade `--color-gold-ink: #816A46` a la paleta. El reparto es estricto:

- **`--color-gold` #B89968** → filetes, bordes, rellenos. **Nunca texto.**
- **`--color-gold-ink` #816A46** → cualquier texto en oro.

`.yidoca-highlight-eyebrow` pasa a `p.yidoca-highlight-eyebrow` y a
`var(--color-gold-ink)`. El filete izquierdo del bloque se queda en `--color-gold`:
es borde, no texto, y ahí el oro de marca luce y no tiene que leerse.

`.yidoca-mono` pasa a `p.yidoca-mono`, sin tocar el color.

### 2. La regla general: cuándo se retira un color del texto y cuándo se le hace variante

Los ADR 0004 y 0005 resuelven el mismo problema —un color que no llega a 4,5:1— de
dos maneras opuestas. La distinción va a volver a hacer falta, así que conviene
dejarla escrita:

**`--color-ink-soft` se retiró del texto. No llevaba significado.** Era gris claro
para etiquetas, y al quitarlo no se perdió nada, porque la jerarquía de un eyebrow
ya la llevaban el tamaño, el peso, las versalitas y el `letter-spacing`. El color
solo estaba repitiendo, más flojo, algo que ya decían otras cuatro señales.

**El oro se corrige, no se retira. Sí lleva significado, y no lo lleva nada más.**
Marca el momento de decisión: en la Demo G es el único sitio de toda la pantalla
donde aparece, y el momento 1 renuncia a él entero para que el momento 3 lo tenga
(ADR 0004 de `yidoca-demo-cabina`). Si el oro sobreviviera solo como un filete de
3px, proyectado a tres metros ese filete no existe y el bloque dorado deja de ser
dorado. Se perdería la señal, no un adorno.

> **Un color decorativo que no pasa contraste se retira del texto. Un color con
> carga semántica se corrige con una variante del mismo tono.**

El coste de la variante es real y hay que asumirlo: dos tokens del mismo color son
dos oportunidades de usar el que no toca. Por eso el reparto está en el comentario
del token, en la tabla de este ADR y en el README, y por eso la variante es del
mismo tono y no un oro distinto: puestos uno al lado del otro —filete #B89968,
texto #816A46— se leen como el mismo color a dos profundidades, no como dos
colores.

## Alternativas consideradas

- **Dejar el eyebrow del highlight en `--color-ink-muted` y que el oro viva solo en
  el filete.** Rechazada por lo del punto 2: es coherente con lo que se hizo con
  ink-soft, pero ink-soft no significaba nada y el oro sí. Habría dejado el bloque
  de decisión sin la marca que lo hace bloque de decisión.
- **Reutilizar `--chart-cat-2` #AF843A.** Rechazada por medida: 3,20:1 sobre panel.
  Era la opción preferible —un token menos— y no da.
- **Subir el peso o el tamaño del eyebrow para acogerse al 3:1 de texto grande.**
  Rechazada. El umbral de texto grande empieza en 18,66px con peso 700, y un
  eyebrow de 11px en versalitas no es texto grande ni por asomo. Además el ADR 0004
  fijó 4,5:1 sin excepción por tamaño, precisamente para no tener esta conversación
  en cada componente.
- **Oscurecer `--color-gold` a #816A46 para todos los usos.** Rechazada: el filete
  y los rellenos perderían el brillo que hace reconocible el oro de marca, y ahí no
  hay problema de legibilidad que resolver.

## Consecuencias

- El bloque dorado vuelve a tener oro en el texto, por primera vez desde que existe
  el componente. Es un cambio visible en las demos publicadas, y es el aspecto
  correcto: el anterior era el bug.
- Los captions monoespaciados de las demos cambian de aspecto: pasan de cuerpo de
  texto normal a JetBrains Mono 13px apagada. Es para lo que existen.
- La paleta tiene ahora doce tokens de color y dos de ellos son oro. Quien añada un
  componente con texto en oro tiene que elegir bien; el comentario del token lo
  dice en una línea.
- La guía de UI (`6. GUIA_UI_YIDOCA.md`) suma a lo ya desactualizado por el ADR
  0004 la sección 4.1 (falta el token) y 4.2 (la fila de `--color-gold` dice
  "highlights estratégicos, recomendaciones, decisiones" sin distinguir texto de
  filete).

## Notas

Medido con Playwright sobre la página en marcha, resolviendo el fondo real subiendo
por el DOM hasta el primer antecesor opaco:

| Componente | Familia | Tamaño | Color | Fondo | Ratio |
|---|---|---|---|---|---|
| `mono_caption()` | JetBrains Mono | 13px | #5A6270 | #F6F2EA | 5,51 |
| `highlight_block()` · eyebrow | Inter | 11px | #816A46 | #FBF8F2 | 4,85 |
| `highlight_block()` · cuerpo | Inter | 15px | #141A24 | #FBF8F2 | 16,47 |

Barrido completo de clases servidas sobre un `<p>` de markdown, que son las únicas
que `.stMarkdown p` alcanza: `yidoca-eyebrow`, `yidoca-section-kicker`,
`yidoca-parrafo`, `yidoca-mono`, `yidoca-highlight-eyebrow` y
`yidoca-highlight-text`. Las cinco primeras llevan ya el tipo delante.

**Queda una, y se deja a propósito.** `.yidoca-highlight-text` es un `<p>` con clase
suelta, así que también la pisa `.stMarkdown p` — pero declara exactamente los
mismos valores que la regla que la pisa (0.9375rem, `--color-ink`, `line-height`
1.6), así que hoy no se nota. Es una trampa latente: el día que alguien cambie el
color o el tamaño de esa clase, el cambio no tendrá efecto y no habrá pista de por
qué. Se toca cuando haya motivo para tocarla, no antes.

`.yidoca-score-number`, `.yidoca-score-denom` y `.yidoca-score-label` son `<span>`,
`<span>` y `<div>`; `.yidoca-table` y sus celdas son tabla. Ninguna la alcanza
`.stMarkdown p`. `.yidoca-panel` y `.yidoca-wordmark` no las emite ninguna función:
son CSS disponible para quien lo quiera usar a mano, y si alguien las pone sobre un
`<p>` se encontrará con lo mismo.

Versiones sobre las que se validó: Streamlit 1.58.0.
