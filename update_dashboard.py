#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
XOLOITZCUINTLES — JUGADORES PRESTADOS
Dashboard para Pyto (iPad)
Temporada 2026/2027 — Apertura 2026

El script:
1. Consulta las fichas de los 12 jugadores.
2. Extrae JJ, MJ, JT, G, AG, TA y TR de Apertura 2026.
3. Descarga la foto de cada jugador al iPad.
4. Genera un dashboard HTML con fondo del Estadio Caliente.
5. El HTML queda listo para abrirse en Safari.
SofaScore: estadísticas MP/MIN/GLS/AST capturadas manualmente.

Requisitos en Pyto:
    pip install requests beautifulsoup4
"""

import html
import re
from pathlib import Path
from urllib.parse import urljoin

import requests

from bs4 import BeautifulSoup
import time


# ============================================================
# CONFIGURACIÓN
# ============================================================

JUGADORES = [
    {
        "nombre": "Jesús Hernández Moreno",
        "url": "https://www.ligabbvaexpansion.mx/cancha/jugador/124277/jesus-hernandez-moreno",
    },
    {
        "nombre": "Ramón Eligio Palomares Verdugo",
        "url": "https://www.ligabbvaexpansion.mx/cancha/jugador/125435/ramon-eligio-palomares-verdugo",
    },
    {
        "nombre": "Eduardo Ochoa Chaparro",
        "url": "https://www.ligabbvaexpansion.mx/cancha/jugador/131793/eyJpZENsdWIiOiAxNDI2Nn0=/eduardo-ochoa-chaparro",
    },
    {
        "nombre": "Diego Emilio Sanchez Torres",
        "url": "https://www.ligabbvaexpansion.mx/cancha/jugador/138301/eyJpZENsdWIiOiAxNDI2Nn0=/diego-emilio-sanchez-torres",
    },
    {
        "nombre": "Daniel Guadalupe López Valdez",
        "url": "https://www.ligabbvaexpansion.mx/cancha/jugador/98510/eyJpZENsdWIiOiAxNDI2MH0=/daniel-guadalupe-lopez-valdez",
    },
    {
        "nombre": "Diego Emmanuel Martinez Rodriguez",
        "url": "https://www.ligabbvaexpansion.mx/cancha/jugador/150466/eyJpZENsdWIiOiAxMTc4MH0=/diego-emmanuel-martinez-rodriguez",
    },
    {
        "nombre": "Aldieri Josue Valenzuela Garcia",
        "url": "https://www.ligabbvaexpansion.mx/cancha/jugador/152775/eyJpZENsdWIiOiAxNDI5NX0=/aldieri-josue-valenzuela-garcia",
    },
    {
        "nombre": "Luis Ernesto Ruiz Bustillos",
        "url": "https://www.ligabbvaexpansion.mx/cancha/jugador/127040/eyJpZENsdWIiOiAxMjU4NH0=/luis-ernesto-ruiz-bustillos",
    },
    {
        "nombre": "Ángel Iván Ramírez Molina",
        "url": "https://www.ligabbvaexpansion.mx/cancha/jugador/162872",
    },
    {
        "nombre": "Daniel Vazquez Contreras",
        "url": "https://www.ligabbvaexpansion.mx/cancha/jugador/141261/daniel-vazquez-contreras",
    },
    {
        "nombre": "Juan Alejandro Martinez Valdez",
        "url": "https://www.ligabbvaexpansion.mx/cancha/jugador/131486/juan-alejandro-martinez-valdez",
    },
    {
        "nombre": "Diego Armando Araujo De La Luz",
        "url": "https://www.ligabbvaexpansion.mx/cancha/jugador/132477",
    },
]


# ============================================================
# SEGUNDO GRUPO — 8 JUGADORES PRESTADOS
#
# Los primeros 4 se consultan en Liga MX.
# Los últimos 4 se consultan en SofaScore.
# ============================================================

JUGADORES_SEGUNDO_GRUPO_LIGAMX = [
    {
        "nombre": "Diogo Osmar Bagui Tobar",
        "url": "https://www.ligamx.net/cancha/jugador/190940/eyJpZENsdWIiOiAxNDI1N30=/diogo-osmar-bagui-tobar",
        "fuente": "LIGA MX",
    },
    {
        "nombre": "Octavio Martín Vázquez González",
        "url": "https://www.ligamx.net/cancha/jugador/139137/eyJpZENsdWIiOiAxNDI1N30=/octavio-martin-vazquez-gonzalez",
        "fuente": "LIGA MX",
    },
    {
        "nombre": "Jhojan Esmaider Julio Palacios",
        "url": "https://www.ligamx.net/cancha/jugador/179375/eyJpZENsdWIiOiAxNDI1N30=/jhojan-esmaider-julio-palacios",
        "fuente": "LIGA MX",
    },
    {
        "nombre": "Ezequiel Eduardo Bullaude",
        "url": "https://www.ligamx.net/cancha/jugador/187398/eyJpZENsdWIiOiAxNDEwMn0=/ezequiel-eduardo-bullaude",
        "fuente": "LIGA MX",
    },
]

JUGADORES_SEGUNDO_GRUPO_SOFASCORE = [
    {
        "nombre": "Nicolás Díaz",
        "url": "https://www.sofascore.com/es/football/player/nicolas-diaz/924530#tab:career",
        "sofascore_id": "924530",
        "equipo": "Alianza Lima",
        "torneos": [
            {"id": 406, "nombre": "Liga 1 Te Apuesto"}
        ],
        "competencias": [
            "Liga 1 Te Apuesto"
        ],
        "fuente": "SOFASCORE",
    },
    {
        "nombre": "Vitinho",
        "url": "https://www.sofascore.com/es/football/player/vitinho/1066721#tab:career",
        "sofascore_id": "1066721",
        "equipo": "Fortaleza",
        "torneos": [
            {"id": 390, "nombre": "Brasileirão Série B"},
            {"id": 373, "nombre": "Copa Betano do Brasil"},
            {"id": 1596, "nombre": "Copa do Nordeste"},
            {"id": 378, "nombre": "Cearense"}
        ],
        "competencias": [
            "Brasileirão Série B",
            "Copa Betano do Brasil",
            "Copa do Nordeste",
            "Cearense"
        ],
        "fuente": "SOFASCORE",
    },
    {
        "nombre": "Domingo Blanco",
        "url": "https://www.sofascore.com/es/football/player/domingo-blanco/791140#tab:career",
        "sofascore_id": "791140",
        "equipo": "Defensa y Justicia",
        "torneos": [
            {"id": 155, "nombre": "Liga Profesional de Fútbol"},
            {"id": 1024, "nombre": "Copa Argentina"}
        ],
        "competencias": [
            "Liga Profesional de Fútbol",
            "Copa Argentina"
        ],
        "fuente": "SOFASCORE",
    },
    {
        "nombre": "Shamar Nicholson",
        "url": "https://www.sofascore.com/es/football/player/shamar-nicholson/884948#tab:career",
        "sofascore_id": "884948",
        "equipo": "ML Vitebsk",
        "torneos": [
            {"id": 169, "nombre": "Vysshaya Liga"}
        ],
        "competencias": [
            "Vysshaya Liga"
        ],
        "fuente": "SOFASCORE",
    },
]

SOFA_ESTADISTICAS = ["MP", "MIN", "GLS", "AST"]

ESTADISTICAS = ["JJ", "MJ", "JT", "G", "AG", "TA", "TR"]

# ============================================================
# LEAGUES CUP 2026 — ESTADÍSTICA HISTÓRICA FIJA
# ============================================================
#
# Estos datos corresponden exclusivamente a Leagues Cup.
# El torneo ya terminó para estos jugadores, por lo que estos
# valores NO se actualizan semanalmente.
#
# Se suman a las estadísticas acumuladas de la temporada.
#
# ============================================================

LEAGUES_CUP_MANUAL = {
    "Jhojan Esmaider Julio Palacios": {
        "JJ": 3,
        "MJ": 266,
        "JT": 3,
        "G": 1,
        "AG": 0,
        "TA": 0,
        "TR": 0,
    },

    "Octavio Martín Vázquez González": {
        "JJ": 1,
        "MJ": 12,
        "JT": 0,
        "G": 0,
        "AG": 0,
        "TA": 0,
        "TR": 0,
    },

    "Diogo Osmar Bagui Tobar": {
        "JJ": 3,
        "MJ": 195,
        "JT": 2,
        "G": 0,
        "AG": 0,
        "TA": 0,
        "TR": 0,
    },

    "Ezequiel Eduardo Bullaude": {
        "JJ": 3,
        "MJ": 170,
        "JT": 1,
        "G": 2,
        "AG": 0,
        "TA": 1,
        "TR": 0,
    },
}
# Fondo solicitado por el usuario.
BACKGROUND_URL = (
    "https://upload.wikimedia.org/wikipedia/commons/7/7f/"
    "Xolos_estadio_caliente.jpg"
)

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (iPad; CPU OS 17_0 like Mac OS X) "
        "AppleWebKit/605.1.15 (KHTML, like Gecko) "
        "Version/17.0 Mobile/15E148 Safari/604.1"
    )
}


# ============================================================
# FUNCIONES DE EXTRACCIÓN
# ============================================================

def limpiar_texto(texto):
    return re.sub(r"\s+", " ", texto).strip()


def extraer_numero(texto):
    texto = limpiar_texto(texto)
    match = re.search(r"-?\d+(?:[.,]\d+)?", texto)
    return match.group(0) if match else "0"


def encontrar_fila_temporada(soup):
    """
    Busca la temporada 2026-2027 sin limitar la división.

    Esto es importante porque algunos jugadores están en:
      - EXPANSIÓN MX / Apertura 2026
    mientras que otros aparecen en:
      - LIGA PREMIER / Liga 2026

    En ambos casos queremos la fila correspondiente a 2026-2027.
    """

    filas = soup.select("tr.informacion")

    # 1. Preferencia: Apertura 2026 de Expansión MX.
    for fila in filas:
        texto = limpiar_texto(fila.get_text(" ", strip=True))

        if (
            "2026-2027" in texto
            and "Apertura 2026" in texto
            and "EXPANSIÓN MX" in texto
        ):
            return fila

    # 2. Cualquier registro 2026-2027.
    #    Esto permite recuperar Liga Premier / Liga 2026.
    for fila in filas:
        texto = limpiar_texto(fila.get_text(" ", strip=True))

        if "2026-2027" in texto:
            return fila

    # 3. Fallback por si cambia la clase CSS.
    for fila in soup.select("tr"):
        texto = limpiar_texto(fila.get_text(" ", strip=True))

        if (
            "2026-2027" in texto
            and (
                "Apertura 2026" in texto
                or "Liga 2026" in texto
            )
        ):
            return fila

    return None


def extraer_estadisticas(fila):
    """
    Extrae:
    JJ — Juegos Jugados
    MJ — Minutos Jugados
    JT — Juegos como Titular
    G  — Goles
    AG — Asistencias
    TA — Tarjetas Amarillas
    TR — Tarjetas Rojas
    """

    resultado = {x: "0" for x in ESTADISTICAS}

    if fila is None:
        return resultado

    celdas = fila.find_all("td")

    valores = []

    # Las estadísticas de Liga Expansión aparecen en las columnas
    # col*_9 hasta col*_15.
    for celda in celdas:
        clase = " ".join(celda.get("class", []))

        if re.search(r"col\d+_(9|10|11|12|13|14|15)", clase):
            valores.append(
                extraer_numero(celda.get_text(" ", strip=True))
            )

    if len(valores) >= 7:
        for i, nombre in enumerate(ESTADISTICAS):
            resultado[nombre] = valores[i]

    return resultado


def obtener_id_jugador(url):
    """
    Obtiene el ID numérico de la ficha del jugador.
    Ejemplo:
    /cancha/jugador/127040/... -> 127040
    """
    match = re.search(r"/jugador/(\d+)", url)
    return match.group(1) if match else ""


def encontrar_foto(soup, url_base):
    """
    La web de Liga Expansión utiliza una ruta conocida para las
    fotografías de jugadores:

    https://cldrsrcs.apilmx.com/v1/media/wpagephotos/77/1/ID/ID.jpg

    En el HTML original de la página de Luis Ernesto Ruiz se observa
    exactamente este patrón. Si la primera imagen no está disponible,
    la web utiliza como respaldo el servidor dksx1d.ligamx.net.
    """

    jugador_id = obtener_id_jugador(url_base)

    if jugador_id:
        return (
            "https://cldrsrcs.apilmx.com/v1/media/wpagephotos/"
            f"77/1/{jugador_id}/{jugador_id}.jpg"
        )

    # Respaldo: intenta localizar la imagen en el HTML.
    for imagen in soup.select(".jugador img, .ficha img, img"):
        for atributo in ("src", "data-src", "data-original"):
            valor = imagen.get(atributo)

            if valor and (
                "wpagephotos" in valor
                or "AfldDrvd/photos" in valor
            ):
                return urljoin(url_base, valor)

    return ""


# ============================================================
# DESCARGA DE FOTOS
# ============================================================

def nombre_archivo_foto(indice, nombre):
    nombre_limpio = re.sub(r"[^a-zA-Z0-9]+", "_", nombre)
    nombre_limpio = nombre_limpio.strip("_").lower()
    return f"{indice:02d}_{nombre_limpio}.jpg"


def descargar_foto(url_foto, destino):
    """
    Descarga la fotografía localmente.

    Primero intenta el servidor principal de Liga Expansión.
    Si falla, intenta el servidor alternativo utilizado por la propia web.
    """

    if not url_foto:
        return False

    urls = [url_foto]

    # Crear URL alternativa automáticamente.
    match = re.search(r"/(\d+)/(\d+)\.jpg$", url_foto)

    if match:
        jugador_id = match.group(2)

        urls.append(
            "https://dksx1d.ligamx.net/sttcdcs/arcdgt/"
            f"AfldDrvd/photos/{jugador_id}/{jugador_id}.jpg"
        )

    for url in urls:

        try:
            respuesta = requests.get(
                url,
                headers=HEADERS,
                timeout=20
            )

            respuesta.raise_for_status()

            contenido = respuesta.content

            content_type = (
                respuesta.headers.get(
                    "content-type",
                    ""
                ).lower()
            )

            if (
                len(contenido) > 1000
                and (
                    content_type.startswith("image/")
                    or contenido[:3] == b"\xff\xd8\xff"
                    or contenido[:8] == b"\x89PNG\r\n\x1a\n"
                )
            ):
                destino.write_bytes(contenido)
                return True

        except Exception:
            continue

    return False


# ============================================================
# OBTENER DATOS DE CADA JUGADOR
# ============================================================

def obtener_jugador(jugador, indice, carpeta_fotos):
    print(f"[{indice}/{len(JUGADORES)}] {jugador['nombre']}")

    try:
        respuesta = requests.get(
            jugador["url"],
            headers=HEADERS,
            timeout=25
        )
        respuesta.raise_for_status()

        soup = BeautifulSoup(respuesta.text, "html.parser")

        fila = encontrar_fila_temporada(soup)

        estadisticas = extraer_estadisticas(fila)

        foto_url = encontrar_foto(
            soup,
            jugador["url"]
        )

        archivo_foto = carpeta_fotos / nombre_archivo_foto(
            indice,
            jugador["nombre"]
        )

        foto_local = descargar_foto(
            foto_url,
            archivo_foto
        )

        if fila:
            texto_fila = limpiar_texto(
                fila.get_text(" ", strip=True)
            )

            if "LIGA PREMIER" in texto_fila:
                competencia = "LIGA PREMIER"
            elif "EXPANSIÓN MX" in texto_fila:
                competencia = "EXPANSIÓN MX"
            else:
                competencia = "OTRA"

            print(
                f"    Temporada 2026-2027: OK "
                f"({competencia})"
            )
        else:
            print(
                "    Temporada 2026-2027: "
                "NO ENCONTRADA"
            )

        print(
            f"    Foto: "
            f"{'OK' if foto_local else 'NO DISPONIBLE'}"
        )

        return {
            "nombre": jugador["nombre"],
            "url": jugador["url"],
            "estadisticas": estadisticas,
            "foto": archivo_foto.name if foto_local else "",
            "foto_url": foto_url,
        }

    except Exception as error:
        print(f"    ERROR: {error}")

        return {
            "nombre": jugador["nombre"],
            "url": jugador["url"],
            "estadisticas": {x: "0" for x in ESTADISTICAS},
            "foto": "",
            "foto_url": "",
        }


# ============================================================
# HTML
# ============================================================

def crear_tarjeta(jugador):
    nombre = html.escape(jugador["nombre"])
    url = html.escape(jugador["url"])

    if jugador.get("foto"):
        foto = html.escape("xolos_fotos/" + jugador["foto"])

        imagen = (
            f'<img class="foto" src="{foto}" '
            f'alt="{nombre}" loading="lazy">'
        )

    elif jugador.get("foto_url"):
        foto = html.escape(jugador["foto_url"])

        # Si Safari puede cargar la imagen directamente, se muestra.
        # Si no, se cambia al servidor alternativo.
        jugador_id = obtener_id_jugador(jugador["url"])

        fallback = html.escape(
            "https://dksx1d.ligamx.net/sttcdcs/arcdgt/"
            f"AfldDrvd/photos/{jugador_id}/{jugador_id}.jpg"
        )

        imagen = (
            f"""<img class=\"foto\" src=\"{foto}\"
                alt=\"{nombre}\" loading=\"lazy\"
                onerror=\"this.onerror=null;this.src='{fallback}';\">"""
        )

    else:
        imagen = '<div class="foto sin-foto">⚽</div>'

    estadisticas_html = ""

    for estadistica in ESTADISTICAS:
        valor = html.escape(
            str(
                jugador["estadisticas"].get(
                    estadistica,
                    "0"
                )
            )
        )

        estadisticas_html += f"""
            <div class="stat">
                <div class="stat-label">{estadistica}</div>
                <div class="stat-value">{valor}</div>
            </div>
        """

    return f"""
    <article class="card">

        <div class="player-top">

            {imagen}

            <div class="player-name">
                {nombre}
            </div>

            <a class="open-link"
               href="{url}"
               target="_blank"
               title="Abrir ficha">
                ↗
            </a>

        </div>

        <div class="stats">
            {estadisticas_html}
        </div>

    </article>
    """


