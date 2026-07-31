# ADR 0003 — La tabla se escribe a mano en lugar de usar st.dataframe

Fecha: 2026-07-31
Estado: Aceptado
Depende de: ADR 0001 (librería instalable, tokens aislados)

## Contexto

Con la Demo G suben dos componentes más, por la regla de siempre: un componente
sube cuando lo necesita más de una demo. `parrafo()` es mecánico —el estilo en
línea que la Demo G repetía en tres módulos, convertido en función—. `tabla()` no
lo es, porque hay dos formas de hacerla y una de ellas es un riesgo comercial.

Streamlit trae `st.dataframe` y `st.table`, y las dos funcionan. Escribir una
tabla propia en HTML es más código, más superficie de error y una función más que
mantener.

El problema es que **el riesgo de posicionamiento número uno de las demos del
stack es parecer una herramienta más**. En la Demo G está registrado con nombre:
*"parece un Tableau más"*. Y el aspecto de rejilla de datos —cabecera con fondo
sólido, líneas verticales, filas apretadas, ordenación por clic, la esquinita de
redimensionar— es exactamente lo que dispara esa lectura. No hace falta que el
cliente lo piense: lo reconoce antes de leer la primera cifra, porque es el
aspecto que ya tiene en su CRM y en su Excel.

Una demo que se vende a 20-25 k€ pierde esa venta en el primer pantallazo si el
cliente concluye "esto ya lo tengo".

## Decisión

`tabla()` compone HTML propio con la clase `.yidoca-table` y lo inyecta con un
solo `st.markdown`. No se usa `st.dataframe` ni `st.table` en ninguna demo.

Lo que la separa de una rejilla es sobre todo lo que **no** lleva:

- Sin bordes verticales, sin zebra, sin fondo de fila. La única línea es la
  divisoria horizontal, en `--color-rule-soft`, y la última fila no la lleva.
- Cabecera en versalitas pequeñas con `letter-spacing` amplio y color apagado,
  sobre fondo transparente y con una línea en `--color-rule` debajo. Nada de
  fondo navy sólido: eso es de los documentos, no de la UI de demo.
- Altura de fila generosa (padding vertical de 1rem, ~55 px de fila). Esto se lee
  en una reunión, proyectado, a tres metros, no en un monitor a cincuenta
  centímetros.
- Sin scroll, sin ordenación por clic, sin paginación. **Es una tabla para mirar,
  no para operar.** Quien necesite operar sobre los datos necesita otra cosa, y
  esa otra cosa no es una demo.

Tres decisiones de API que van con lo anterior:

**Recibe texto ya formateado.** La tabla no formatea números. Quien llama es quien
sabe si son euros, días o unidades, y quien conoce el criterio de redondeo de su
demo. Una tabla que formatea acaba con un parámetro por tipo de dato.

**`alineacion` es explícita, con "izquierda" o "derecha" por columna.** No se
adivina por el contenido: detectar "parece un número" falla con "12 deals", con
"−8.600 €" y con cualquier celda vacía, y falla en silencio. Por defecto todo a la
izquierda; las columnas numéricas se pasan a la derecha siempre, y ahí van además
con cifras de ancho fijo (`tabular-nums`) para que las unidades caigan una debajo
de otra.

**`ultima_fila_total` se declara, no se deduce.** Una tabla de cuatro filas donde
la cuarta es un total y una donde no lo es se escriben exactamente igual. Marcada,
la fila lleva línea superior de 2 px en `--color-rule` —el doble de peso que las
divisorias— y negrita.

## Alternativas consideradas

- **`st.dataframe` con CSS encima.** Rechazada. Su DOM son clases `emotion-cache`
  generadas y una capa de virtualización (glide-data-grid) que renderiza celdas en
  canvas: buena parte del aspecto no es alcanzable desde CSS, y lo que sí lo es
  depende de hashes que cambian entre versiones. El ADR 0001 ya advertía de eso
  para las clases emotion; aquí sería peor, porque el componente entero está
  construido para ser una rejilla interactiva.
- **`st.table`.** Rechazada. Es más domable que `st.dataframe` —renderiza un
  `<table>` de verdad— pero obliga a un pandas.DataFrame de entrada, arrastra el
  índice, y sigue trayendo la cabecera con fondo y las líneas de rejilla que hay
  que apagar una a una. Se acaba escribiendo el mismo CSS que aquí, con una
  dependencia de pandas y menos control sobre el marcado.
- **`st.columns` + `render_score` o markdown por celda.** Rechazada. No hay forma
  de alinear las columnas entre filas: cada fila es un contenedor independiente y
  el ancho lo reparte Streamlit. Una tabla cuyas columnas no cuadran verticalmente
  es peor que ninguna.
- **Aceptar el aspecto de rejilla y ahorrarse el componente.** Rechazada por lo
  del Contexto. Es la alternativa barata y es la que pierde la venta.

## Consecuencias

- Positivas: las tablas de todas las demos se ven igual y se ven Yidoca. El
  aspecto vive en `.yidoca-table`, así que cambiarlo es una edición en un sitio.
  Al ser HTML propio no hay acoplamiento a la versión de Streamlit, a diferencia
  de `panel()` (ADR 0002): esta es la parte de la librería que menos se va a
  romper sola.
- Negativas / coste: quien llama tiene que formatear cada celda y decidir la
  alineación. Es trabajo real en cada demo, y es deliberado —ver las tres
  decisiones de API—.
- La tabla escapa todo su contenido con `html.escape`. No admite negrita ni
  enlaces dentro de una celda. Si algún día hace falta, se añade con una lista
  blanca explícita, nunca desactivando el escapado.
- `parrafo()` usa el selector `p.yidoca-parrafo`, con el tipo delante. La regla
  `.stMarkdown p` de `aplicar_estilo_yidoca` fija color y `line-height` con la
  misma especificidad que una clase suelta y, siendo anterior en la hoja, ganaría.
  Con el tipo delante empatan y decide el orden. Comprobado sobre el DOM real: el
  párrafo mide `rgb(90,98,112)` = `#5A6270` = `--color-ink-muted`.

## Notas

Verificado con Playwright sobre la página en ejecución, no solo por import.
Medidas reales: cabecera `#8A8F99` sobre fondo transparente con línea inferior
`#E2DCCF` de 1 px; celdas `#141A24` con divisoria `#ECE6D8` de 1 px y cero bordes
laterales; fondo de las cinco filas transparente (no hay zebra); fila de total con
borde superior de 2 px `#E2DCCF`, peso 600 y sin borde inferior; alto de fila
54,75 px; columnas numéricas a la derecha con `tabular-nums`.

**Defecto anterior detectado y no corregido aquí.** En la misma medición,
`eyebrow()` y `section_kicker()` salen en `rgb(20,26,36)` (`--color-ink`) cuando la
guía pide `--color-ink-soft`. Es el mismo choque de especificidad contra
`.stMarkdown p`, y se arregla igual: `p.yidoca-eyebrow` y `p.yidoca-section-kicker`
en lugar de las clases sueltas. No se toca en este commit porque cambia el aspecto
de las dos demos ya publicadas y esa es una decisión de diseño, no de librería.

Versiones sobre las que se validó: Streamlit 1.58.0.
