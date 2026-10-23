import matplotlib.pyplot as plt


def visualizar_csv_laberinto(ruta_csv):
  matriz = []

  # Abrimos el archivo CSV línea por línea
  with open(ruta_csv, 'r', encoding='utf-8') as f:
    for linea in f:
      # Limpiamos los saltos de línea y separamos por comas, convirtiendo a enteros
      fila = [int(x) for x in linea.strip().split(',') if x != '']
      matriz.append(fila)

  # Configuramos la visualización gráfica
  plt.figure(figsize=(8, 8))
  # Usamos cmap='binary' para ver paredes negras (1) y caminos blancos (0)
  plt.imshow(matriz, cmap='binary')

  plt.title('Laberinto 150x150', fontsize=14)
  plt.xlabel('Eje X')
  plt.ylabel('Eje Y')
  plt.show()


if __name__ == '__main__':
  visualizar_csv_laberinto('laberinto_150x150.csv')