# ADR 0007 — El bloque dorado acota su medida a 68ch

Fecha: 2026-10-05
Estado: Aceptado
Depende de: ADR 0004 (el tipo delante en toda clase servida sobre un `<p>`),
ADR 0005 (dos oros), ADR 0006 (la tabla se ajusta a su contenido)

## Contexto

`highlight_block` nació para **una frase corta**: el cierre de la Demo B, dos
líneas de recomendación consultiva. El momento 3 de la Demo G lo usa para otra
cosa — cuatro decisiones de tres y cuatro líneas cada una, que son el contenido
más importante de toda la demo.

Medido sobre el DOM en marcha, con la pestaña "Las decisiones" a 1.440 px de
viewport:

| Bloque | Ancho | Líneas | Máx. caracteres por línea |
|---|---|---|---|
| 1 | 1.229 px | 3 | 174 |
| 2 | 1.229 px | 2 | 173 |
| 3 | 1.229 px | 3 | 175 |
| 4 | 1.229 px | 4 | 176 |

**176 caracteres por línea, en cursiva.** La medida cómoda de lectura está entre
60 y 75 caracteres (en unidades `ch`); `parrafo()` va a 62ch desde el principio.
Un bloque de cuatro líneas de 176 caracteres es exactamente donde el ojo pierde
el renglón al volver al margen izquierdo, y pasa en la pantalla que más atención
pide de la demo.

## Decisión

```css
p.yidoca-highlight-text { max-width: 68ch; }
```

**Se acorta solo la línea de texto.** El `div` del bloque —su fondo y su filete
dorado— sigue ocupando el ancho completo, que es lo que le da peso en la página y
lo que hace que el oro funcione como señal. Lo que se acota es la medida
tipográfica, no el elemento.

**68ch y no 62ch** como el párrafo: un bloque destacado puede permitirse ser algo
más ancho que el cuerpo corrido, y la proporción resultante (1,10×) se mantiene
estable porque las dos medidas están en la misma unidad.

**La cursiva se queda.** Es parte de la identidad del componente, y a 68
caracteres se lee sin esfuerzo; lo que la hacía incómoda era la medida, no la
inclinación.

**El prefijo de tipo no es opcional** (ADR 0004): `.stMarkdown p` le robaría la
declaración a una clase suelta.

### Medido después, en el mismo sitio y con el mismo método

| | Ancho | Máx. caract./línea | Media |
|---|---|---|---|
| `parrafo()` a 62ch (referencia del sistema) | 587 px | 81 | 73 |
| `highlight_block` a 68ch | 643 px | 94 | 84 |
| `highlight_block` antes | 1.229 px | 176 | 147 |

La proporción entre los dos componentes (643/587 = 1,095) reproduce la de sus
`max-width` (68/62 = 1,097), que es la comprobación de que la unidad se comporta
como se espera.

**Nota sobre `ch` frente a caracteres reales**, porque induce a error al medir:
`1ch` es el ancho del glifo **"0"**, de los más anchos de la fuente. El texto
real —minúsculas, espacios— es más estrecho, así que `68ch` da unos 94 caracteres
reales por línea, no 68. Los dos números son correctos; lo que no se puede es
compararlos entre sí. La referencia sigue siendo `parrafo()`, medido igual.

## Alternativas consideradas

- **Acotar el `div` entero en lugar del `<p>`.** Rechazada: encoge el filete
  dorado y el fondo, y con ellos la presencia del bloque en la página. El
  componente dejaría de leerse como un alto en el recorrido.
- **Arreglarlo en la Demo G** envolviendo el texto o partiéndolo en varios
  bloques. Rechazada: es un defecto del componente, no de quien lo usa. Cualquier
  otra demo con un bloque de tres líneas tropezaría con lo mismo.
- **Un parámetro de anchura en la firma.** Rechazada por lo de siempre (ADR
  0006): un parámetro que hoy nadie necesita es deuda, y delega en cada demo una
  decisión que debe ser la misma en todas.
- **Quitar la cursiva.** Rechazada: no era el problema, y es seña de identidad del
  componente.

## Consecuencias

- Las decisiones del momento 3 pasan de 3-4 líneas larguísimas a 4-7 líneas de
  medida cómoda, alineadas con el resto del texto de la página.
- **El único consumidor hoy es la Demo G.** Se comprobó: la Demo B importa
  `yidoca_ui` pero solo `aplicar_estilo_yidoca`, `eyebrow`, `section_kicker` y
  `mono_caption` — nunca llamó a `highlight_block`, así que no cambia. Los otros
  dos proyectos que usan un bloque dorado (`yidoca-outreach-pipeline` y Hermes)
  llevan su propia copia del tema y no consumen esta librería.
- Un bloque de una sola frase corta —el uso original— no cambia: ya medía menos
  de 68ch.

## Notas

Medido sobre el DOM y no sobre la captura, recorriendo el nodo de texto carácter
a carácter con `Range.getClientRects()` y detectando el salto de línea por cambio
de `top`. Es la única forma de contar caracteres por **línea visual**: el ancho en
píxeles no dice cuántos caben, y una captura no se puede contar.

Y vuelve a aplicar la nota del ADR 0006: al tocar la librería hay que **reiniciar
el servidor** de la demo. Streamlit reejecuta el script pero no reimporta los
módulos ya cargados, así que el CSS viejo sigue sirviéndose y parece que el
cambio no surte efecto.
