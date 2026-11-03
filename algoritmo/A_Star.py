import heapq
from itertools import count
from typing import Callable, Hashable, Iterable, List, NamedTuple, Optional, Tuple

Nodo = Hashable
FuncionVecinos = Callable[[Nodo], Iterable[Tuple[Nodo, float]]]
Heuristica = Callable[[Nodo, Nodo], float]


class Resultado(NamedTuple):
    camino: Optional[List[Nodo]]  # None si no existe camino
    costo: float  # costo total del camino (inf si no existe)
    nodos_expandidos: int  # cuántos nodos saco de la lista abierta y expandio


def a_estrella(
    inicio: Nodo,
    meta: Nodo,
    obtener_vecinos: FuncionVecinos,
    heuristica: Heuristica,
    al_expandir: Optional[Callable[[Nodo, Optional[Nodo]], None]] = None,
) -> Resultado:
    """
    Busca el camino de menor costo de inicio a meta con A*.

    Parametros:
        inicio, meta:    nodos de origen y destino.
        obtener_vecinos: función nodo -> iterable de (vecino, costo_del_paso).
        heuristica:      función (nodo, meta) -> estimación del costo restante.
        al_expandir:     (opcional) función que se llama cada vez que A* expande un
                         nodo, como al_expandir(nodo, padre). Sirve para seguir paso
                         a paso la búsqueda (por ejemplo, para animarla). padre es
                         None en el nodo inicial.

    f(n) = g(n) + h(n), donde g es el costo real acumulado desde inicio
    y h es la estimación hasta meta. El camino devuelto es optimo si la
    heuristica es admisible (nunca sobreestima el costo real).
    """
    contador = count()  # desempata entradas con igual f y h (orden de llegada)

    g = {inicio: 0}  # mejor costo conocido desde inicio hasta cada nodo
    padre = {inicio: None}  # para reconstruir el camino al final

    h_inicial = heuristica(inicio, meta)
    # Entradas de la lista abierta: (f, h, desempate, g_al_insertar, nodo).
    # Ante igual f se prefiere menor h (el nodo que parece más cercano a la meta).
    abierta = [(h_inicial, h_inicial, next(contador), 0, inicio)]
    expandidos = 0

    while abierta:
        _, _, _, g_entrada, actual = heapq.heappop(abierta)

        # Entrada obsoleta: despues de insertarla se encontro un camino mejor.
        if g_entrada > g[actual]:
            continue

        # La prueba de meta se hace al sacar el nodo (no al generarlo);
        # así el primer camino que llega a la meta es el óptimo.
        if actual == meta:
            return Resultado(_reconstruir_camino(padre, actual), g[actual], expandidos)

        expandidos += 1
        if al_expandir is not None:
            al_expandir(actual, padre[actual])

        for vecino, costo_paso in obtener_vecinos(actual):
            g_nuevo = g[actual] + costo_paso
            if vecino not in g or g_nuevo < g[vecino]:
                g[vecino] = g_nuevo
                padre[vecino] = actual
                h = heuristica(vecino, meta)
                heapq.heappush(abierta, (g_nuevo + h, h, next(contador), g_nuevo, vecino))

    return Resultado(None, float("inf"), expandidos)


def _reconstruir_camino(padre, nodo) -> List[Nodo]:
    camino = []
    while nodo is not None:
        camino.append(nodo)
        nodo = padre[nodo]
    camino.reverse()
    return camino


# Funciones de expansion (vecinos) para cada problema.
# Son lo minimo para que a_estrella pueda recorrer cada tipo de mapa.

def vecinos_grafo(mapa):
    """Vecinos para el mapa de ciudades: {ciudad: {vecina: distancia_km}}."""

    def vecinos(ciudad):
        return mapa[ciudad].items()

    return vecinos


def vecinos_laberinto(matriz):
    """Vecinos para el laberinto: matriz de 0 (camino) y 1 (pared).

    Movimientos en 4 direcciones (arriba, abajo, izquierda, derecha),
    cada paso cuesta 1. Los nodos son tuplas (fila, columna).
    """
    filas = len(matriz)
    columnas = len(matriz[0])

    def vecinos(celda):
        fila, col = celda
        for d_fila, d_col in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            n_fila, n_col = fila + d_fila, col + d_col
            if 0 <= n_fila < filas and 0 <= n_col < columnas and matriz[n_fila][n_col] == 0:
                yield (n_fila, n_col), 1

    return vecinos
