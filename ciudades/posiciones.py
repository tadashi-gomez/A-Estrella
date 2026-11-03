"""Posiciones (x, y) aproximadas de las ciudades, tomadas de la imagen de referencia.

Se usan para (1) calcular la heuristica de ciudades (distancia en linea recta) y
(2) dibujar el mapa en la animacion. La y crece hacia abajo (como en una imagen),
asi que al dibujar se invierte para que el norte quede arriba.

Estan en un archivo aparte para que el algoritmo y la animacion no dependan de
como se dibuje el mapa en mapa_ciudades.py.
"""

POSICIONES = {
    "Tijuana": (55, 18),
    "Tecate": (118, 12),
    "Rosarito": (22, 85),
    "Ensenada": (50, 138),
    "San Quintin": (55, 243),
    "Mexicali": (207, 13),
    "San Luis Rio Colorado": (318, 18),
    "San Felipe": (195, 172),
    "Guerrero negro": (145, 326),
    "Santa Rosalia": (232, 405),
    "Mulege": (265, 513),
    "Ciudad Constitucion": (245, 655),
    "San Carlos": (143, 689),
    "La Paz": (293, 790),
    "San Jose del Cabo": (333, 858),
    "Cabo San Lucas": (256, 902),
    "Sonoyta": (508, 63),
    "Puerto Penasco": (370, 147),
    "Caborca": (585, 233),
    "Nogales": (708, 98),
    "Cananea": (862, 217),
    "Santa Ana": (710, 270),
    "Agua Prieta": (990, 125),
    "Janos": (1111, 154),
    "Ciudad Juarez": (1437, 58),
    "Villa Ahumada": (1492, 172),
    "Flores Magon": (1270, 281),
    "Sueco": (1528, 318),
    "Moctezuma": (937, 358),
    "Hermosillo": (725, 413),
    "Guaymas": (655, 538),
    "Ciudad Obregon": (757, 628),
    "Yecora": (1025, 524),
    "Ciudad Cuauhtemoc": (1449, 531),
    "Chihuahua": (1583, 443),
    "Ojinaga": (1680, 209),
    "Delicias": (1658, 565),
    "Ciudad Jimenez": (1706, 688),
    "Parral": (1547, 760),
}