def crear_html(jugadores):
    tarjetas = "\n".join(
        crear_tarjeta(jugador)
        for jugador in jugadores
    )

    return f"""<!DOCTYPE html>

<html lang="es">

<head>

<meta charset="UTF-8">

<meta name="viewport"
      content="width=device-width,
               initial-scale=1.0,
               maximum-scale=1.0,
               user-scalable=no">

<title>Xoloitzcuintles — Jugadores Prestados</title>


<style>

/* ==========================================================
   BASE
   ========================================================== */

* {{
    box-sizing: border-box;
}}

html {{
    min-height: 100%;
}}

body {{

    margin: 0;

    min-height: 100vh;

    color: #ffffff;

    font-family:
        -apple-system,
        BlinkMacSystemFont,
        "SF Pro Display",
        "Helvetica Neue",
        Arial,
        sans-serif;

    background-color: #080808;

    background-image:
        linear-gradient(
            rgba(0, 0, 0, 0.75),
            rgba(0, 0, 0, 0.75)
        ),
        url("{BACKGROUND_URL}");

    background-size: cover;

    background-position: center;

    background-attachment: fixed;

}}


/* ==========================================================
   CONTENEDOR
   ========================================================== */

.page {{

    width: 100%;

    max-width: 1450px;

    margin: 0 auto;

    padding:
        34px
        28px
        32px;

}}


/* ==========================================================
   HEADER
   ========================================================== */

.header {{

    text-align: center;

    margin-bottom: 28px;

}}

.kicker {{

    color: #e30613;

    font-size: 22px;

    font-weight: 900;

    letter-spacing: 1px;

    margin-bottom: 2px;

}}

.title {{

    margin: 0;

    font-size: clamp(34px, 5vw, 58px);

    line-height: .95;

    font-weight: 900;

    letter-spacing: -1.5px;

    text-transform: uppercase;

}}

.season {{

    display: inline-block;

    margin-top: 13px;

    padding-top: 9px;

    border-top: 2px solid #e30613;

    font-size: 16px;

    font-weight: 800;

    letter-spacing: .5px;

    text-transform: uppercase;

}}

.season strong {{

    color: #e30613;

}}


/* ==========================================================
   GRID
   ========================================================== */

.grid {{

    display: grid;

    grid-template-columns:
        repeat(4, minmax(0, 1fr));

    gap: 13px;

}}


/* ==========================================================
   TARJETAS
   ========================================================== */

.card {{

    background:
        linear-gradient(
            135deg,
            rgba(28, 28, 28, .91),
            rgba(8, 8, 8, .88)
        );

    border:
        1px solid
        rgba(255, 255, 255, .20);

    border-radius: 11px;

    overflow: hidden;

    box-shadow:
        0 8px 25px
        rgba(0, 0, 0, .38);

    backdrop-filter: blur(4px);

}}

.player-top {{

    min-height: 122px;

    display: flex;

    align-items: center;

    gap: 13px;

    padding: 15px 14px;

    position: relative;

}}

.foto {{

    width: 82px;

    height: 82px;

    flex: 0 0 82px;

    border-radius: 50%;

    object-fit: cover;

    object-position: center top;

    background: #eeeeee;

    border: 3px solid #ffffff;

}}

.sin-foto {{

    display: flex;

    align-items: center;

    justify-content: center;

    color: #e30613;

    font-size: 28px;

}}

.player-name {{

    font-size: 18px;

    line-height: 1.12;

    font-weight: 850;

    padding-right: 24px;

}}

.open-link {{

    position: absolute;

    top: 16px;

    right: 15px;

    color: #e30613;

    text-decoration: none;

    font-size: 26px;

    line-height: 1;

    font-weight: 500;

}}


/* ==========================================================
   ESTADÍSTICAS
   ========================================================== */

.stats {{

    display: grid;

    grid-template-columns:
        repeat(7, 1fr);

    border-top:
        1px solid
        rgba(255, 255, 255, .18);

    padding:
        10px 9px 13px;

}}

.stat {{

    text-align: center;

}}

.stat-label {{

    color: #e30613;

    font-size: 12px;

    font-weight: 850;

    letter-spacing: .5px;

}}

.stat-value {{

    margin-top: 5px;

    color: #ffffff;

    font-size: 18px;

    line-height: 1;

    font-weight: 850;

}}


/* ==========================================================
   PIE
   ========================================================== */

.footer {{

    margin-top: 26px;

    text-align: center;

    color: rgba(255,255,255,.72);

    font-size: 12px;

    line-height: 1.6;

}}

.footer strong {{

    color: #ffffff;

}}


/* ==========================================================
   iPAD VERTICAL
   ========================================================== */

@media (max-width: 900px) {{

    .page {{

        padding: 24px 16px 28px;

    }}

    .grid {{

        grid-template-columns:
            repeat(2, minmax(0, 1fr));

        gap: 12px;

    }}

    .player-name {{

        font-size: 16px;

    }}

}}


/* ==========================================================
   iPHONE / PANTALLA PEQUEÑA
   ========================================================== */

@media (max-width: 560px) {{

    .grid {{

        grid-template-columns: 1fr;

    }}

    .title {{

        font-size: 35px;

    }}

}}

</style>

</head>


<body>

<div class="page">


<header class="header">

    <div class="kicker">
        XOLOITZCUINTLES
    </div>

    <h1 class="title">
        Jugadores Prestados
    </h1>

    <div class="season">
        Temporada
        <strong>2026/2027</strong>
        — Apertura 2026
    </div>

</header>


<main class="grid">

    {tarjetas}

</main>


<footer class="footer">

    <div>
        <strong>JJ</strong> Juegos Jugados
        ·
        <strong>MJ</strong> Minutos Jugados
        ·
        <strong>JT</strong> Juegos como Titular
        ·
        <strong>G</strong> Goles
        ·
        <strong>AG</strong> Asistencias
        ·
        <strong>TA</strong> Tarjetas Amarillas
        ·
        <strong>TR</strong> Tarjetas Rojas
    </div>

    <div>
        Datos obtenidos de Liga BBVA Expansión MX
    </div>

</footer>


</div>

</body>

</html>
"""


