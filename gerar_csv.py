import random
from shapely.geometry import Point, Polygon
import csv
from datetime import datetime, timedelta
import os

# Coordenadas dos vértices do polígono
vertices = [
    (-17.31721813, -41.97760306),
    (-17.14670391, -41.24975887),
    (-18.33954368, -42.05176077),
    (-18.38907108, -41.20856015)
]

# Criar o polígono com os vértices fornecidos
poligono = Polygon(vertices)

def gerar_coordenadas_no_poligono(num_coordenadas):
    coordenadas = []
    min_lat = min(v[0] for v in vertices)
    max_lat = max(v[0] for v in vertices)
    min_lon = min(v[1] for v in vertices)
    max_lon = max(v[1] for v in vertices)
    
    while len(coordenadas) < num_coordenadas:
        # Gerar coordenadas aleatórias dentro do retângulo delimitador do polígono
        latitude = random.uniform(min_lat, max_lat)
        longitude = random.uniform(min_lon, max_lon)
        ponto = Point(latitude, longitude)
        
        # Verificar se o ponto está dentro do polígono
        if poligono.contains(ponto):
            coordenadas.append((latitude, longitude))
    return coordenadas

def gerar_data_aleatoria():
    inicio = datetime(2027, 1, 1)
    fim = datetime(2027, 12, 31)
    delta = fim - inicio
    dias_aleatorios = random.randint(0, delta.days)
    data_aleatoria = inicio + timedelta(days=dias_aleatorios)
    return data_aleatoria.strftime("%d/%m/%Y")

def gerar_codigo_reds():
    # Modelo 2027-0????????-005
    parte_inicial = "2027-0"
    parte_meio = ''.join(str(random.randint(0, 9)) for _ in range(8))
    parte_final = "-005"
    return f"{parte_inicial}{parte_meio}{parte_final}"

def gerar_tabela_csv(num_linhas, caminho):
    coordenadas = gerar_coordenadas_no_poligono(num_linhas)
    with open(caminho, mode="w", newline='', encoding="utf-8") as arquivo_csv:
        escritor = csv.writer(arquivo_csv)
        # Escrever cabeçalho
        escritor.writerow(["REDS", "DATA", "Latitude", "Longitude"])
        for i in range(num_linhas):
            reds = gerar_codigo_reds()
            data = gerar_data_aleatoria()
            latitude, longitude = coordenadas[i]
            escritor.writerow([reds, data, latitude, longitude])

def main():
    try:
        # Perguntar o número de linhas
        num_linhas = int(input("Quantas linhas você deseja gerar? "))
        
        # Perguntar o caminho para salvar
        caminho = input("Digite o caminho completo para salvar o arquivo (exemplo: C:/caminho/arquivo.csv): ")
        
        # Validar extensão do arquivo
        if not caminho.endswith(".csv"):
            caminho += ".csv"
        
        # Criar a tabela e salvar no caminho especificado
        gerar_tabela_csv(num_linhas, caminho)
        print(f"Arquivo CSV gerado com sucesso em: {caminho}")
    except Exception as e:
        print(f"Ocorreu um erro: {e}")

if __name__ == "__main__":
    main()
