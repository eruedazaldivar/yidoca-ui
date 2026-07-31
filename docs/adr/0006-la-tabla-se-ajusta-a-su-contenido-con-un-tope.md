# ADR 0006 — La tabla se ajusta a su contenido con un tope, no al ancho de la pantalla

Fecha: 2026-07-31
Estado: Aceptado
Depende de: ADR 0003 (la tabla se escribe a mano)

## Contexto

`tabla()` nació con `width: 100%`, que es lo que hace por defecto cualquier tabla
de dashboard. En un monitor panorámico eso deja la tabla del momento 1 de la Demo G
a 1.440 px de ancho, con tres columnas: entre la etiqueta de una fila —"Contacto"—
y su primer número —"10"— quedan más de 700 px de crema.

**El ojo no une esos dos datos.** Hay que barrer la pantalla de izquierda a derecha
por cada fila, y proyectado en una reunión eso es una lectura perdida por fila. Es
además, visualmente, exactamente lo que el ADR 0003 quería evitar: una hoja de
cálculo que ocupa el escritorio.

## Decisión

La tabla se **ajusta a su contenido** —`width: auto`— con un tope de `58rem`
(928 px) y `margin-right: auto` para que quede pegada a la izquierda, alineada con
la columna editorial del resto de la página. No centrada: centrarla la desancla del
texto que la precede.

`max-width` va como `min(58rem, 100%)`. El `100%` es la salvaguarda para una
ventana estrecha: la tabla envuelve el texto en lugar de desbordar el contenedor y
sacarle barra horizontal a la página.

Las celdas numéricas llevan `white-space: nowrap`, para que un importe no se parta
en dos líneas.

Medidas resultantes, idénticas a 2560, 1600 y 760 px de viewport —el ancho lo manda
el contenido, no la pantalla—:

| Tabla | Columnas | Ancho | Hueco etiqueta → primer número |
|---|---|---|---|
| Momento 1 de la Demo G | 3 | 339 px | 133 px |
| Momento 2, con la lectura por evidencia | 6 | 669 px | 133 px |
| Deals en disputa, primera columna larga | 4 | 634 px | 32 px |
| Dos columnas de texto | 2 | 409 px | 74 px |

El tope de 58 rem no lo alcanza ninguna de las cuatro. Está para el caso
patológico —una celda de texto muy largo—, donde prefiere envolver a seguir
creciendo.

## Alternativas consideradas

- **`width: 100%` con `max-width`, y `width: 1%` en las columnas numéricas para que
  la primera se lleve el sobrante.** Es el recurso clásico y fue el primer intento.
  **No funciona aquí, y falla justo en lo que se venía a arreglar:** una anchura en
  porcentaje sobre las celdas empuja la tabla hasta el tope, así que la tabla de
  tres columnas se iba a 928 px y la primera columna se quedaba 694 px de los 928.
  El hueco entre la etiqueta y su número seguía siendo de 722 px. Medido, no
  supuesto. Con la tabla ajustada al contenido no hay sobrante que repartir y el
  problema desaparece en lugar de mudarse.
- **Un ancho fijo en rem para todas las tablas.** Rechazada: una tabla de dos
  columnas y una de seis no quieren el mismo ancho, y cualquier valor único deja
  una de las dos mal.
- **Un parámetro `ancho` en la firma de `tabla()`.** Rechazada por lo de siempre:
  un parámetro que hoy nadie necesita es deuda, y además delega en cada demo una
  decisión que debe ser la misma en todas.
- **Centrarla.** Rechazada: la desancla del `section_kicker` y del párrafo que la
  preceden, que sí empiezan en el margen izquierdo.

## Consecuencias

- Positiva: la tabla es un bloque compacto y una fila se lee de un vistazo. El
  ancho ya no depende del monitor en el que se proyecte la demo.
- La tabla del momento 1 pasa de 1.440 px a 339 px y se lee como un bloque pequeño
  bajo cuatro fichas que sí ocupan todo el ancho. Es deliberado: son dos objetos
  distintos y no tienen por qué medir lo mismo.
- Las columnas quedan separadas solo por su padding —32 px entre dos numéricas
  contiguas—. Si en el momento 2, con seis columnas de importes, eso resulta
  apretado al proyectarlo, lo que se toca es el padding de la celda, no el ancho de
  la tabla.

## Notas

Comprobado sobre el DOM en marcha con cuatro formas de tabla y tres viewports
(2560, 1600 y 760 px). Ninguna produce barra horizontal en la página:
`scrollWidth == innerWidth` en los tres.

Al medir la primera versión pareció que el CSS no surtía efecto: era el servidor de
Streamlit, que tenía `yidoca_ui.theme` cacheado en `sys.modules` desde el arranque.
Streamlit reejecuta el script principal cuando cambia un fichero pero no reimporta
los módulos. Al tocar la librería hay que reiniciar el servidor de la demo, no solo
guardar.

Versiones sobre las que se validó: Streamlit 1.58.0.
