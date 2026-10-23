import matplotlib.pyplot as plt
import networkx as nx
from datos_mapa import MAPA_CIUDADES


def visualizar_grafo():
  # Creamos un grafo vacío
  G = nx.Graph()

  # Añadimos las ciudades y las distancias como pesos de las aristas
  for ciudad, vecinos in MAPA_CIUDADES.items():
    for vecino, distancia in vecinos.items():
      G.add_edge(ciudad, vecino, weight=distancia)

  # Configuramos una ventana mucho más grande (ej. 16x12 pulgadas)
  plt.figure(figsize=(16, 12))

  # 'k' controla la distancia de separación entre nodos (a mayor número, más espacio/expansión)
  # 'iterations' le da más tiempo al algoritmo para acomodar los nodos de forma limpia
  pos = nx.spring_layout(G, k=1.8, iterations=100, seed=42)

  # Dibujar nodos un poco más compactos y limpios
  nx.draw_networkx_nodes(
      G, pos, node_size=500, node_color='skyblue', node_shape='o'
  )

  # Etiquetas de las ciudades con fuente más legible para que no choquen
  nx.draw_networkx_labels(G, pos, font_size=8, font_weight='bold')

  # Dibujar las conexiones (aristas)
  nx.draw_networkx_edges(G, pos, width=1.5, edge_color='gray')

  # Mostrar las etiquetas con los kilómetros con fuente más chica para que no saturen el mapa
  pesos = nx.get_edge_attributes(G, 'weight')
  nx.draw_networkx_edge_labels(G, pos, edge_labels=pesos, font_size=7)

  plt.title(
      'Mapa de Ciudades',
      fontsize=14,
      fontweight='bold',
  )
  plt.axis('off')

  # Ajusta los márgenes para que nada quede cortado en los bordes de la ventana
  plt.tight_layout()
  plt.show()


if __name__ == '__main__':
  visualizar_grafo()