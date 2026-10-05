# ADR 0008 — Las fuentes viajan dentro del paquete

Fecha: 2026-10-05
Estado: Aceptado
Depende de: ADR 0007 (la medida del bloque dorado)

## Contexto

La librería cargaba Inter, Instrument Serif y JetBrains Mono desde
`fonts.googleapis.com` con un `<link>` en el CSS que inyecta
`aplicar_estilo_yidoca()`.

Eso falla en el sitio donde más caro sale: **un pabellón de feria**. Sin red, la
página cae a las fuentes del sistema, el titular deja de ser Instrument Serif, el
cuerpo deja de ser Inter, y toda la pantalla cambia de aspecto delante de quien la
está mirando. No se cae: se ve mal, que es peor, porque no hay nada que arreglar
sobre la marcha.

Y hay un segundo motivo que pesa igual fuera de la feria: **una consultora que
entra en la red de un cliente y le pide tres ficheros a un tercero está haciendo
justo lo que no debe**.

## Decisión

Las tres familias viajan dentro del paquete como woff2 subconjuntados, y se
embeben en base64 en el mismo CSS que ya se inyecta. **Ninguna petición externa.**

- `yidoca_ui/fuentes/*.woff2` — siete caras: Inter 400/500/600, Instrument Serif
  normal y cursiva, JetBrains Mono 400/500.
- `herramientas/empaquetar_fuentes.py` las descarga de los repositorios oficiales
  de Google Fonts, instancia los ejes variables en el peso concreto, subconjunta
  y guarda. Se ejecuta a mano; su salida va al repositorio.
- Las tres son OFL 1.1 y el texto de cada licencia viaja junto a los ficheros.

**El subconjunto** es ASCII imprimible, los acentos y signos del español, y los
tipográficos que las demos usan de verdad: `− · — « » ≥ € ± ✓ ✗`. 154 caracteres.

| | Tamaño |
|---|---|
| woff2 en disco, las siete caras | 128,0 KB |
| CSS de fuentes (base64) | 172,2 KB |
| CSS estático (el de siempre) | 19,8 KB |
| **CSS total inyectado** | **192,1 KB** |

Menos de la mitad del tope de 400 KB que se había fijado.

**`font-display: block`** y no `swap`: con las fuentes embebidas no hay descarga
que esperar, así que no existe el parpadeo que `swap` viene a evitar, y `block`
elimina el destello de fuente del sistema en el primer pintado.

**`_css_fuentes()` se cachea con `lru_cache`**: son 172 KB de base64 y
`aplicar_estilo_yidoca()` se llama en cada reejecución del script de Streamlit,
que son muchas.

**`package-data` en `pyproject.toml`.** Sin eso, una instalación desde git deja
`yidoca_ui/fuentes` vacío y el tema cae a las fuentes del sistema **en silencio**:
exactamente el fallo que este ADR viene a cerrar, y de los que no se ven hasta que
estás delante del cliente.

## Alternativas consideradas

- **Servir los woff2 como estáticos de Streamlit.** Rechazada: Streamlit no expone
  un directorio de estáticos que una librería instalada pueda usar sin que cada
  demo lo configure, y lo que funciona en local tiene que funcionar igual en
  Streamlit Cloud.
- **Descargar las fuentes la primera vez y cachearlas en disco.** Rechazada: sigue
  necesitando red una vez, y esa vez puede ser la de la feria.
- **Quedarse con las fuentes del sistema.** Rechazada: la identidad visual de las
  demos es medio producto.

## Consecuencias

- La demo se ve **idéntica con red y sin red**. Comprobado abortando en Playwright
  toda petición que no vaya a localhost y comparando las capturas: mismo sha256.
- Las siete caras aparecen como `loaded` en `document.fonts`; cero peticiones a
  `fonts.googleapis.com` o `fonts.gstatic.com`.
- Los iconos de Streamlit (Material Symbols) **no dependen de la red**: salen como
  `unloaded` tanto con red como sin ella, y la pantalla no cambia.
- Quedan dos peticiones externas que **no son de esta librería** sino de la
  telemetría de Streamlit (`data.streamlit.io/metrics.json` y un webhook de
  Fivetran). Se desactivan por demo con `gatherUsageStats = false` en
  `.streamlit/config.toml`; queda anotado aquí porque es lo que completa la
  promesa de "ninguna petición a terceros".
- `herramientas/` es nuevo y no forma parte del paquete instalado.

## Notas

El subsetter revienta con `KeyError: 'space.tf'` si se le pasa directamente la
fuente que devuelve `instantiateVariableFont`: quedan referencias a glifos
intermedios en las tablas de variación. Se arregla guardando a bytes y recargando
antes de subconjuntar, que es lo que hace `_instancia()`.

Y sigue aplicando la nota del ADR 0006: al tocar la librería hay que **reiniciar
el servidor** de la demo; Streamlit no reimporta los módulos ya cargados.
