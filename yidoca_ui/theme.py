"""
Tema visual Yidoca aplicado a Streamlit.

Centraliza CSS, tipografía y clases custom según GUIA_UI_YIDOCA.md (Sistema 2).
Las páginas llaman a aplicar_estilo_yidoca() al inicio para que todo se vea coherente.

Decisiones aplicadas:
 - Sistema 2 (crema + navy + oro) según guía sección 4.
 - Inter (sans), Instrument Serif (display editorial), JetBrains Mono (datos).
 - Sin emojis, sin sombras, sin gradientes, sin border-radius >12px.
 - Componentes custom: yidoca-eyebrow, yidoca-section-kicker, yidoca-panel,
   yidoca-highlight-block.
"""

import html
from contextlib import contextmanager

import streamlit as st


YIDOCA_TOKENS = """
        :root {
            /* Fondos */
            --color-bg: #F6F2EA;
            --color-bg-elev: #FBF8F2;
            --color-surface: #FFFFFF;

            /* Texto. Contraste medido sobre --color-bg (#F6F2EA):
               ink 15,63:1 · ink-muted 5,51:1 · ink-soft 2,91:1 */
            --color-ink: #141A24;
            --color-ink-muted: #5A6270;

            /* NO ES UN COLOR DE TEXTO. Con 2,91:1 no llega al 4,5:1 de AA ni
               al 3:1 de texto grande, y un eyebrow de 11px a ese contraste no
               se lee proyectado en una sala de reuniones. Su papel es todo lo
               que no es texto: filetes, divisorias, bordes suaves y estados
               desactivados. Para micro-etiquetas, ink-muted. Ver ADR 0004. */
            --color-ink-soft: #8A8F99;

            /* Bordes */
            --color-rule: #E2DCCF;
            --color-rule-soft: #ECE6D8;

            /* Acentos */
            --color-accent: #1E3A5F;
            --color-accent-deep: #0E1A33;
            --color-cream: #F1ECDF;
            --color-gold: #B89968;

            /* Tipografía */
            --font-sans: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            --font-serif: 'Instrument Serif', Georgia, 'Times New Roman', serif;
            --font-mono: 'JetBrains Mono', 'SF Mono', Menlo, monospace;
        }
"""