# ============================================================
# SOFASCORE
# ============================================================

_SOFASCORE_SESSION = None



def sofascore_get(url, timeout=30):
    """
    Consulta SofaScore evitando el bloqueo 403 habitual de clientes
    Python estándar.

    Punto clave:
    SofaScore está detrás de protección anti-bot/TLS. Un User-Agent
    por sí solo no es suficiente en algunas redes. Se añade
    X-Requested-With y, si está disponible, curl_cffi impersonando
    Safari iOS/Chrome.

    Las rutas oficiales utilizadas siguen siendo:
      /api/v1/player/{id}/events/last/{page}
      /api/v1/event/{eventId}/lineups
    """

    session, transporte = obtener_sesion_sofascore()

    # Aseguramos que todas las rutas usen el dominio API.
    if url.startswith(
        "https://api.sofascore.com"
    ):
        endpoint = url

    elif url.startswith(
        "https://api.sofascore.app"
    ):
        endpoint = url.replace(
            "https://api.sofascore.app",
            "https://api.sofascore.com",
            1
        )

    elif url.startswith(
        "https://www.sofascore.com"
    ):
        endpoint = url.replace(
            "https://www.sofascore.com",
            "https://api.sofascore.com",
            1
        )

    else:
        endpoint = url

    errores = []

    # Primera petición: el endpoint solicitado.
    try:
        respuesta = session.get(
            endpoint,
            timeout=timeout
        )

        if respuesta.status_code == 200:
            return respuesta.json()

        errores.append(
            f"{transporte}: HTTP "
            f"{respuesta.status_code}"
        )

    except Exception as error:
        errores.append(
            f"{transporte}: {error}"
        )

    # Si requests dio 403 y curl_cffi no estaba instalado,
    # hacemos una última prueba con headers reforzados.
    if (
        respuesta.status_code == 403
        if "respuesta" in locals()
        else True
    ) and curl_requests is None:

        try:
            headers_reforzados = {
                "User-Agent": (
                    "Mozilla/5.0 (iPhone; CPU iPhone OS 18_6 "
                    "like Mac OS X) AppleWebKit/605.1.15 "
                    "(KHTML, like Gecko) Version/18.0 "
                    "Mobile/15E148 Safari/604.1"
                ),
                "Accept": "application/json, text/plain, */*",
                "Accept-Language": "es-MX,es;q=0.9",
                "Referer": (
                    "https://www.sofascore.com/"
                ),
                "Origin": (
                    "https://www.sofascore.com"
                ),
                "X-Requested-With": (
                    "XMLHttpRequest"
                ),
            }

            respuesta2 = requests.get(
                endpoint,
                headers=headers_reforzados,
                timeout=timeout
            )

            if respuesta2.status_code == 200:
                return respuesta2.json()

            errores.append(
                "requests reforzado: HTTP "
                f"{respuesta2.status_code}"
            )

        except Exception as error:
            errores.append(
                f"requests reforzado: {error}"
            )

    raise RuntimeError(
        "SofaScore devolvió 403. "
        "El servidor está rechazando el cliente Python. "
        + " | ".join(errores)
        + (
            " | Instala curl_cffi en Pyto para usar "
            "impersonación TLS de Safari/Chrome."
            if curl_requests is None
            else ""
        )
    )


