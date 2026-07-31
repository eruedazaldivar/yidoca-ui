# ADR 0004 — Contraste mínimo del Sistema 2 y nuevo papel de --color-ink-soft

Fecha: 2026-07-31
Estado: Aceptado
Depende de: ADR 0001 (tokens aislados), ADR 0003 (tabla)

## Contexto

Midiendo los componentes del ADR 0003 sobre el DOM real aparecieron dos defectos
encadenados, y el primero estaba tapando al segundo.

**El de especificidad.** La regla `.stMarkdown p` de `aplicar_estilo_yidoca` fija
`color`, `font-size`, `line-height` y `font-family` para todo párrafo de markdown.
Su especificidad es (0,1,1) —una clase y un tipo—; la de una clase suelta como
`.yidoca-eyebrow`, (0,1,0). Gana `.stMarkdown p`. Resultado: `eyebrow()` y
`section_kicker()` no salían en el color que declara su propia regla, sino en
`--color-ink`.

**El de contraste, que el anterior escondía.** El color declarado era
`--color-ink-soft` (#8A8F99), y sobre el fondo crema #F6F2EA da **2,91:1**. No
llega al 4,5:1 que WCAG AA pide para texto normal ni al 3:1 de texto grande. Sobre
el fondo de panel #FBF8F2 tampoco: 3,06:1.

Es decir: el bug de especificidad estaba haciendo que el eyebrow se viera *mejor*
de lo que su regla pedía. Y donde no había bug que lo tapara, el token salía tal
cual: `.yidoca-score-label` y `.yidoca-score-denom` son un `<div>` y un `<span>`,
así que `.stMarkdown p` no los alcanza, y llevaban publicándose a 2,91:1 en las
dos demos vivas. La etiqueta del score es la que dice qué significa el número
grande. Arreglar solo la especificidad habría llevado los eyebrows al mismo sitio.

## Decisión

### 1. Regla de contraste del Sistema 2

**Cualquier texto que el espectador tenga que leer va a 4,5:1 o mejor sobre su
fondo real.** Sin excepción por tamaño, por decorativo o por secundario.

Cuando un color de la guía de UI no lo cumple, **manda el contraste y se corrige la
guía**, no al revés. La guía describe la intención de diseño; el ratio es una
medida. Una intención que no se lee no es una intención, es un descuido.

El fondo que cuenta es el real, no el nominal: dentro de un `panel()` es
`--color-bg-elev` (#FBF8F2) y no el crema de la página.

### 2. --color-ink-soft deja de ser un color de texto

Se queda en la paleta y con el mismo valor, #8A8F99. Cambia su papel: **a partir de
ahora es solo para lo que no es texto** —filetes, divisorias, bordes suaves,
estados desactivados—. Está escrito en el comentario del token.

Las micro-etiquetas pasan a `--color-ink-muted` (#5A6270): 5,51:1 sobre la página,
5,80:1 sobre un panel.

**Por qué esto no pierde jerarquía.** La jerarquía de un eyebrow la llevan el
tamaño (11px contra 15px del cuerpo), el peso (600 contra 400), las versalitas y un
`letter-spacing` de 0,16em. Cuatro señales, y ninguna es el color. Bajar el
contraste por encima de eso no añade jerarquía: solo quita legibilidad. Y estas
pantallas se leen proyectadas, en una sala, a tres metros, que es el caso peor.

Cuatro clases cambian de token:

    p.yidoca-eyebrow           p.yidoca-section-kicker
    .yidoca-score-label        .yidoca-score-denom

Y una quinta por barrido, con el mismo criterio: `.yidoca-table th`, la cabecera de
la tabla del ADR 0003. Es texto que hay que leer.

### 3. Especificidad: el tipo delante solo donde hace falta

`p.yidoca-eyebrow` y `p.yidoca-section-kicker` llevan el tipo delante para empatar
con `.stMarkdown p` en (0,1,1) y ganar por orden, que es el mismo recurso que ya
usaba `p.yidoca-parrafo`.

`.yidoca-score-label`, `.yidoca-score-denom` y `.yidoca-table th` se quedan como
clase suelta: son un `<div>`, un `<span>` y un `<th>`, y `.stMarkdown p` no los
alcanza. **No se añade especificidad que no hace falta**, porque cada punto de
especificidad de más es un punto que el siguiente que quiera sobreescribir esto
tendrá que superar.

Detalle que conviene recordar al depurar: el `<style>` de `aplicar_estilo_yidoca`
se inyecta en el **body**, no en el head. Una regla de prueba metida en el head
empata en especificidad y pierde por orden, y parece que el arreglo no funciona.

### 4. El tema de gráficos, por el mismo criterio

En `graficos.py`, `tinta_suave` (#8A8F99) pintaba las etiquetas y los títulos de
eje y el título de leyenda: texto de 10-11px sobre el fondo del gráfico, a 3,06:1.
Pasan a `tinta_media` (#5A6270). La variable `tinta_suave` desaparece: lo recesivo
del andamiaje del gráfico ya lo llevan `regla` y `regla_suave`, que son bordes y
rejilla, no texto.

## Consecuencias

- Las dos demos publicadas cambian de aspecto: eyebrows y kickers pasan de navy a
  gris medio, y las etiquetas de score y las cabeceras de tabla se oscurecen. Es el
  aspecto correcto; el anterior era el bug.
- La guía de UI (`6. GUIA_UI_YIDOCA.md`) queda desactualizada en la sección 4.1
  (comentario del token), 4.2 (tabla de significado semántico, fila
  `--color-ink-soft`), 7.1, 7.5, 7.6 y 14.8. Hay que corregirla: la librería es
  ahora la referencia y la guía va detrás.
- Cualquier componente nuevo con texto se mide antes de darlo por terminado. Un
  ratio calculado a ojo no vale: los tres tokens de tinta parecen los tres
  legibles sobre crema, y uno de ellos no lo es.

## Notas

Medido con Playwright sobre la página en marcha, resolviendo el fondo real subiendo
por el DOM hasta el primer antecesor opaco —todos estos elementos son
transparentes—:

| Componente | Color | Fondo | Tamaño | Ratio |
|---|---|---|---|---|
| `eyebrow()` | #5A6270 | #F6F2EA | 11px | 5,51 |
| `section_kicker()` | #5A6270 | #F6F2EA | 11px | 5,51 |
| `render_score()` · etiqueta, en panel | #5A6270 | #FBF8F2 | 11px | 5,80 |
| `render_score()` · denominador, en panel | #5A6270 | #FBF8F2 | 25,2px | 5,80 |
| `tabla()` · cabecera, en panel | #5A6270 | #FBF8F2 | 11px | 5,80 |
| `parrafo()` | #5A6270 | #F6F2EA | 15px | 5,51 |

**Dos defectos más del mismo tipo, detectados y NO corregidos aquí.** `.yidoca-mono`
y `.yidoca-highlight-eyebrow` son párrafos con clase suelta, así que `.stMarkdown p`
les roba color, tamaño y familia:

- `mono_caption()` sale hoy en Inter 15px #141A24. Debería ser JetBrains Mono
  13px #5A6270. El arreglo es contrastivamente seguro (5,51:1) pero cambia el
  aspecto de las dos demos.
- `highlight_block()` sale hoy con su eyebrow en Inter 15px #141A24. **Debería ser
  oro #B89968 a 11px, y no lo es: el bloque dorado no tiene oro.** Aquí el arreglo
  de especificidad no se puede aplicar sin más, porque #B89968 sobre #FBF8F2 da
  **2,54:1** y chocaría de frente con la regla de este ADR. Hay que decidir antes si
  se oscurece el oro para texto o si el oro se reserva a filetes y bordes —donde ya
  está el borde izquierdo del bloque, que sí se ve—.

Ambos comprobados inyectando la regla con el tipo delante en el stylesheet del body:
con ella, `.yidoca-mono` pasa a JetBrains Mono 13px `rgb(90,98,112)` y
`.yidoca-highlight-eyebrow` a 11px `rgb(184,153,104)`.

Versiones sobre las que se validó: Streamlit 1.58.0.
