"""
Hay dos formas de elegir el punto inicial y el final:

1) Editando las constantes de abajo y ejecutando el archivo (por ejemplo, desde PyCharm).
2) Con argumentos en la terminal:

    python main.py ciudades --origen Mexicali --destino "Cabo San Lucas"
    python main.py ciudades --listar
    python main.py laberinto --inicio 1 1 --meta 147 147
    python main.py laberinto --inicio 5 3 --meta 101 121 --intervalo 10

   Opciones de animacion (en ambos problemas):
    --intervalo MS           milisegundos entre cuadros (menor = más rápido)
    --nodos-por-cuadro N     cuántos nodos explorados se pintan en cada cuadro

"""

import argparse
import sys

# ----------------------------------------------------------------------------
# CONFIGURACION
# ----------------------------------------------------------------------------
PROBLEMA = "ciudades"  # "ciudades" o "laberinto"

CIUDAD_ORIGEN = "Tijuana"
CIUDAD_DESTINO = "La Paz"

LABERINTO_INICIO = (1, 1)  # (fila, columna), contando desde 0; la fila 0 es la de arriba
LABERINTO_META = (147, 147)  # tiene que ser una celda libre (valor 0 en el CSV)


def _crear_parser():
    comunes = argparse.ArgumentParser(add_help=False)
    comunes.add_argument("--intervalo", type=int, help="milisegundos entre cuadros de la animación")
    comunes.add_argument("--nodos-por-cuadro", type=int, help="nodos explorados que se pintan por cuadro")
    comunes.add_argument("--guardar", metavar="ARCHIVO.gif", help="guarda la animación como GIF")
    comunes.add_argument("--sin-ventana", action="store_true", help="no abre la ventana de la animación")

    parser = argparse.ArgumentParser(
        description="Algoritmo A* con animación (amarillo = recorrido, azul = camino final).",
        epilog="Sin argumentos se usan las constantes de la sección CONFIGURACIÓN de main.py.",
    )
    sub = parser.add_subparsers(dest="problema")

    c = sub.add_parser("ciudades", parents=[comunes], help="mapa de ciudades")
    c.add_argument("--origen", default=CIUDAD_ORIGEN)
    c.add_argument("--destino", default=CIUDAD_DESTINO)
    c.add_argument("--listar", action="store_true", help="muestra las ciudades disponibles y termina")

    l = sub.add_parser("laberinto", parents=[comunes], help="laberinto 150x150")
    l.add_argument("--inicio", nargs=2, type=int, default=list(LABERINTO_INICIO), metavar=("FILA", "COL"))
    l.add_argument("--meta", nargs=2, type=int, default=list(LABERINTO_META), metavar=("FILA", "COL"))
    return parser


def main(argv=None):
    args = _crear_parser().parse_args(argv)
    problema = args.problema or PROBLEMA

    # Opciones de animacion
    opciones = {"mostrar": not getattr(args, "sin_ventana", False)}
    if getattr(args, "intervalo", None):
        opciones["intervalo_ms"] = args.intervalo
    if getattr(args, "nodos_por_cuadro", None):
        opciones["nodos_por_cuadro"] = args.nodos_por_cuadro
    if getattr(args, "guardar", None):
        opciones["guardar_en"] = args.guardar

    try:
        if problema == "ciudades":
            from visualizacion.animacion_ciudades import listar_ciudades, resolver_ciudades

            if getattr(args, "listar", False):
                print("\n".join(listar_ciudades()))
                return 0
            origen = getattr(args, "origen", CIUDAD_ORIGEN)
            destino = getattr(args, "destino", CIUDAD_DESTINO)
            resolver_ciudades(origen, destino, **opciones)
        elif problema == "laberinto":
            from visualizacion.animacion_laberinto import resolver_laberinto

            inicio = tuple(getattr(args, "inicio", LABERINTO_INICIO))
            meta = tuple(getattr(args, "meta", LABERINTO_META))
            resolver_laberinto(inicio, meta, **opciones)
        else:
            print(f"PROBLEMA debe ser 'ciudades' o 'laberinto', no {problema!r}.", file=sys.stderr)
            return 2
    except ValueError as error:  # ciudad inexistente, celda pared / fuera del laberinto, etc.
        print(f"Error: {error}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
