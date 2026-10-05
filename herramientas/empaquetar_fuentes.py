"""
Descarga, subconjunta y empaqueta las tres fuentes de Yidoca como woff2.

SE EJECUTA A MANO Y SU SALIDA VA AL REPOSITORIO. No es parte de la librería en
tiempo de ejecución: produce `yidoca_ui/fuentes/*.woff2`, que es lo que
`aplicar_estilo_yidoca()` embebe en el CSS.

POR QUÉ EXISTEN ESTOS FICHEROS
-------------------------------
Hasta el bloque 9 la librería cargaba las tres familias desde
`fonts.googleapis.com`. Sin red —el pabellón de una feria, la wifi de invitados
de un cliente— el titular deja de ser Instrument Serif, el cuerpo deja de ser
Inter, y la demo cambia de aspecto delante de quien la está mirando.

Y hay un segundo motivo que pesa igual: una consultora que entra en la red de un
cliente y pide tres ficheros a un tercero está haciendo justo lo que no debe.
Ahora no sale ninguna petición fuera.

EL SUBCONJUNTO
--------------
Latín con los caracteres del español —tildes, eñe, apertura de interrogación y
exclamación— más los tipográficos que la demo usa de verdad: el menos U+2212, el
punto medio, la raya, las comillas angulares, el ≥ y el €. Sin subconjuntar, las
tres familias pesan más de un mega; con él, el CSS entero cabe en unos cientos de
kilobytes.

    python herramientas/empaquetar_fuentes.py
"""

from __future__ import annotations

import io
import sys
from pathlib import Path

import requests
from fontTools import subset
from fontTools.ttLib import TTFont

DESTINO = Path(__file__).resolve().parent.parent / "yidoca_ui" / "fuentes"

#: De dónde salen los ficheros. Son los repositorios oficiales de Google Fonts,
#: que sirven el TTF original junto a su licencia; no se descargan de la API de
#: CSS, que entrega woff2 ya subconjuntados por Google y sin control sobre qué
#: caracteres llevan.
RAIZ = "https://raw.githubusercontent.com/google/fonts/main"

FUENTES = [
    # (fichero destino, url, familia CSS, peso, estilo)
    ("inter-400.woff2", f"{RAIZ}/ofl/inter/Inter%5Bopsz,wght%5D.ttf",
     "Inter", 400, "normal"),
    ("inter-500.woff2", f"{RAIZ}/ofl/inter/Inter%5Bopsz,wght%5D.ttf",
     "Inter", 500, "normal"),
    ("inter-600.woff2", f"{RAIZ}/ofl/inter/Inter%5Bopsz,wght%5D.ttf",
     "Inter", 600, "normal"),
    ("instrument-serif-400.woff2",
     f"{RAIZ}/ofl/instrumentserif/InstrumentSerif-Regular.ttf",
     "Instrument Serif", 400, "normal"),
    ("instrument-serif-400-italic.woff2",
     f"{RAIZ}/ofl/instrumentserif/InstrumentSerif-Italic.ttf",
     "Instrument Serif", 400, "italic"),
    ("jetbrains-mono-400.woff2",
     f"{RAIZ}/ofl/jetbrainsmono/JetBrainsMono%5Bwght%5D.ttf",
     "JetBrains Mono", 400, "normal"),
    ("jetbrains-mono-500.woff2",
     f"{RAIZ}/ofl/jetbrainsmono/JetBrainsMono%5Bwght%5D.ttf",
     "JetBrains Mono", 500, "normal"),
]

#: Licencias a copiar junto a los woff2. Las tres familias son OFL 1.1 y la
#: licencia exige que el texto viaje con los ficheros.
LICENCIAS = [
    ("OFL-Inter.txt", f"{RAIZ}/ofl/inter/OFL.txt"),
    ("OFL-InstrumentSerif.txt", f"{RAIZ}/ofl/instrumentserif/OFL.txt"),
    ("OFL-JetBrainsMono.txt", f"{RAIZ}/ofl/jetbrainsmono/OFL.txt"),
]

#: ASCII imprimible, los acentos del español y los signos tipográficos que la
#: demo usa. Se declaran uno a uno en lugar de con rangos amplios: cada bloque
#: Unicode que se añade engorda el woff2, y lo que no se usa no viaja.
CARACTERES = (
    "".join(chr(c) for c in range(0x20, 0x7F))        # ASCII imprimible
    + "áéíóúÁÉÍÓÚàèìòùÀÈÌÒÙäëïöüÄËÏÖÜñÑçÇ¿¡ºª"         # español
    + "€·—–−±≥≤«»“”‘’…✓✗→←↑↓"                          # tipográficos de la demo
)


def _descargar(url: str) -> bytes:
    respuesta = requests.get(url, timeout=60)
    respuesta.raise_for_status()
    return respuesta.content


def _instancia(datos: bytes, peso: int) -> TTFont:
    """
    Una fuente lista para subconjuntar, fijando el peso si es variable.

    Inter y JetBrains Mono se publican como fuentes variables; embeberlas enteras
    traería todos los pesos del eje en cada fichero. `instancer` las congela en
    el peso concreto que la librería usa.
    """
    fuente = TTFont(io.BytesIO(datos))
    if "fvar" not in fuente:
        return fuente

    from fontTools.varLib import instancer
    fuente = instancer.instantiateVariableFont(
        fuente, {"wght": peso}, optimize=False, updateFontNames=False)

    # Se guarda y se vuelve a cargar antes de subconjuntar. Sin esta vuelta, el
    # subsetter revienta con `KeyError: 'space.tf'`: el instanciador deja en las
    # tablas de variación referencias a glifos intermedios que ya no existen, y
    # al recargar desde los bytes esas referencias no llegan a reconstruirse.
    memoria = io.BytesIO()
    fuente.save(memoria)
    memoria.seek(0)
    return TTFont(memoria)


def main() -> None:
    DESTINO.mkdir(parents=True, exist_ok=True)
    cache: dict[str, bytes] = {}

    print(f"Subconjunto: {len(CARACTERES)} caracteres")
    total = 0
    for nombre, url, familia, peso, estilo in FUENTES:
        if url not in cache:
            print(f"  descargando {url.rsplit('/', 1)[-1]} …")
            cache[url] = _descargar(url)

        fuente = _instancia(cache[url], peso)
        opciones = subset.Options()
        opciones.flavor = "woff2"
        opciones.desubroutinize = True
        # Sin layout features innecesarias: las ligaduras y los números
        # tabulares sí se conservan (la demo usa `font-variant-numeric`).
        opciones.layout_features = ["kern", "liga", "clig", "tnum", "onum",
                                    "calt", "ccmp", "locl", "mark", "mkmk"]
        subsetter = subset.Subsetter(options=opciones)
        subsetter.populate(text=CARACTERES)
        subsetter.subset(fuente)

        salida = DESTINO / nombre
        fuente.flavor = "woff2"
        fuente.save(salida)
        peso_kb = salida.stat().st_size / 1024
        total += peso_kb
        print(f"  {nombre:<36} {familia} {peso} {estilo:<7} {peso_kb:>7.1f} KB")

    for nombre, url in LICENCIAS:
        (DESTINO / nombre).write_bytes(_descargar(url))
        print(f"  {nombre:<36} licencia OFL")

    print(f"\nTotal woff2: {total:.1f} KB  "
          f"(en base64 dentro del CSS: ~{total * 4 / 3:.1f} KB)")


if __name__ == "__main__":
    sys.exit(main())