def aplicar_estilo_yidoca() -> None:
    """
    Inyecta el CSS Yidoca en la página actual de Streamlit.

    Llamar al inicio de cada página, justo después de st.set_page_config().
    """
    st.markdown(
        f"""
        <link rel="preconnect" href="https://fonts.googleapis.com">
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Instrument+Serif:ital@0;1&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">

        <style>
        /* ============================================================
           Variables CSS canónicas Yidoca (Sistema 2)
           ============================================================ */
        {YIDOCA_TOKENS}

        /* ============================================================
           Reset/base Streamlit
           NOTA: aplicamos Inter SOLO a elementos de TEXTO genéricos,
           NO a contenedores genéricos. Esto evita pisar iconos.
           ============================================================ */

        body, p, h1, h2, h3, h4, h5, h6, label, button, input, textarea, select {{
            font-family: var(--font-sans);
        }}

        .stApp, body, p, h1, h2, h3, h4, h5, h6, label {{
            color: var(--color-ink);
        }}

        /* FIX V2 — Iconos de Streamlit (BaseWeb).
           Streamlit usa un sistema de iconos con webfont. Los renderiza dentro
           de elementos con clases dinámicas tipo "emotion-cache-XXX epifhcv2".
           Algunos llevan caracteres especiales que cuando heredan Inter,
           muestran nombres crudos ("arrow_right", "POW_LIGHT", etc.).
           Estrategia: para CUALQUIER span dentro de un summary de expander,
           o cualquier elemento marcado como icono por BaseWeb, forzamos
           la familia de iconos. */

        /* Iconos dentro de expanders (las flechitas de abrir/cerrar) */
        details summary span[class*="emotion-cache"]:not([class*="MarkdownContainer"]),
        summary > span > span:first-child,
        details summary span > span:not([data-testid]):empty,
        details summary span:has(> svg),
        [data-baseweb] span[class*="epifhcv2"],
        span[class*="epifhcv"] {{
            font-family: 'Material Symbols Rounded', 'Material Symbols Outlined',
                         'Material Symbols Sharp', 'Material Icons' !important;
            font-feature-settings: 'liga';
            -webkit-font-feature-settings: 'liga';
            font-variation-settings: 'FILL' 0, 'wght' 400, 'GRAD' 0, 'opsz' 24;
        }}

        /* SVG dentro de cualquier componente BaseWeb — no tocar fuente */
        [data-baseweb] svg,
        [role="presentation"] svg,
        button svg,
        summary svg {{
            font-family: inherit !important;
        }}

        .stApp {{
            background: var(--color-bg);
        }}

        /* Ocultar elementos por defecto de Streamlit que ensucian */
        #MainMenu {{visibility: hidden;}}
        footer {{visibility: hidden;}}
        header[data-testid="stHeader"] {{
            background: transparent;
        }}

        /* Contenedor principal con margen lateral generoso */
        .main .block-container {{
            padding-top: 3rem;
            padding-bottom: 4rem;
            max-width: 1280px;
        }}

        /* ============================================================
           Tipografía
           ============================================================ */

        h1 {{
            font-family: var(--font-serif) !important;
            font-weight: 400 !important;
            font-size: clamp(2.25rem, 4vw, 3.25rem) !important;
            letter-spacing: -0.02em !important;
            line-height: 1.1 !important;
            color: var(--color-ink) !important;
            margin-bottom: 0.5rem !important;
        }}

        h2 {{
            font-family: var(--font-sans) !important;
            font-weight: 500 !important;
            font-size: 1.5rem !important;
            letter-spacing: -0.01em !important;
            line-height: 1.25 !important;
            color: var(--color-ink) !important;
            margin-top: 2.5rem !important;
            margin-bottom: 1rem !important;
        }}

        h3 {{
            font-family: var(--font-sans) !important;
            font-weight: 500 !important;
            font-size: 1.125rem !important;
            color: var(--color-ink) !important;
            margin-top: 1.75rem !important;
            margin-bottom: 0.75rem !important;
        }}

        /* Caption: texto secundario que va bajo títulos */
        [data-testid="stCaptionContainer"], .stCaption, caption {{
            color: var(--color-ink-muted) !important;
            font-size: 0.9375rem !important;
            line-height: 1.5 !important;
        }}

        /* Markdown body */
        .stMarkdown p {{
            font-family: var(--font-sans);
            font-size: 0.9375rem;
            line-height: 1.6;
            color: var(--color-ink);
        }}

        /* ============================================================
           Componentes Streamlit nativos
           ============================================================ */

        /* Botones — el contenedor */
        .stButton > button, .stFormSubmitButton > button {{
            background: var(--color-accent) !important;
            color: var(--color-bg) !important;
            border: none !important;
            border-radius: 4px !important;
            padding: 0.75rem 1.5rem !important;
            font-family: var(--font-sans) !important;
            font-weight: 500 !important;
            font-size: 0.875rem !important;
            letter-spacing: 0.01em !important;
            transition: background 200ms ease !important;
            box-shadow: none !important;
        }}

        .stButton > button:hover, .stFormSubmitButton > button:hover {{
            background: var(--color-accent-deep) !important;
            color: var(--color-bg) !important;
        }}

        .stButton > button:focus, .stFormSubmitButton > button:focus {{
            box-shadow: 0 0 0 2px var(--color-rule) !important;
            outline: none !important;
        }}

        /* FIX V2 — Texto interno de botones.
           El <p> dentro del botón hereda color de .stMarkdown p (navy oscuro).
           Forzamos color crema en TODOS los descendientes textuales del botón. */
        .stButton > button *,
        .stFormSubmitButton > button *,
        .stButton > button p,
        .stFormSubmitButton > button p,
        button[kind="primaryFormSubmit"] *,
        button[kind="primary"] *,
        button[kind="secondaryFormSubmit"] * {{
            color: var(--color-bg) !important;
        }}

        /* Inputs y textareas */
        .stTextInput input, .stTextArea textarea, .stNumberInput input {{
            background: var(--color-surface) !important;
            border: 1px solid var(--color-rule) !important;
            border-radius: 4px !important;
            font-family: var(--font-sans) !important;
            color: var(--color-ink) !important;
            font-size: 0.9375rem !important;
            caret-color: var(--color-ink) !important;
        }}

        .stTextInput input:focus, .stTextArea textarea:focus, .stNumberInput input:focus {{
            border-color: var(--color-accent) !important;
            box-shadow: none !important;
        }}

        /* FIX V2 — Caret-color con MÁXIMA especificidad.
           Streamlit aplica clases generadas (st-bc, st-ca, etc.) que ganan
           a .stTextInput input. Atacamos directamente input[type="text"] y
           el contenedor BaseWeb que envuelve los inputs. */
        input[type="text"],
        input[type="number"],
        input[type="email"],
        textarea,
        [data-baseweb="base-input"] input,
        [data-baseweb="input"] input,
        [data-baseweb="textarea"] textarea {{
            caret-color: var(--color-ink) !important;
            color: var(--color-ink) !important;
        }}

        /* Labels de inputs */
        .stTextInput label, .stTextArea label, .stNumberInput label,
        .stSelectbox label, .stMultiSelect label, .stCheckbox label {{
            font-family: var(--font-sans) !important;
            font-size: 0.8125rem !important;
            font-weight: 500 !important;
            color: var(--color-ink) !important;
        }}

        /* Multiselect tags */
        [data-baseweb="tag"] {{
            background: var(--color-accent) !important;
            border-radius: 4px !important;
            font-family: var(--font-sans) !important;
            font-size: 0.8125rem !important;
            font-weight: 500 !important;
        }}

        [data-baseweb="tag"],
        [data-baseweb="tag"] *,
        [data-baseweb="tag"] span,
        [data-baseweb="tag"] div {{
            color: var(--color-bg) !important;
        }}

        [data-baseweb="tag"] [role="button"] svg {{
            fill: var(--color-bg) !important;
            color: var(--color-bg) !important;
        }}

        [data-baseweb="tag"] [role="button"]:hover {{
            background: var(--color-accent-deep) !important;
        }}

        /* Expander */
        .streamlit-expanderHeader, [data-testid="stExpander"] summary {{
            background: var(--color-bg-elev) !important;
            border: 1px solid var(--color-rule-soft) !important;
            border-radius: 6px !important;
            font-family: var(--font-sans) !important;
            font-weight: 500 !important;
            color: var(--color-ink) !important;
        }}

        /* Alerts */
        [data-testid="stAlert"] {{
            border-radius: 4px;
            border: 1px solid var(--color-rule);
            background: var(--color-bg-elev);
            color: var(--color-ink);
            font-family: var(--font-sans);
            box-shadow: none;
        }}

        /* Divider */
        hr {{
            border: none;
            border-top: 1px solid var(--color-rule);
            margin: 2.5rem 0;
        }}

        /* Sidebar */
        [data-testid="stSidebar"] {{
            background: var(--color-bg-elev);
            border-right: 1px solid var(--color-rule-soft);
        }}

        [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {{
            color: var(--color-ink);
        }}

        /* ============================================================
           Clases custom Yidoca
           ============================================================ */

        /* Las micro-etiquetas llevan el tipo delante del selector por lo mismo
           que p.yidoca-parrafo: .stMarkdown p las gana si no. Y van en
           ink-muted, no en ink-soft: la jerarquía de un eyebrow la llevan el
           tamaño, el peso, las versalitas y el letter-spacing. Ver ADR 0004. */
        p.yidoca-eyebrow {{
            font-family: var(--font-sans);
            font-size: 0.6875rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.16em;
            color: var(--color-ink-muted);
            margin: 0 0 0.625rem 0;
        }}

        p.yidoca-section-kicker {{
            font-family: var(--font-sans);
            font-size: 0.6875rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.16em;
            color: var(--color-ink-muted);
            margin: 2rem 0 1rem 0;
            display: flex;
            align-items: center;
            gap: 0.625rem;
        }}

        p.yidoca-section-kicker::after {{
            content: '';
            flex: 1;
            height: 1px;
            background: var(--color-rule-soft);
        }}

        /* Párrafo de contexto: el que va bajo un section_kicker y explica de
           dónde salen las cifras que vienen debajo.

           El selector lleva el tipo delante (p.yidoca-parrafo) a propósito. La
           regla .stMarkdown p de más arriba fija color y line-height con la
           misma especificidad que una clase suelta, y ganaría por ser anterior.
           Con el tipo empatan y decide el orden, que aquí nos favorece. */
        p.yidoca-parrafo {{
            font-family: var(--font-sans);
            font-size: 0.9375rem;
            line-height: 1.65;
            color: var(--color-ink-muted);
            max-width: 62ch;
            margin: 0 0 1rem 0;
        }}

        /* ------------------------------------------------------------------
           Tabla editorial (guía 7.5). Sin bordes verticales, sin zebra, sin
           fondo de fila: lo que separa una tabla Yidoca de una rejilla de datos
           es lo que NO lleva. Ver ADR 0003.
           ------------------------------------------------------------------ */

        .yidoca-table {{
            width: 100%;
            border-collapse: collapse;
            font-family: var(--font-sans);
            font-size: 0.9375rem;
            margin: 0.25rem 0 1.5rem 0;
            background: transparent;
        }}

        .yidoca-table th {{
            font-family: var(--font-sans);
            font-size: 0.6875rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.14em;
            color: var(--color-ink-muted);
            background: transparent;
            padding: 0 1rem 0.75rem 1rem;
            border: none;
            border-bottom: 1px solid var(--color-rule);
            white-space: nowrap;
            vertical-align: bottom;
        }}

        .yidoca-table td {{
            /* Altura de fila generosa: esto se lee proyectado, a tres metros. */
            padding: 1rem;
            border: none;
            border-bottom: 1px solid var(--color-rule-soft);
            color: var(--color-ink);
            line-height: 1.45;
            background: transparent;
        }}

        .yidoca-table th:first-child, .yidoca-table td:first-child {{
            padding-left: 0;
        }}

        .yidoca-table th:last-child, .yidoca-table td:last-child {{
            padding-right: 0;
        }}

        .yidoca-table tbody tr:last-child td {{
            border-bottom: none;
        }}

        .yidoca-table .yidoca-td-derecha {{
            text-align: right;
            font-variant-numeric: tabular-nums;
        }}

        .yidoca-table .yidoca-td-izquierda {{
            text-align: left;
        }}

        /* Fila de total: la declara quien llama, no se adivina. */
        .yidoca-table tr.yidoca-fila-total td {{
            border-top: 2px solid var(--color-rule);
            font-weight: 600;
            color: var(--color-ink);
        }}

        .yidoca-panel {{
            background: var(--color-bg-elev);
            border: 1px solid var(--color-rule);
            border-radius: 10px;
            padding: 1.75rem 1.875rem;
            margin-bottom: 1.25rem;
        }}

        /* Panel Yidoca sobre el contenedor nativo de Streamlit.
           st.container(border=True) es lo unico que admite graficos y widgets
           dentro; un div propio abierto y cerrado en dos llamadas no los envuelve.
           Enganchamos por la clase que Streamlit genera desde la key (API
           publica) y no por data-testid: el testid del contenedor con borde es
           el mismo del bloque raiz y el de cada columna. Ver panel(). */
        [class*="st-key-yidoca_panel"] {{
            background: var(--color-bg-elev);
            border: 1px solid var(--color-rule);
            border-radius: 10px;
            padding: 1.5rem 1.625rem;
            margin-bottom: 1.25rem;
        }}

        .yidoca-highlight-block {{
            background: var(--color-bg-elev);
            border-left: 3px solid var(--color-gold);
            border-radius: 4px;
            padding: 1.25rem 1.5rem;
            margin: 1.75rem 0;
        }}

        .yidoca-highlight-eyebrow {{
            font-family: var(--font-sans);
            font-size: 0.6875rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.18em;
            color: var(--color-gold);
            margin: 0 0 0.625rem 0;
        }}

        .yidoca-highlight-text {{
            font-family: var(--font-sans);
            font-size: 0.9375rem;
            color: var(--color-ink);
            line-height: 1.6;
            font-style: italic;
            margin: 0;
        }}

        .yidoca-score-number {{
            font-family: var(--font-sans);
            font-size: clamp(2.5rem, 5vw, 3.5rem);
            font-weight: 400;
            letter-spacing: -0.04em;
            line-height: 1;
            font-variant-numeric: tabular-nums;
            color: var(--color-ink);
        }}

        /* Sin tipo delante: el denominador es un <span> y la etiqueta un <div>,
           así que .stMarkdown p no los alcanza. No se añade especificidad que
           no hace falta. Comprobado sobre el DOM (ADR 0004). */
        .yidoca-score-denom {{
            font-size: 0.45em;
            color: var(--color-ink-muted);
            font-weight: 500;
            letter-spacing: -0.02em;
            margin-left: 0.05em;
        }}

        .yidoca-score-label {{
            font-family: var(--font-sans);
            font-size: 0.6875rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.18em;
            color: var(--color-ink-muted);
            margin-top: 0.625rem;
        }}

        .yidoca-mono {{
            font-family: var(--font-mono);
            font-size: 0.8125rem;
            color: var(--color-ink-muted);
        }}

        .yidoca-wordmark {{
            font-family: var(--font-serif);
            font-size: 1.5rem;
            font-weight: 400;
            color: var(--color-ink);
            letter-spacing: -0.01em;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def eyebrow(texto: str) -> None:
    """Renderiza una eyebrow (kicker pequeño uppercase). Patrón universal Yidoca."""
    st.markdown(
        f'<p class="yidoca-eyebrow">{texto}</p>',
        unsafe_allow_html=True,
    )


def section_kicker(texto: str) -> None:
    """Renderiza un section kicker con línea decorativa. 'TÍTULO ────────'."""
    st.markdown(
        f'<p class="yidoca-section-kicker">{texto}</p>',
        unsafe_allow_html=True,
    )


def parrafo(texto: str) -> None:
    """
    Párrafo de contexto: el que va bajo un section_kicker y dice de dónde salen
    las cifras que vienen debajo.

    Cuerpo pequeño, color apagado y medida corta —62 caracteres— para que se lea
    de un vistazo. No lleva parámetros de color ni de ancho: el día que haga
    falta una variante se añade, y hasta entonces un parámetro que nadie usa es
    deuda.

        section_kicker("EL PIPELINE A 29 DE JULIO DE 2026")
        parrafo("Foto del CRM con 44 operaciones abiertas.")
    """
    st.markdown(
        f'<p class="yidoca-parrafo">{html.escape(texto)}</p>',
        unsafe_allow_html=True,
    )


def tabla(cabeceras: list[str],
          filas: list[list[str]],
          alineacion: list[str] | None = None,
          ultima_fila_total: bool = False) -> None:
    """
    Tabla editorial Yidoca. HTML propio, no `st.dataframe` ni `st.table`.

    Recibe **texto ya formateado**. La tabla no formatea números: quien llama es
    quien sabe si son euros, días o unidades, y quien conoce el criterio de
    redondeo de su demo.

    `alineacion` lleva "izquierda" o "derecha" por columna; por defecto todo a la
    izquierda. **Las columnas numéricas van a la derecha siempre**: una columna de
    importes alineada a la izquierda no se lee de un vistazo, que es el único uso
    que tiene una tabla en una demo. Las de la derecha llevan además cifras de
    ancho fijo, para que las unidades caigan una debajo de otra.

    `ultima_fila_total` marca la última fila con una línea superior más marcada y
    negrita. Se declara, no se adivina: una tabla de cuatro filas donde la cuarta
    resulta ser un total y una donde no lo es se escriben igual.

    No hay scroll, ni ordenación por clic, ni paginación. Es una tabla para mirar,
    no para operar; quien necesite operar necesita otra cosa (ADR 0003).

        tabla(["Comercial", "Deals", "En disputa"],
              [["Daniel Ferreras", "12", "184.200 €"],
               ["Marta Iglesias", "9", "-31.400 €"]],
              alineacion=["izquierda", "derecha", "derecha"])
    """
    n = len(cabeceras)
    if alineacion is None:
        alineacion = ["izquierda"] * n
    if len(alineacion) != n:
        raise ValueError(
            f"alineacion tiene {len(alineacion)} entradas y hay {n} columnas.")
    for valor in alineacion:
        if valor not in ("izquierda", "derecha"):
            raise ValueError(
                f'alineacion solo admite "izquierda" o "derecha", no {valor!r}.')
    for i, fila in enumerate(filas):
        if len(fila) != n:
            raise ValueError(
                f"la fila {i} tiene {len(fila)} celdas y hay {n} columnas.")

    clases = [f"yidoca-td-{lado}" for lado in alineacion]

    cabecera = "".join(f'<th class="{clase}">{html.escape(str(texto))}</th>'
                       for clase, texto in zip(clases, cabeceras))

    cuerpo = []
    for i, fila in enumerate(filas):
        es_total = ultima_fila_total and i == len(filas) - 1
        clase_fila = ' class="yidoca-fila-total"' if es_total else ""
        celdas = "".join(f'<td class="{clase}">{html.escape(str(celda))}</td>'
                         for clase, celda in zip(clases, fila))
        cuerpo.append(f"<tr{clase_fila}>{celdas}</tr>")

    # Sin saltos de línea ni sangrado: el markdown de Streamlit trata una línea
    # sangrada como bloque de código y partiría la tabla por la mitad.
    st.markdown(
        f'<table class="yidoca-table"><thead><tr>{cabecera}</tr></thead>'
        f'<tbody>{"".join(cuerpo)}</tbody></table>',
        unsafe_allow_html=True,
    )


def highlight_block(eyebrow_text: str, body_text: str) -> None:
    """
    Renderiza un highlight block con borde lateral oro.
    Reservado para recomendaciones consultivas, decisiones clave, momentos
    donde el lector debe parar. Su escasez le da peso.
    """
    st.markdown(
        f"""
        <div class="yidoca-highlight-block">
            <p class="yidoca-highlight-eyebrow">{eyebrow_text}</p>
            <p class="yidoca-highlight-text">{body_text}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def mono_caption(texto: str) -> None:
    """Caption en monoespaciada para datos técnicos: IDs, timestamps."""
    st.markdown(
        f'<p class="yidoca-mono">{texto}</p>',
        unsafe_allow_html=True,
    )


def render_score(
    valor: str | int | float,
    denominador: str | int | float | None = None,
    etiqueta: str | None = None,
) -> None:
    """
    Cifra grande editorial, con denominador y etiqueta opcionales.

    El denominador va ANIDADO dentro del número, no como hermano: su tamaño es
    0.45em y necesita resolverse contra el número, no contra el cuerpo de texto.

    No lleva delta ni indicador de tendencia a propósito. Para una nota debajo,
    usar mono_caption(), que ya existe.
    """
    denom_html = (
        f'<span class="yidoca-score-denom">/{html.escape(str(denominador))}</span>'
        if denominador is not None
        else ""
    )
    etiqueta_html = (
        f'<div class="yidoca-score-label">{html.escape(str(etiqueta))}</div>'
        if etiqueta
        else ""
    )
    st.markdown(
        f'<span class="yidoca-score-number">{html.escape(str(valor))}{denom_html}</span>'
        f"{etiqueta_html}",
        unsafe_allow_html=True,
    )


@contextmanager
def panel(nombre: str):
    """
    Panel Yidoca: contenedor elevado con borde suave.

    Envuelve st.container(border=True) en lugar de inyectar un div propio. Un
    <div> abierto en una llamada a st.markdown y cerrado en otra NO envuelve los
    elementos de en medio: Streamlit mete cada elemento en su propio contenedor.
    El contenedor nativo es lo único que admite gráficos y widgets dentro, que es
    lo que necesita una cabina de mando.

    El nombre es obligatorio y debe ser ÚNICO en la página: se convierte en la
    key del contenedor, y Streamlit lanza StreamlitDuplicateElementKey si dos
    elementos comparten key.

    De ese nombre sale la clase st-key-yidoca_panel_<nombre>, y de esa clase
    cuelga todo el aspecto del panel: la regla [class*="st-key-yidoca_panel"]
    de aplicar_estilo_yidoca. Es API pública de Streamlit (key -> clase CSS),
    a diferencia de los data-testid, pero sigue siendo acoplamiento: la versión
    de Streamlit queda fijada en todos los repos. Ver docs/adr/0002.

        with panel("forecast"):
            section_kicker("FORECAST")
            grafico_yidoca(mi_grafico)
    """
    with st.container(border=True, key=f"yidoca_panel_{nombre}"):
        yield
