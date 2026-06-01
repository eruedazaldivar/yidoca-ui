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

import streamlit as st


YIDOCA_TOKENS = """
        :root {
            /* Fondos */
            --color-bg: #F6F2EA;
            --color-bg-elev: #FBF8F2;
            --color-surface: #FFFFFF;

            /* Texto */
            --color-ink: #141A24;
            --color-ink-muted: #5A6270;
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

        .yidoca-eyebrow {{
            font-family: var(--font-sans);
            font-size: 0.6875rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.16em;
            color: var(--color-ink-soft);
            margin: 0 0 0.625rem 0;
        }}

        .yidoca-section-kicker {{
            font-family: var(--font-sans);
            font-size: 0.6875rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.16em;
            color: var(--color-ink-soft);
            margin: 2rem 0 1rem 0;
            display: flex;
            align-items: center;
            gap: 0.625rem;
        }}

        .yidoca-section-kicker::after {{
            content: '';
            flex: 1;
            height: 1px;
            background: var(--color-rule-soft);
        }}

        .yidoca-panel {{
            background: var(--color-bg-elev);
            border: 1px solid var(--color-rule);
            border-radius: 10px;
            padding: 1.75rem 1.875rem;
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

        .yidoca-score-denom {{
            font-size: 0.45em;
            color: var(--color-ink-soft);
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
            color: var(--color-ink-soft);
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
