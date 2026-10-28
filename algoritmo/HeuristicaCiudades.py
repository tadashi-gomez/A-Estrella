"""Heurística para el mapa de ciudades.

Se usa la distancia en línea recta entre las posiciones (x, y) de las ciudades
(las de POSICIONES en ciudades/mapa_ciudades.py), convertida a kilómetros.

Esas posiciones están en píxeles de una imagen de referencia, no en km, así que
hay que multiplicarlas por una escala. Para que la heurística sea admisible
(nunca sobreestime) la escala se calcula con los propios datos:

    escala = mínimo de (km de la carretera / distancia en píxeles) sobre todas las aristas

Con esa escala, para cada arista se cumple escala * distancia_px <= km reales,
y por la desigualdad triangular eso se mantiene para cualquier camino. Por lo
tanto h(n) <= costo real hasta la meta y A* devuelve la ruta óptima.
"""

import math


def calcular_escala(mapa, posiciones):
    """Km por píxel más pequeño entre todas las aristas del grafo."""
    escala = math.inf
    for ciudad, vecinos in mapa.items():
        for vecino, km in vecinos.items():
            pixeles = math.dist(posiciones[ciudad], posiciones[vecino])
            if pixeles > 0:
                escala = min(escala, km / pixeles)
    return escala


def crear_heuristica_ciudades(mapa, posiciones):
    """Devuelve h(ciudad, meta) -> km estimados en línea recta.

    Uso:
        h = crear_heuristica_ciudades(MAPA_CIUDADES, POSICIONES)
        a_estrella("Tijuana", "La Paz", vecinos_grafo(MAPA_CIUDADES), h)
    """
    escala = calcular_escala(mapa, posiciones)

    def heuristica(ciudad, meta):
        return escala * math.dist(posiciones[ciudad], posiciones[meta])

    return heuristica