def es_temporada_2026(season):
    """Identifica la temporada que corresponde al año 2026."""

    if not isinstance(season, dict):
        return False

    nombre = str(season.get("name", ""))
    year = str(season.get("year", ""))

    return (
        "2026" in nombre
        or year.startswith("26/")
        or year == "2026"
    )


def numero(valor):
    try:
        return int(float(valor or 0))
    except Exception:
        return 0


def normalizar_comparacion(texto):
    """
    Normaliza nombres para comparar competiciones/equipos aunque
    SofaScore utilice pequeñas variaciones de escritura.
    """
    import unicodedata

    texto = str(texto or "").strip().lower()

    texto = unicodedata.normalize(
        "NFKD",
        texto
    ).encode(
        "ascii",
        "ignore"
    ).decode(
        "ascii"
    )

    texto = re.sub(
        r"[^a-z0-9]+",
        " ",
        texto
    )

    return " ".join(texto.split())


def nombre_competencia_coincide(nombre_real, nombres_permitidos):
    """
    Compara el nombre que devuelve SofaScore contra la lista
    específica solicitada para cada jugador.
    """

    real = normalizar_comparacion(
        nombre_real
    )

    for permitido in nombres_permitidos:

        objetivo = normalizar_comparacion(
            permitido
        )

        if (
            real == objetivo
            or objetivo in real
            or real in objetivo
        ):
            return True

    return False


