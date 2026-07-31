# yidoca-ui

Sistema de diseño compartido de Yidoca (Sistema 2: crema + navy + oro) para demos en Streamlit.

Fuente única de verdad de la identidad visual. Las demos lo instalan en modo editable:

    pip install -e ../yidoca-ui

Uso:

    from yidoca_ui import aplicar_estilo_yidoca, eyebrow, section_kicker, parrafo, tabla

    aplicar_estilo_yidoca()  # al inicio de cada página, tras st.set_page_config()

Origen: extraído de yidoca-outreach-pipeline/core/ui_theme.py (super-demo) y promovido a librería independiente en junio 2026.

## Componentes

| Función | Para qué |
|---|---|
| `aplicar_estilo_yidoca()` | Inyecta el CSS. Al inicio de cada página, tras `st.set_page_config()`. |
| `eyebrow(texto)` | Kicker pequeño en versalitas. |
| `section_kicker(texto)` | Título de sección con línea decorativa. |
| `parrafo(texto)` | Párrafo de contexto bajo un section_kicker: cuerpo pequeño, apagado, medida corta. |
| `render_score(valor, denominador, etiqueta)` | Cifra grande editorial. |
| `tabla(cabeceras, filas, alineacion, ultima_fila_total)` | Tabla editorial. Recibe texto ya formateado. |
| `panel(nombre)` | Contenedor elevado, como context manager. Nombre único por página. |
| `highlight_block(eyebrow, cuerpo)` | Bloque con borde oro. Solo para decisiones y recomendaciones. |
| `mono_caption(texto)` | Caption monoespaciada para IDs y timestamps. |
| `activar_tema_graficos()` / `grafico_yidoca(g)` | Tema de Altair. |

El oro (`highlight_block`) no es decorativo: solo donde hay decisión consultiva o
recomendación. Su escasez le da peso. Y son **dos** tokens: `--color-gold` #B89968
para filetes, bordes y rellenos, `--color-gold-ink` #816A46 para cualquier texto en
oro. No son intercambiables — el de marca da 2,54:1 y no se lee (ADR 0005).

`tabla()` recibe texto **ya formateado** y la alineación por columna: no formatea
números ni adivina cuáles lo son. Las columnas numéricas van a la derecha siempre.

    tabla(["Comercial", "Deals", "En disputa"],
          [["Daniel Ferreras", "12", "184.200 €"],
           ["Marta Iglesias", "9", "−31.400 €"]],
          alineacion=["izquierda", "derecha", "derecha"])

## Decisiones de arquitectura

Por qué esto es una librería instalable (y no CSS copiado en cada demo), por qué los tokens de diseño están aislados en una constante, y por qué el repo es público: ver docs/adr/0001-libreria-instalable-tokens-aislados.md.

Por qué panel() envuelve el contenedor nativo de Streamlit en vez de inyectar un div propio, y por qué eso ata la versión de Streamlit: ver docs/adr/0002-panel-envuelve-contenedor-nativo-streamlit.md.

Por qué tabla() se escribe a mano en lugar de usar st.dataframe o st.table —el aspecto de rejilla de datos es el riesgo de posicionamiento número uno de las demos—: ver docs/adr/0003-tabla-escrita-a-mano-en-lugar-de-st-dataframe.md.

Por qué todo texto va a 4,5:1 o mejor sobre su fondo, por qué las micro-etiquetas cambian a --color-ink-muted y por qué --color-ink-soft deja de ser un color de texto: ver docs/adr/0004-contraste-minimo-y-nuevo-papel-de-ink-soft.md.

Por qué el oro se parte en dos tokens, y la regla general de cuándo un color que no pasa contraste se retira del texto y cuándo se le hace una variante del mismo tono: ver docs/adr/0005-dos-oros-gold-para-filete-gold-ink-para-texto.md.

## Contraste

Regla del Sistema 2: **cualquier texto que el espectador tenga que leer va a 4,5:1 o mejor sobre su fondo real** (ADR 0004). Sobre el crema de página #F6F2EA:

| Token | Ratio | Para texto |
|---|---|---|
| `--color-ink` #141A24 | 15,63:1 | sí |
| `--color-ink-muted` #5A6270 | 5,51:1 | sí |
| `--color-gold-ink` #816A46 | 4,61:1 | sí, el oro de texto |
| `--color-ink-soft` #8A8F99 | 2,91:1 | **no** — filetes, divisorias, desactivados |
| `--color-gold` #B89968 | 2,41:1 | **no** — filetes, bordes, rellenos |

Un color decorativo que no pasa contraste se retira del texto; uno con carga semántica se corrige con una variante del mismo tono (ADR 0005).
