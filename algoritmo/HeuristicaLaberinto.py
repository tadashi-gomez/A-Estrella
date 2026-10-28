"""Heurísticas para el laberinto.

Los nodos son celdas (fila, columna). Como el movimiento es en 4 direcciones
y cada paso cuesta 1, la distancia Manhattan es admisible (no puede ser mayor
que el número real de pasos) y además consistente.
"""

import math


def distancia_manhattan(celda, meta):
    """|Δfila| + |Δcolumna|. Es la heurística recomendada para este laberinto."""
    return abs(celda[0] - meta[0]) + abs(celda[1] - meta[1])


def distancia_euclidiana(celda, meta):
    """Línea recta entre las celdas. También admisible, pero más débil que Manhattan
    (expande más nodos); sirve para comparar."""
    return math.hypot(celda[0] - meta[0], celda[1] - meta[1])
