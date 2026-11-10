"""Piezas comunes de las animaciones de A* (ciudades y laberinto)."""

from math import ceil
from typing import NamedTuple, Optional, Tuple

import matplotlib.pyplot as plt

# Colores de la animacion
AMARILLO = "#FFD400"  # nodos/celdas que A* ya recorrio 
AZUL = "#1F5FFF"  # camino final encontrado
VERDE = "#1FA34A"  # marca del punto inicial
ROJO = "#E5322D"  # marca de la meta


class PlanDeCuadros(NamedTuple):
    """Cómo se reparte la animación en cuadros."""

    nodos_por_cuadro: int  # cuantos nodos expandidos se muestran por cuadro
    cuadros_exploracion: int
    camino_por_cuadro: int  # cuantos nodos del camino final se pintan por cuadro
    cuadros_camino: int

    @property
    def total(self) -> int:
        return self.cuadros_exploracion + self.cuadros_camino


def crear_plan(
    n_expandidos: int,
    n_camino: int,
    intervalo_ms: int,
    nodos_por_cuadro: Optional[int] = None,
    camino_por_cuadro: Optional[int] = None,
    duracion_exploracion_s: float = 8.0,
    duracion_camino_s: float = 3.0,
) -> PlanDeCuadros:
    """Calcula los cuadros de la animación.

    Si no se indica `nodos_por_cuadro` / `camino_por_cuadro`, se eligen para que la
    exploración dure ~8 s y el trazado del camino final ~3 s, sin importar el tamaño
    del problema.
    """
    if nodos_por_cuadro is None:
        objetivo = max(1, int(duracion_exploracion_s * 1000 / intervalo_ms))
        nodos_por_cuadro = max(1, ceil(n_expandidos / objetivo))
    if camino_por_cuadro is None:
        objetivo = max(1, int(duracion_camino_s * 1000 / intervalo_ms))
        camino_por_cuadro = max(1, ceil(n_camino / objetivo))
    nodos_por_cuadro = max(1, int(nodos_por_cuadro))
    camino_por_cuadro = max(1, int(camino_por_cuadro))

    cuadros_exploracion = max(1, ceil(n_expandidos / nodos_por_cuadro))
    cuadros_camino = ceil(n_camino / camino_por_cuadro) if n_camino else 0
    return PlanDeCuadros(nodos_por_cuadro, cuadros_exploracion, camino_por_cuadro, cuadros_camino)


def visibles(plan: PlanDeCuadros, cuadro: int, n_expandidos: int, n_camino: int) -> Tuple[int, int]:
    """Devuelve (expandidos_visibles, camino_visible) en el cuadro dado.

    Primero se muestra la exploración (amarillo) y después se traza el camino (azul).
    Depende solo del número de cuadro, así que se puede dibujar cualquier cuadro
    en cualquier orden.
    """
    if cuadro < plan.cuadros_exploracion:
        return min(n_expandidos, (cuadro + 1) * plan.nodos_por_cuadro), 0
    avance = cuadro - plan.cuadros_exploracion + 1
    return n_expandidos, min(n_camino, avance * plan.camino_por_cuadro)


def terminar(fig, animacion, guardar_en: Optional[str], mostrar: bool, intervalo_ms: int) -> None:
    """Guarda la animación como GIF (opcional) y la muestra (opcional)."""
    if guardar_en:
        animacion.save(guardar_en, writer="pillow", fps=1000 / intervalo_ms, dpi=80)
        print(f"Animacion guardada en: {guardar_en}")
    if mostrar:
        plt.show()
    else:
        plt.close(fig)
