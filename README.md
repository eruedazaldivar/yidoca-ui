# yidoca-ui

Sistema de diseño compartido de Yidoca (Sistema 2: crema + navy + oro) para demos en Streamlit.

Fuente única de verdad de la identidad visual. Las demos lo instalan en modo editable:

    pip install -e ../yidoca-ui

Uso:

    from yidoca_ui import aplicar_estilo_yidoca, eyebrow, section_kicker, highlight_block, mono_caption

    aplicar_estilo_yidoca()  # al inicio de cada página, tras st.set_page_config()

Origen: extraído de yidoca-outreach-pipeline/core/ui_theme.py (super-demo) y promovido a librería independiente en junio 2026.

## Decisiones de arquitectura

Por qué esto es una librería instalable (y no CSS copiado en cada demo), por qué los tokens de diseño están aislados en una constante, y por qué el repo es público: ver docs/adr/0001-libreria-instalable-tokens-aislados.md.
