"""yidoca_ui — sistema de diseño compartido de Yidoca para Streamlit."""

from yidoca_ui.theme import (
    YIDOCA_TOKENS,
    aplicar_estilo_yidoca,
    eyebrow,
    section_kicker,
    highlight_block,
    mono_caption,
    render_score,
    panel,
)
from yidoca_ui.graficos import (
    tema_yidoca,
    activar_tema_graficos,
    grafico_yidoca,
)

__all__ = [
    "YIDOCA_TOKENS",
    "aplicar_estilo_yidoca",
    "eyebrow",
    "section_kicker",
    "highlight_block",
    "mono_caption",
    "render_score",
    "panel",
    "tema_yidoca",
    "activar_tema_graficos",
    "grafico_yidoca",
]
