"""Animación de A* en el mapa de ciudades.

Amarillo: ciudades y carreteras que A* va recorriendo (expandiendo) mientras busca.
Azul:     ruta final encontrada.
Aro verde / rojo: ciudad de origen / destino.
"""

import difflib
import sys
import unicodedata
from pathlib import Path

_RAIZ = Path(__file__).resolve().parent.parent
for _ruta in (_RAIZ, _RAIZ / "algoritmo", _RAIZ / "ciudades"):
    if str(_ruta) not in sys.path:
        sys.path.insert(0, str(_ruta))

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.collections import LineCollection

from A_Star import a_estrella, vecinos_grafo
from HeuristicaCiudades import crear_heuristica_ciudades
from datos_mapa import MAPA_CIUDADES
from posiciones import POSICIONES  # posiciones (x, y) de las ciudades (ciudades/posiciones.py)
from visualizacion.comun import AMARILLO, AZUL, ROJO, VERDE, crear_plan, terminar, visibles

GRIS_NODO = "#D9D9D9"
GRIS_ARISTA = "#9A9A9A"


def listar_ciudades():
    """Nombres de todas las ciudades del mapa, en orden alfabético."""
    return sorted(MAPA_CIUDADES)


def _normalizar(texto):
    """Minúsculas, sin acentos y sin espacios sobrantes (para comparar nombres)."""
    sin_acentos = unicodedata.normalize("NFD", str(texto))
    sin_acentos = "".join(c for c in sin_acentos if unicodedata.category(c) != "Mn")
    return " ".join(sin_acentos.lower().split())


def buscar_ciudad(nombre):
    """Devuelve el nombre exacto de la ciudad tal como está en el mapa.

    No distingue mayúsculas ni acentos ("la paz", "Mulegé" funcionan). Si no existe,
    lanza ValueError sugiriendo nombres parecidos.
    """
    por_normal = {_normalizar(c): c for c in MAPA_CIUDADES}
    clave = _normalizar(nombre)
    if clave in por_normal:
        return por_normal[clave]
    parecidas = difflib.get_close_matches(clave, list(por_normal), n=3, cutoff=0.5)
    sugerencia = f" ¿Quisiste decir: {', '.join(por_normal[p] for p in parecidas)}?" if parecidas else ""
    raise ValueError(
        f"La ciudad {nombre!r} no existe en el mapa.{sugerencia} "
        f"Ciudades disponibles: {', '.join(listar_ciudades())}."
    )