def equipo_coincide(nombre_real, equipo_objetivo):
    """
    Comprueba el club cuando SofaScore lo incluye en la respuesta.
    Si el endpoint no devuelve team en ese bloque concreto,
    no descartamos automáticamente el registro: la competición
    sigue siendo el filtro principal.
    """

    if not equipo_objetivo:
        return True

    if not nombre_real:
        return True

    real = normalizar_comparacion(
        nombre_real
    )

    objetivo = normalizar_comparacion(
        equipo_objetivo
    )

    return (
        real == objetivo
        or objetivo in real
        or real in objetivo
    )


def timestamp_a_fecha(timestamp):
    """Convierte timestamp Unix a fecha local del dispositivo."""
    from datetime import datetime

    try:
        return datetime.fromtimestamp(
            int(timestamp)
        ).date()
    except Exception:
        return None


def obtener_eventos_jugador_2026(player_id):
    """
    Obtiene los partidos recientes asociados al jugador mediante
    /player/{id}/events/last/{page}.

    Se pagina hasta que los eventos ya sean anteriores a 2026.
    Así no necesitamos conocer el seasonId de cada competición.
    """

    eventos = []

    for pagina in range(0, 5):

        url = (
            "https://api.sofascore.com/api/v1/player/"
            f"{player_id}/events/last/{pagina}"
        )

        try:
            data = sofascore_get(
                url,
                timeout=30
            )

        except Exception as error:
            print(
                f"      Error obteniendo partidos "
                f"página {pagina}: {error}"
            )
            break

        lote = data.get(
            "events",
            []
        )

        if not isinstance(
            lote,
            list
        ) or not lote:
            break

        eventos.extend(
            lote
        )

        # Los eventos vienen de más reciente a más antiguo.
        fechas = [
            timestamp_a_fecha(
                evento.get(
                    "startTimestamp"
                )
            )
            for evento in lote
        ]

        fechas_validas = [
            fecha
            for fecha in fechas
            if fecha is not None
        ]

        if fechas_validas:

            fecha_mas_antigua = min(
                fechas_validas
            )

            if fecha_mas_antigua.year < 2026:
                break

        if not data.get(
            "hasNextPage",
            False
        ):
            break

    return eventos


def evento_es_objetivo(
    evento,
    jugador
):
    """
    Comprueba simultáneamente:

      1. que el partido sea de 2026;
      2. que la competición esté permitida;
      3. que el club del préstamo sea uno de los dos equipos.
    """

    fecha = timestamp_a_fecha(
        evento.get(
            "startTimestamp"
        )
    )

    if not fecha or fecha.year != 2026:
        return False

    tournament = evento.get(
        "tournament",
        {}
    )

    unique_tournament = (
        tournament.get(
            "uniqueTournament",
            {}
        )
        if isinstance(
            tournament,
            dict
        )
        else {}
    )

    nombre_competencia = str(
        unique_tournament.get(
            "name",
            tournament.get(
                "name",
                ""
            )
        )
    )

    competencias = jugador.get(
        "competencias",
        []
    )

    if not nombre_competencia_coincide(
        nombre_competencia,
        competencias
    ):
        return False

    equipo_objetivo = jugador.get(
        "equipo",
        ""
    )

    home = evento.get(
        "homeTeam",
        {}
    )

    away = evento.get(
        "awayTeam",
        {}
    )

    nombres_equipos = [
        home.get(
            "name",
            ""
        )
        if isinstance(
            home,
            dict
        )
        else "",
        away.get(
            "name",
            ""
        )
        if isinstance(
            away,
            dict
        )
        else "",
    ]

    return any(
        equipo_coincide(
            nombre,
            equipo_objetivo
        )
        for nombre in nombres_equipos
        if nombre
    )


