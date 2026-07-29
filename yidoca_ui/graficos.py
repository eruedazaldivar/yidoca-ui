"""yidoca_ui.graficos — tema de Altair y helper de pintado para Streamlit."""

import altair as alt

YIDOCA_RAMPA_NAVY = ["#97ADCB", "#748EB2", "#537098", "#35547D", "#1E3A5F"]
YIDOCA_CATEGORICA = ["#406AA2", "#AF843A"]
YIDOCA_DIVERGENTE = ["#2F4E77", "#5E7CA4", "#97ADCB", "#DBD7CF",
                     "#C3A678", "#9C7225", "#664605"]


@alt.theme.register("yidoca", enable=False)
def tema_yidoca() -> alt.theme.ThemeConfig:
    """Tema Altair de Yidoca. Se registra al importar, pero NO se activa solo."""
    tinta, tinta_media, tinta_suave = "#141A24", "#5A6270", "#8A8F99"
    regla, regla_suave = "#E2DCCF", "#ECE6D8"
    return alt.theme.ThemeConfig({
        "config": {
            "background": "#FBF8F2",
            "font": "Inter",
            "view": {"stroke": "transparent",
                     "continuousWidth": 400, "continuousHeight": 220},
            "title": {"font": "Inter", "fontSize": 13, "fontWeight": 500,
                      "color": tinta, "anchor": "start", "offset": 12,
                      "subtitleColor": tinta_media, "subtitleFontSize": 11,
                      "subtitleFontWeight": 400},
            "axis": {"labelFont": "Inter", "labelFontSize": 11,
                     "labelColor": tinta_suave, "labelPadding": 6,
                     "titleFont": "Inter", "titleFontSize": 10,
                     "titleFontWeight": 600, "titleColor": tinta_suave,
                     "titlePadding": 10, "domainColor": regla,
                     "tickColor": regla, "tickSize": 4,
                     "gridColor": regla_suave, "gridWidth": 1},
            "axisY": {"domain": False, "ticks": False, "labelPadding": 10},
            "axisX": {"grid": False},
            "legend": {"labelFont": "Inter", "labelFontSize": 11,
                       "labelColor": tinta_media, "titleFont": "Inter",
                       "titleFontSize": 10, "titleFontWeight": 600,
                       "titleColor": tinta_suave, "orient": "top",
                       "direction": "horizontal", "offset": 8,
                       "symbolType": "square", "symbolSize": 70},
            "line": {"strokeWidth": 2, "color": "#1E3A5F"},
            "bar": {"fill": "#406AA2", "cornerRadiusEnd": 4},
            "point": {"size": 64, "filled": True, "color": "#1E3A5F"},
            "rule": {"color": regla},
            "text": {"font": "Inter", "fontSize": 11, "color": tinta},
            "range": {"category": YIDOCA_CATEGORICA,
                      "ordinal": YIDOCA_RAMPA_NAVY,
                      "ramp": YIDOCA_RAMPA_NAVY,
                      "heatmap": YIDOCA_RAMPA_NAVY,
                      "diverging": YIDOCA_DIVERGENTE},
        }
    })


def activar_tema_graficos() -> None:
    """
    Activa el tema Yidoca en Altair. Llamar una vez al arrancar la aplicación.

    Va separada del registro a propósito: importar una librería no debe cambiar
    el aspecto de los gráficos de quien la importa. Simetría con
    aplicar_estilo_yidoca(), que tampoco se ejecuta sola.
    """
    alt.theme.enable("yidoca")


def grafico_yidoca(grafico, altura: int | None = None) -> None:
    """
    Pinta un gráfico Altair con el tema Yidoca en Streamlit.

    Existe porque st.altair_chart aplica su propio tema por defecto y pisa el
    nuestro: hay que pasarle theme=None siempre. Envolverlo aquí evita que
    alguien lo olvide en una demo futura.
    """
    import streamlit as st

    if altura is not None:
        grafico = grafico.properties(height=altura)
    st.altair_chart(grafico, theme=None, use_container_width=True)
