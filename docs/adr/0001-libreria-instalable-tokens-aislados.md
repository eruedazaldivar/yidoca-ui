# ADR 0001 — yidoca-ui como librería instalable, pública, con tokens de diseño aislados

Fecha: 2026-06-01
Estado: Aceptado

## Contexto

El stack Yidoca contempla 7 demos (A-G). Cada una es una app Streamlit independiente que debe compartir la misma identidad visual (Sistema 2: crema + navy + oro). La super-demo ya tenía el sistema visual maduro en core/ui_theme.py, pero acoplado a su repo.

El stack (sección 6.3) advierte el Riesgo 3: si cada demo se construye en un repo distinto copiando el CSS, las UIs se desincronizan con el tiempo y un fix visual obliga a editar N repos.

## Decisión

Extraer el sistema visual a un repo propio, yidoca-ui, empaquetado como librería Python instalable (pyproject.toml + setuptools). Las demos lo consumen como dependencia, no como copia.

Tres sub-decisiones:

1. Librería instalable, no copia de archivos. En local se instala en modo editable (pip install -e ../yidoca-ui); en deploy se trae vía git+https en requirements.txt. Fuente única de verdad.

2. Tokens de diseño aislados. El bloque de variables CSS :root se extrae a una constante de módulo YIDOCA_TOKENS, separada de las funciones que la pintan. El resto sigue acoplado a Streamlit (st.markdown), que es el stack de todas las demos sandbox.

3. Repo público. Necesario para que Streamlit Community Cloud free pueda instalarlo vía git+https (no admite paquetes desde rutas locales en deploy).

## Alternativas consideradas

- Construir los componentes en la Demo B y copiarlos a las demás demos. Rechazada: reintroduce el Riesgo 3 (copias desincronizadas).
- Publicar en PyPI privado con versionado semántico y CI. Rechazada: sobre-ingeniería para un fundador en fase sandbox.
- Desacoplar el CSS por completo de Streamlit (render-agnóstico). Rechazada de momento: todas las demos sandbox usan Streamlit (ADR 002 super-demo); solo se aísla el bloque de tokens, por si una futura demo migra a Next.js.
- Mantener el repo privado y vendorizar (copiar la carpeta) en cada deploy. Rechazada: reintroduce las copias que la librería pretende eliminar.

## Consecuencias

- Positivas: una sola fuente de verdad para la identidad visual; un fix de componente beneficia a todas las demos al instante; ahorra 30-40% del tiempo en demos C-G (estimación stack 6.3); independencia entre demos preservada (solo importan, no dependen unas de otras).
- Negativas / coste: el sistema de diseño queda visible públicamente (asumido: es CSS, sin valor competitivo; los activos sensibles —prompts, metodología— viven en repos privados). Hay que mantener alineadas las versiones de Streamlit entre yidoca-ui y las demos para que los fixes V2 de CSS (dependientes de las clases emotion-cache de Streamlit) no se rompan.

## Notas

Commit raíz de yidoca-ui: 1ce5c6c. El refactor de tokens se validó por import + render visual real (no solo py_compile).
