# ADR 0002 — panel() envuelve el contenedor nativo de Streamlit y engancha el CSS por la key

Fecha: 2026-07-29
Estado: Aceptado

## Contexto

La Demo G (cabina de mando del CEO/CFO) es la segunda demo del stack, y era la condición acordada para promover componentes a yidoca-ui: un componente sube cuando dos demos lo necesitan. Con ella suben el tema de gráficos (yidoca_ui/graficos.py) y las dos funciones cuyo CSS ya vivía aquí desde la sesión 22 sin su parte Python: render_score y panel.

El CSS de .yidoca-panel (fondo elevado, borde crema, esquinas de 10px) existía desde la sesión 22, pero nunca tuvo función que lo pintara. La forma obvia de escribirla —la misma que usan eyebrow, section_kicker o highlight_block— sería inyectar un `<div class="yidoca-panel">` con st.markdown. No funciona para un panel.

Streamlit envuelve cada llamada a st.markdown en su propio contenedor del DOM. Un `<div>` abierto en una llamada y cerrado en otra no envuelve los elementos de en medio: quedan como hermanos del div vacío, no como hijos. Sirve para un bloque de texto cerrado en una sola llamada (highlight_block), pero no para un contenedor que debe albergar gráficos y widgets, que es justo lo que necesita una cabina de mando.

## Decisión

panel() es un context manager que envuelve `st.container(border=True)`, el contenedor nativo de Streamlit, en lugar de inyectar HTML propio. El aspecto Yidoca se le aplica desde el CSS de aplicar_estilo_yidoca.

Eso obliga a una segunda decisión: cómo engancha el CSS a ese contenedor nativo.

panel() lleva nombre obligatorio, que se convierte en la key del contenedor (`key=f"yidoca_panel_{nombre}"`). Streamlit deriva de la key una clase CSS `st-key-<key>`, y la regla ataca `[class*="st-key-yidoca_panel"]`. El nombre debe ser único en la página: Streamlit lanza StreamlitDuplicateElementKey si dos elementos comparten key.

## Alternativas consideradas

- Inyectar un `<div class="yidoca-panel">` propio con st.markdown, abriendo y cerrando en dos llamadas. Rechazada: no envuelve los elementos de en medio (ver Contexto). El CSS de .yidoca-panel se conserva igualmente en el bloque `<style>`, porque sigue siendo válido para un panel de contenido cerrado.
- Atacar `[data-testid="stVerticalBlockBorderWrapper"]`. Rechazada: ese atributo no existe en Streamlit 1.58.0. Se comprobó contra el DOM real con Playwright — el selector devolvía cero elementos, y lo que se veía en pantalla era el borde por defecto de Streamlit (`rgba(49,51,63,0.2)`, radio 8px, padding 15px), no el nuestro.
- Atacar `[data-testid="stVerticalBlock"]`, que es quien lleva el borde en 1.58. Rechazada: es el mismo testid del bloque raíz de la página y el de cada columna. Pintaría de panel media aplicación.
- Atacar la clase emotion del contenedor con borde (`st-emotion-cache-1ne20ew`). Rechazada: es un hash generado que cambia entre versiones y entre builds. Inservible como contrato.
- Dejar el borde por defecto de Streamlit y no tematizar el panel. Rechazada: el gris azulado de Streamlit rompe el Sistema 2, y el panel sin fondo elevado deja ver el `#F6F2EA` de la página, con lo que el gráfico (fondo `#FBF8F2` por el tema de Altair) se recorta dentro del panel como un rectángulo más claro.

## Consecuencias

- Positivas: el panel admite gráficos, widgets y cualquier elemento de Streamlit dentro, que es el requisito de la cabina de mando. La key→clase es API pública documentada de Streamlit, bastante más firme que un data-testid o un hash de emotion. El nombre obligatorio, además de dar la clase, documenta cada panel en el código de la demo.
- Negativas / coste: la librería queda atada a la versión de Streamlit, como ya advertía el ADR 0001 sobre las clases emotion-cache. Si Streamlit cambia el prefijo `st-key-`, todos los paneles de todas las demos pierden el estilo a la vez. La versión de Streamlit debe mantenerse alineada entre yidoca-ui y las demos que la consumen.
- El nombre único por página es una carga que el desarrollador de la demo tiene que llevar: un nombre repetido no degrada el estilo, revienta la página con StreamlitDuplicateElementKey.

## Notas

Verificado contra el DOM real con Playwright sobre la app en ejecución, no solo por import. Con la regla enganchada, el contenedor mide: fondo `rgb(251,248,242)` (#FBF8F2), borde `1px solid rgb(226,220,207)` (#E2DCCF), radio 10px, padding 24×26px. Sin doble padding: el hueco real entre el borde y el primer hijo es de 25px = 24 de padding + 1 de borde, o sea que la regla sustituye el padding de Streamlit en vez de sumarse. Ningún otro stVerticalBlock de la página resultó pintado.

En la misma sesión se corrigió el registro del tema de Altair: `@alt.theme.register("yidoca", enable=False)` en lugar de `enable=True`, más una función activar_tema_graficos() explícita. Un import no debe tener efectos globales sobre el aspecto de los gráficos de quien importa; la simetría es con aplicar_estilo_yidoca(), que tampoco se ejecuta sola. En altair 6.1.0 el argumento `enable` es keyword-only y obligatorio, así que omitirlo no es opción: hay que pasar `enable=False`.

Versiones sobre las que se validó: Streamlit 1.58.0, Altair 6.1.0.
