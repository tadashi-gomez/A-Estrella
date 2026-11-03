"""Animación de A* en el laberinto.

Amarillo: celdas que A* va recorriendo (expandiendo) mientras busca.
Azul:     camino final encontrado.
Verde / rojo: punto inicial / meta.

Las celdas se indican como (fila, columna), contando desde 0 y con la fila 0 arriba,
igual que en el archivo CSV y en la imagen del laberinto.
"""

import sys
from pathlib import Path

_RAIZ = Path(__file__).resolve().parent.parent
for _ruta in (_RAIZ, _RAIZ / "algoritmo"):
    if str(_ruta) not in sys.path:
        sys.path.insert(0, str(_ruta))

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
from matplotlib.colors import to_rgb

from A_Star import a_estrella, vecinos_laberinto
from HeuristicaLaberinto import distancia_manhattan
from visualizacion.comun import AMARILLO, AZUL, ROJO, VERDE, crear_plan, terminar, visibles

RUTA_CSV = _RAIZ / "laberinto" / "laberinto_150x150.csv"


def cargar_laberinto(ruta_csv=RUTA_CSV):
    """Lee el CSV y devuelve la matriz (lista de listas) de 0 = camino y 1 = pared."""
    matriz = []
    with open(ruta_csv, "r", encoding="utf-8") as f:
        for linea in f:
            fila = [int(x) for x in linea.strip().split(",") if x != ""]
            if fila:
                matriz.append(fila)
    return matriz


def validar_celda(matriz, celda, nombre):
    """Comprueba que `celda` = (fila, columna) esté dentro del laberinto y no sea pared.

    Devuelve la celda como tupla de enteros; si no es válida lanza ValueError con un
    mensaje que explica el problema.
    """
    try:
        fila, col = (int(celda[0]), int(celda[1]))
        if len(celda) != 2:
            raise ValueError
    except (TypeError, ValueError, IndexError):
        raise ValueError(f"{nombre.capitalize()} debe ser (fila, columna) con dos numeros enteros, no {celda!r}.")

    filas, columnas = len(matriz), len(matriz[0])
    if not (0 <= fila < filas and 0 <= col < columnas):
        raise ValueError(
            f"{nombre.capitalize()} {(fila, col)} esta fuera del laberinto "
            f"(filas 0-{filas - 1}, columnas 0-{columnas - 1})."
        )
    if matriz[fila][col] != 0:
        raise ValueError(f"{nombre.capitalize()} {(fila, col)} es una pared; elige una celda libre (valor 0).")
    return (fila, col)


def resolver_laberinto(
    inicio=(1, 1),
    meta=(147, 147),
    ruta_csv=RUTA_CSV,
    intervalo_ms=30,
    nodos_por_cuadro=None,
    camino_por_cuadro=None,
    guardar_en=None,
    mostrar=True,
):
    """Resuelve el laberinto con A* (heurística Manhattan) y lo anima.

    Para cambiar el punto inicial o la meta basta con pasar otras celdas:
        resolver_laberinto(inicio=(5, 3), meta=(101, 121))
    Las dos celdas tienen que ser camino libre (0 en el CSV), no pared.

    Parámetros de la animación (opcionales):
        intervalo_ms:     milisegundos entre cuadros (menor = más rápido).
        nodos_por_cuadro: celdas exploradas que se pintan por cuadro (None = automático).
        camino_por_cuadro: celdas del camino final que se pintan por cuadro (None = automático).
        guardar_en:       ruta de un .gif para guardar la animación.
        mostrar:          False para no abrir la ventana.

    Devuelve el Resultado de a_estrella (camino, costo, nodos_expandidos).
    """
    matriz = cargar_laberinto(ruta_csv)
    inicio = validar_celda(matriz, inicio, "el punto inicial")
    meta = validar_celda(matriz, meta, "la meta")

    # 1) Se ejecuta A* anotando, en orden, cada celda que expande.
    expandidas = []
    resultado = a_estrella(
        inicio,
        meta,
        vecinos_laberinto(matriz),
        distancia_manhattan,
        al_expandir=lambda celda, padre: expandidas.append(celda),
    )
    camino = resultado.camino or []

    print(f"Laberinto: {inicio} -> {meta}")
    if resultado.camino is None:
        print(f"No existe camino. Celdas exploradas: {resultado.nodos_expandidos}")
    else:
        print(f"Camino encontrado: {resultado.costo} pasos | celdas exploradas: {resultado.nodos_expandidos}")

    # 2) Se anima esa ejecución: primero lo explorado (amarillo), luego el camino (azul).
    filas_e = np.array([c[0] for c in expandidas], dtype=int)
    cols_e = np.array([c[1] for c in expandidas], dtype=int)
    filas_p = np.array([c[0] for c in camino], dtype=int)
    cols_p = np.array([c[1] for c in camino], dtype=int)

    base = np.ones((len(matriz), len(matriz[0]), 3))  # blanco = camino libre
    base[np.array(matriz) == 1] = (0, 0, 0)  # negro = pared
    amarillo, azul = to_rgb(AMARILLO), to_rgb(AZUL)

    plan = crear_plan(len(expandidas), len(camino), intervalo_ms, nodos_por_cuadro, camino_por_cuadro)

    fig, ax = plt.subplots(figsize=(8, 8))
    imagen = ax.imshow(base, interpolation="nearest")
    ax.scatter([inicio[1]], [inicio[0]], s=90, c=VERDE, marker="o", edgecolors="black", zorder=3)
    ax.scatter([meta[1]], [meta[0]], s=90, c=ROJO, marker="s", edgecolors="black", zorder=3)
    ax.set_xticks([])
    ax.set_yticks([])

    def dibujar(cuadro):
        n_exp, n_cam = visibles(plan, cuadro, len(expandidas), len(camino))
        img = base.copy()
        img[filas_e[:n_exp], cols_e[:n_exp]] = amarillo
        img[filas_p[:n_cam], cols_p[:n_cam]] = azul
        imagen.set_data(img)

        if n_cam == 0:
            ax.set_title(f"A* explorando... celdas recorridas: {n_exp}")
        elif resultado.camino is None:
            ax.set_title(f"No existe camino | celdas recorridas: {n_exp}")
        elif n_cam < len(camino):
            ax.set_title(f"Trazando el camino... celdas recorridas: {n_exp}")
        else:
            ax.set_title(f"Camino encontrado: {resultado.costo} pasos | celdas recorridas: {n_exp}")
        return (imagen,)

    animacion = FuncAnimation(fig, dibujar, frames=plan.total, interval=intervalo_ms, repeat=False)
    terminar(fig, animacion, guardar_en, mostrar, intervalo_ms)
    return resultado