def extraer_estadistica_jugador_de_lineup(
    lineups,
    player_id
):
    """
    Encuentra al jugador dentro de home/away.

    SofaScore puede devolver jugadores bajo:
      - players
      - startingLineup
      - substitutes

    La función acepta las tres variantes.
    """

    player_id = int(
        player_id
    )

    equipos = []

    if isinstance(
        lineups,
        dict
    ):
        equipos = [
            lineups.get(
                "home",
                {}
            ),
            lineups.get(
                "away",
                {}
            ),
        ]

    for equipo in equipos:

        if not isinstance(
            equipo,
            dict
        ):
            continue

        candidatos = []

        for clave in (
            "players",
            "startingLineup",
            "substitutes",
        ):

            valor = equipo.get(
                clave,
                []
            )

            if isinstance(
                valor,
                list
            ):
                candidatos.extend(
                    valor
                )

        for registro in candidatos:

            if not isinstance(
                registro,
                dict
            ):
                continue

            player = registro.get(
                "player",
                {}
            )

            if not isinstance(
                player,
                dict
            ):
                continue

            try:
                current_id = int(
                    player.get(
                        "id"
                    )
                )
            except Exception:
                continue

            if current_id != player_id:
                continue

            statistics = registro.get(
                "statistics",
                {}
            )

            if not isinstance(
                statistics,
                dict
            ):
                statistics = {}

            return statistics

    return None


# ============================================================
# SOFASCORE — CAPTURA MANUAL
# ============================================================
#
# Se mantiene el dashboard exactamente igual, pero los cuatro
# jugadores de SofaScore se capturan manualmente.
#
# MÉTRICAS:
#   MP  = Partidos
#   MIN = Minutos
#   GLS = Goles
#   AST = Asistencias
#
# Cuando quieras actualizar un jugador, modifica solamente los
# cuatro números de su bloque.
#
# Ejemplo:
#   "Nicolas Diaz": {"MP": 5, "MIN": 312, "GLS": 1, "AST": 0}
#
# ============================================================

SOFASCORE_MANUAL = {
    "Nicolas Diaz": {
        "MP": 4,
        "MIN": 261,
        "GLS": 0,
        "AST": 0,
    },

    "Vitinho": {
        "MP": 35,
        "MIN": 1850,
        "GLS": 10,
        "AST": 1,
    },

    "Domingo Blanco": {
        "MP": 7,
        "MIN": 218,
        "GLS": 0,
        "AST": 0,
    },

    "Shamar Nicholson": {
        "MP": 13,
        "MIN": 451,
        "GLS": 0,
        "AST": 1,
    },
    }


def clave_sofascore_manual(nombre):
    """
    Normaliza los nombres para que pequeñas diferencias de
    mayúsculas/acentos no impidan encontrar los datos manuales.
    """
    import unicodedata

    texto = str(nombre).strip().lower()

    texto = unicodedata.normalize(
        "NFD",
        texto
    )

    texto = "".join(
        caracter
        for caracter in texto
        if unicodedata.category(caracter) != "Mn"
    )

    return texto


def obtener_estadisticas_sofascore_manual(jugador):
    """
    Devuelve las estadísticas introducidas manualmente.

    No realiza ninguna conexión con SofaScore.
    """

    nombre = jugador.get(
        "nombre",
        ""
    )

    objetivo = clave_sofascore_manual(
        nombre
    )

    for nombre_manual, estadisticas in SOFASCORE_MANUAL.items():

        if clave_sofascore_manual(
            nombre_manual
        ) == objetivo:

            resultado = {
                "MP": int(
                    estadisticas.get(
                        "MP",
                        0
                    )
                ),
                "MIN": int(
                    estadisticas.get(
                        "MIN",
                        0
                    )
                ),
                "GLS": int(
                    estadisticas.get(
                        "GLS",
                        0
                    )
                ),
                "AST": int(
                    estadisticas.get(
                        "AST",
                        0
                    )
                ),
            }

            print(
                "    Estadísticas capturadas manualmente: "
                f"MP {resultado['MP']} · "
                f"MIN {resultado['MIN']} · "
                f"GLS {resultado['GLS']} · "
                f"AST {resultado['AST']}"
            )

            return resultado

    print(
        "    ⚠️ Jugador no encontrado en "
        "SOFASCORE_MANUAL."
    )

    return {
        "MP": 0,
        "MIN": 0,
        "GLS": 0,
        "AST": 0,
    }


def extraer_estadisticas_sofascore_api(jugador):
    objetivo = clave_sofascore_manual(jugador.get("nombre", ""))
    for nombre, valores in SOFASCORE_MANUAL.items():
        if clave_sofascore_manual(nombre) == objetivo:
            return {k: int(valores.get(k, 0)) for k in SOFA_ESTADISTICAS}
    return {k: 0 for k in SOFA_ESTADISTICAS}

def obtener_jugador_sofascore(jugador, indice, carpeta_fotos):
    print(
        f"[Sofascore {indice}/"
        f"{len(JUGADORES_SEGUNDO_GRUPO_SOFASCORE)}] "
        f"{jugador['nombre']}"
    )

    estadisticas = {
        x: 0
        for x in SOFA_ESTADISTICAS
    }

    foto_url = (
        "https://img.sofascore.com/api/v1/player/"
        f"{jugador['sofascore_id']}/image"
    )

    archivo_foto = carpeta_fotos / nombre_archivo_foto(
        20 + indice,
        jugador["nombre"]
    )

    foto_local = descargar_foto(
        foto_url,
        archivo_foto
    )

    try:
        # YA NO dependemos del HTML de la página para las estadísticas.
        # La página visible es dinámica; la API contiene los valores reales.
        estadisticas = extraer_estadisticas_sofascore_api(
            jugador
        )

        print(
            "    TOTAL SELECCIONADO: ",
            estadisticas
        )

    except Exception as error:
        print(
            f"    ERROR SofaScore: {error}"
        )

    print(
        "    Foto:",
        "OK" if foto_local else "NO DISPONIBLE"
    )

    return {
        "nombre": jugador["nombre"],
        "url": jugador["url"],
        "fuente": "SOFASCORE",
        "competencia": (
            " · ".join(
                jugador.get(
                    "competencias",
                    []
                )
            )
        ),
        "estadisticas": estadisticas,
        "foto": (
            archivo_foto.name
            if foto_local
            else ""
        ),
        "foto_url": foto_url,
        "tipo": "sofascore",
    }