def resolver_ciudades(
    origen="Tijuana",
    destino="La Paz",
    intervalo_ms=450,
    nodos_por_cuadro=1,
    camino_por_cuadro=1,
    guardar_en=None,
    mostrar=True,
):
    """Busca con A* la ruta más corta entre dos ciudades y la anima.

    Para cambiar el origen o el destino basta con pasar otros nombres:
        resolver_ciudades(origen="Mexicali", destino="Cabo San Lucas")

    Parámetros de la animación (opcionales):
        intervalo_ms:      milisegundos entre cuadros (menor = más rápido).
        nodos_por_cuadro:  ciudades exploradas que se pintan por cuadro.
        camino_por_cuadro: ciudades de la ruta final que se pintan por cuadro.
        guardar_en:        ruta de un .gif para guardar la animación.
        mostrar:           False para no abrir la ventana.

    Devuelve el Resultado de a_estrella (camino, costo, nodos_expandidos).
    """
    origen = buscar_ciudad(origen)
    destino = buscar_ciudad(destino)

    # 1) Se ejecuta A* anotando, en orden, cada ciudad que expande y desde cuál llegó.
    expandidas = []
    resultado = a_estrella(
        origen,
        destino,
        vecinos_grafo(MAPA_CIUDADES),
        crear_heuristica_ciudades(MAPA_CIUDADES, POSICIONES),
        al_expandir=lambda ciudad, padre: expandidas.append((ciudad, padre)),
    )
    camino = resultado.camino or []

    print(f"Ciudades: {origen} -> {destino}")
    if resultado.camino is None:
        print(f"No existe ruta. Ciudades exploradas: {resultado.nodos_expandidos}")
    else:
        print(" -> ".join(camino))
        print(f"Distancia: {resultado.costo} km | ciudades exploradas: {resultado.nodos_expandidos}")

    # 2) Se dibuja el mapa y se anima esa ejecución.
    ciudades = list(MAPA_CIUDADES)
    indice = {c: i for i, c in enumerate(ciudades)}
    pos = {c: (POSICIONES[c][0], -POSICIONES[c][1]) for c in ciudades}  # norte arriba

    # Una arista por cada par de ciudades conectadas.
    aristas = []  # (a, b)
    indice_arista = {}
    for a, vecinos in MAPA_CIUDADES.items():
        for b in vecinos:
            clave = frozenset((a, b))
            if clave not in indice_arista:
                indice_arista[clave] = len(aristas)
                aristas.append((a, b))

    fig, ax = plt.subplots(figsize=(17, 9))
    lineas = LineCollection(
        [[pos[a], pos[b]] for a, b in aristas],
        colors=[GRIS_ARISTA] * len(aristas),
        linewidths=[1.5] * len(aristas),
        zorder=1,
    )
    ax.add_collection(lineas)
    for a, b in aristas:  # kilómetros sobre cada carretera
        km = MAPA_CIUDADES[a].get(b, MAPA_CIUDADES.get(b, {}).get(a))
        ax.text(
            (pos[a][0] + pos[b][0]) / 2,
            (pos[a][1] + pos[b][1]) / 2,
            str(km),
            fontsize=7,
            ha="center",
            va="center",
            zorder=2,
            bbox=dict(boxstyle="round,pad=0.1", fc="white", ec="none", alpha=0.75),
        )

    nodos = ax.scatter(
        [pos[c][0] for c in ciudades],
        [pos[c][1] for c in ciudades],
        s=450,
        c=[GRIS_NODO] * len(ciudades),
        edgecolors="black",
        linewidths=0.8,
        zorder=3,
    )
    for c in ciudades:  # nombre encima de cada ciudad
        ax.annotate(
            c,
            xy=pos[c],
            xytext=(0, 13),
            textcoords="offset points",
            ha="center",
            va="bottom",
            fontsize=8,
            fontweight="bold",
            zorder=6,
            bbox=dict(boxstyle="round,pad=0.12", fc="white", ec="none", alpha=0.8),
        )
    for ciudad, color in ((origen, VERDE), (destino, ROJO)):  # aros de origen y destino
        ax.scatter(
            [pos[ciudad][0]], [pos[ciudad][1]],
            s=1100, facecolors="none", edgecolors=color, linewidths=3.5, zorder=5,
        )

    ax.autoscale_view()
    ax.margins(0.04)
    ax.axis("off")
    fig.tight_layout(rect=(0, 0, 1, 0.95))  # deja espacio arriba para el título

    plan = crear_plan(len(expandidas), len(camino), intervalo_ms, nodos_por_cuadro, camino_por_cuadro)

    def dibujar(cuadro):
        n_exp, n_cam = visibles(plan, cuadro, len(expandidas), len(camino))
        color_nodo = [GRIS_NODO] * len(ciudades)
        color_arista = [GRIS_ARISTA] * len(aristas)
        ancho_arista = [1.5] * len(aristas)

        for ciudad, padre in expandidas[:n_exp]:  # recorrido de la búsqueda
            color_nodo[indice[ciudad]] = AMARILLO
            if padre is not None:
                k = indice_arista[frozenset((ciudad, padre))]
                color_arista[k], ancho_arista[k] = AMARILLO, 3.5

        for ciudad in camino[:n_cam]:  # ruta final
            color_nodo[indice[ciudad]] = AZUL
        for a, b in zip(camino[:n_cam], camino[1:n_cam]):
            k = indice_arista[frozenset((a, b))]
            color_arista[k], ancho_arista[k] = AZUL, 5

        nodos.set_facecolor(color_nodo)
        lineas.set_color(color_arista)
        lineas.set_linewidth(ancho_arista)

        if n_cam == 0:
            ax.set_title(f"A*: {origen} → {destino} | explorando... ciudades recorridas: {n_exp}", fontsize=14)
        elif resultado.camino is None:
            ax.set_title(f"No existe ruta de {origen} a {destino} | ciudades recorridas: {n_exp}", fontsize=14)
        elif n_cam < len(camino):
            ax.set_title(f"A*: {origen} → {destino} | trazando la ruta...", fontsize=14)
        else:
            ax.set_title(
                f"Ruta encontrada: {resultado.costo} km | ciudades recorridas: {n_exp}", fontsize=14
            )
        return nodos, lineas

    animacion = FuncAnimation(fig, dibujar, frames=plan.total, interval=intervalo_ms, repeat=False)
    terminar(fig, animacion, guardar_en, mostrar, intervalo_ms)
    return resultado