def crear_tarjeta_segundo_grupo(jugador):
    nombre = html.escape(
        jugador["nombre"]
    )

    url = html.escape(
        jugador["url"]
    )

    if jugador.get("foto"):
        foto = html.escape(
            "xolos_fotos/" + jugador["foto"]
        )

        imagen = (
            f'<img class="foto" src="{foto}" '
            f'alt="{nombre}" loading="lazy">'
        )

    elif jugador.get("foto_url"):
        foto = html.escape(
            jugador["foto_url"]
        )

        imagen = (
            f'<img class="foto" src="{foto}" '
            f'alt="{nombre}" loading="lazy">'
        )

    else:
        imagen = (
            '<div class="foto sin-foto">⚽</div>'
        )

    if jugador.get("tipo") == "sofascore":
        labels = SOFA_ESTADISTICAS
        fuente = "SOFASCORE"
        subtexto = html.escape(
            jugador.get("competencia", "")
        )
    else:
        labels = ESTADISTICAS
        fuente = "LIGA MX"
        subtexto = "Apertura 2026 · 2026/2027"

    estadisticas_html = ""

    for estadistica in labels:
        valor = html.escape(
            str(
                jugador["estadisticas"].get(
                    estadistica,
                    0
                )
            )
        )

        estadisticas_html += f"""
            <div class="stat">
                <div class="stat-label">
                    {estadistica}
                </div>
                <div class="stat-value">
                    {valor}
                </div>
            </div>
        """

    return f"""
    <article class="card">

        <div class="player-top">

            {imagen}

            <div>
                <div class="source-badge">
                    {fuente}
                </div>

                <div class="player-name">
                    {nombre}
                </div>

                <div class="competition">
                    {subtexto}
                </div>
            </div>

            <a class="open-link"
               href="{url}"
               target="_blank"
               title="Abrir ficha">
                ↗
            </a>

        </div>

        <div class="stats stats-secondary">
            {estadisticas_html}
        </div>

    </article>
    """




def crear_dashboard_con_pestanas(
    tarjetas_primer_grupo,
    tarjetas_segundo_grupo
):
    return f"""<!DOCTYPE html>

<html lang="es">

<head>

<meta charset="UTF-8">

<meta name="viewport"
      content="width=device-width,
               initial-scale=1.0,
               maximum-scale=1.0,
               user-scalable=no">

<title>Xoloitzcuintles — Jugadores Prestados</title>

<style>

* {{
    box-sizing: border-box;
}}

html {{
    min-height: 100%;
}}

body {{

    margin: 0;

    min-height: 100vh;

    color: #ffffff;

    font-family:
        -apple-system,
        BlinkMacSystemFont,
        "SF Pro Display",
        "Helvetica Neue",
        Arial,
        sans-serif;

    background-color: #080808;

    background-image:
        linear-gradient(
            rgba(0, 0, 0, 0.75),
            rgba(0, 0, 0, 0.75)
        ),
        url("{BACKGROUND_URL}");

    background-size: cover;

    background-position: center;

    background-attachment: fixed;

}}

.page {{
    width: 100%;
    max-width: 1450px;
    margin: 0 auto;
    padding: 34px 28px 32px;
}}

.header {{
    text-align: center;
    margin-bottom: 22px;
}}

.kicker {{
    color: #e30613;
    font-size: 22px;
    font-weight: 900;
    letter-spacing: 1px;
    margin-bottom: 2px;
}}

.title {{
    margin: 0;
    font-size: clamp(34px, 5vw, 58px);
    line-height: .95;
    font-weight: 900;
    letter-spacing: -1.5px;
    text-transform: uppercase;
}}

.season {{
    display: inline-block;
    margin-top: 13px;
    padding-top: 9px;
    border-top: 2px solid #e30613;
    font-size: 16px;
    font-weight: 800;
    letter-spacing: .5px;
    text-transform: uppercase;
}}

.season strong {{
    color: #e30613;
}}

/* PESTAÑAS */

.tabs {{
    display: flex;
    justify-content: center;
    gap: 8px;
    margin: 0 auto 22px;
}}

.tab {{
    appearance: none;
    border: 1px solid rgba(255,255,255,.22);
    background: rgba(0,0,0,.55);
    color: rgba(255,255,255,.72);
    border-radius: 8px;
    padding: 11px 24px;
    font-size: 14px;
    font-weight: 850;
    letter-spacing: .4px;
    cursor: pointer;
}}

.tab.active {{
    color: #ffffff;
    background: #e30613;
    border-color: #e30613;
}}

.panel {{
    display: none;
}}

.panel.active {{
    display: block;
}}

.section-label {{
    text-align: center;
    color: rgba(255,255,255,.78);
    font-size: 12px;
    font-weight: 750;
    letter-spacing: .7px;
    text-transform: uppercase;
    margin: -6px 0 14px;
}}

.grid {{
    display: grid;
    grid-template-columns:
        repeat(4, minmax(0, 1fr));
    gap: 13px;
}}

.card {{
    background:
        linear-gradient(
            135deg,
            rgba(28, 28, 28, .91),
            rgba(8, 8, 8, .88)
        );

    border:
        1px solid
        rgba(255, 255, 255, .20);

    border-radius: 11px;

    overflow: hidden;

    box-shadow:
        0 8px 25px
        rgba(0, 0, 0, .38);

    backdrop-filter: blur(4px);
}}

.player-top {{
    min-height: 122px;
    display: flex;
    align-items: center;
    gap: 13px;
    padding: 15px 14px;
    position: relative;
}}

.foto {{
    width: 82px;
    height: 82px;
    flex: 0 0 82px;
    border-radius: 50%;
    object-fit: cover;
    object-position: center top;
    background: #eeeeee;
    border: 3px solid #ffffff;
}}

.sin-foto {{
    display: flex;
    align-items: center;
    justify-content: center;
    color: #e30613;
    font-size: 28px;
}}

.source-badge {{
    display: inline-block;
    color: #e30613;
    font-size: 10px;
    font-weight: 900;
    letter-spacing: .7px;
    margin-bottom: 4px;
}}

.player-name {{
    font-size: 18px;
    line-height: 1.12;
    font-weight: 850;
    padding-right: 24px;
}}

.competition {{
    color: rgba(255,255,255,.58);
    font-size: 10px;
    line-height: 1.25;
    margin-top: 5px;
    padding-right: 24px;
}}

.open-link {{
    position: absolute;
    top: 16px;
    right: 15px;
    color: #e30613;
    text-decoration: none;
    font-size: 26px;
    line-height: 1;
    font-weight: 500;
}}

.stats {{
    display: grid;
    grid-template-columns:
        repeat(7, 1fr);
    border-top:
        1px solid
        rgba(255, 255, 255, .18);
    padding: 10px 9px 13px;
}}

.stats-secondary {{
    grid-template-columns:
        repeat(4, 1fr);
}}

.stat {{
    text-align: center;
}}

.stat-label {{
    color: #e30613;
    font-size: 12px;
    font-weight: 850;
    letter-spacing: .5px;
}}

.stat-value {{
    margin-top: 5px;
    color: #ffffff;
    font-size: 18px;
    line-height: 1;
    font-weight: 850;
}}

.footer {{
    margin-top: 26px;
    text-align: center;
    color: rgba(255,255,255,.72);
    font-size: 12px;
    line-height: 1.6;
}}

.footer strong {{
    color: #ffffff;
}}

@media (max-width: 900px) {{

    .page {{
        padding: 24px 16px 28px;
    }}

    .grid {{
        grid-template-columns:
            repeat(2, minmax(0, 1fr));
        gap: 12px;
    }}

    .player-name {{
        font-size: 16px;
    }}

}}

@media (max-width: 560px) {{

    .grid {{
        grid-template-columns: 1fr;
    }}

    .title {{
        font-size: 35px;
    }}

    .tabs {{
        flex-direction: column;
    }}

}}

</style>

</head>

<body>

<div class="page">

<header class="header">

    <div class="kicker">
        XOLOITZCUINTLES
    </div>

    <h1 class="title">
        Jugadores Prestados
    </h1>

    <div class="season">
        Temporada
        <strong>2026/2027</strong>
    </div>

</header>


<nav class="tabs">

    <button
        class="tab active"
        onclick="mostrarPestana('expansion', this)">
        EXPANSIÓN / PREMIER
    </button>

    <button
        class="tab"
        onclick="mostrarPestana('otros', this)">
        OTROS PRÉSTAMOS
    </button>

</nav>


<section
    id="expansion"
    class="panel active">

    <div class="section-label">
        Apertura 2026 · Liga Expansión MX / Liga Premier
    </div>

    <main class="grid">
        {tarjetas_primer_grupo}
    </main>

</section>


<section
    id="otros"
    class="panel">

    <div class="section-label">
        Liga MX · Sofascore
    </div>

    <main class="grid">
        {tarjetas_segundo_grupo}
    </main>

</section>


<footer class="footer">

    <div>
        <strong>JJ</strong> Juegos Jugados
        ·
        <strong>MJ</strong> Minutos Jugados
        ·
        <strong>JT</strong> Juegos como Titular
        ·
        <strong>G</strong> Goles
        ·
        <strong>AG</strong> Asistencias
        ·
        <strong>TA</strong> Tarjetas Amarillas
        ·
        <strong>TR</strong> Tarjetas Rojas
    </div>

    <div>
        En Sofascore:
        <strong>MP</strong> Partidos
        ·
        <strong>MIN</strong> Minutos
        ·
        <strong>GLS</strong> Goles
        ·
        <strong>AST</strong> Asistencias
    </div>

    <div>
        Datos obtenidos de Liga MX / Liga BBVA Expansión MX / Sofascore
    </div>

</footer>

</div>


<script>

function mostrarPestana(id, boton) {{

    document
        .querySelectorAll(".panel")
        .forEach(function(panel) {{
            panel.classList.remove("active");
        }});

    document
        .querySelectorAll(".tab")
        .forEach(function(tab) {{
            tab.classList.remove("active");
        }});

    document
        .getElementById(id)
        .classList.add("active");

    boton.classList.add("active");
}}

</script>

</body>

</html>
"""



# ============================================================
# MAIN
# ============================================================

def main():

    carpeta_base = Path(__file__).resolve().parent

    carpeta_fotos = (
        carpeta_base /
        "xolos_fotos"
    )

    carpeta_fotos.mkdir(
        parents=True,
        exist_ok=True
    )

    print()
    print("=" * 60)
    print(" XOLOITZCUINTLES — DASHBOARD")
    print(" Temporada 2026/2027")
    print("=" * 60)
    print()

    # --------------------------------------------------------
    # PRIMER GRUPO
    # --------------------------------------------------------

    resultados = []

    print("PRIMER GRUPO — EXPANSIÓN / LIGA PREMIER")
    print("-" * 60)

    for indice, jugador in enumerate(
        JUGADORES,
        start=1
    ):

        resultado = obtener_jugador(
            jugador,
            indice,
            carpeta_fotos
        )

        resultado["fuente"] = "LIGA MX"
        resultado["tipo"] = "primer_grupo"

        resultados.append(
            resultado
        )

        print()

    # --------------------------------------------------------
    # SEGUNDO GRUPO — LIGA MX
    # --------------------------------------------------------

    resultados_segundo = []

    print("SEGUNDO GRUPO — LIGA MX")
    print("-" * 60)

    for indice, jugador in enumerate(
        JUGADORES_SEGUNDO_GRUPO_LIGAMX,
        start=1
    ):

        resultado = obtener_jugador(
            jugador,
            20 + indice,
            carpeta_fotos
        )

    # Sumar Leagues Cup 2026 solo a los 4 jugadores correspondientes.
    clave_jugador = clave_sofascore_manual(
        jugador.get("nombre", "")
    )

    if clave_jugador in LEAGUES_CUP_MANUAL:
        for estadistica in ESTADISTICAS:
            resultado["estadisticas"][estadistica] += (
                LEAGUES_CUP_MANUAL[clave_jugador].get(
                    estadistica,
                    0
                )
            )

        resultado["fuente"] = "LIGA MX"
        resultado["tipo"] = "ligamx"
        resultado["competencia"] = (
            "Apertura 2026 · 2026/2027"
        )

        resultados_segundo.append(
            resultado
        )

        print()

    # --------------------------------------------------------
    # SEGUNDO GRUPO — SOFASCORE
    # --------------------------------------------------------

    print("SEGUNDO GRUPO — SOFASCORE")
    print("-" * 60)
    print("Estadísticas SofaScore: captura manual")
    for indice, jugador in enumerate(
        JUGADORES_SEGUNDO_GRUPO_SOFASCORE,
        start=1
    ):

        resultado = (
            obtener_jugador_sofascore(
                jugador,
                indice,
                carpeta_fotos
            )
        )

        resultados_segundo.append(
            resultado
        )

        print()

    # --------------------------------------------------------
    # HTML
    # --------------------------------------------------------

    tarjetas_primer_grupo = "\n".join(
        crear_tarjeta(jugador)
        for jugador in resultados
    )

    tarjetas_segundo_grupo = "\n".join(
        crear_tarjeta_segundo_grupo(jugador)
        for jugador in resultados_segundo
    )

    archivo_html = (
        carpeta_base /
        "index.html"
    )

    archivo_html.write_text(
        crear_dashboard_con_pestanas(
            tarjetas_primer_grupo,
            tarjetas_segundo_grupo
        ),
        encoding="utf-8"
    )

    print("=" * 60)
    print(" DASHBOARD CREADO")
    print("=" * 60)
    print()
    print("HTML:")
    print(archivo_html)
    print()
    print("Fotos:")
    print(carpeta_fotos)
    print()
    print("Dashboard publicado como index.html.")
    print()


if __name__ == "__main__":
    main()
