# 'dataset' tem os dados de entrada para este script
# 'dataset' tem os dados de entrada para este script

import geopandas as gpd
import pandas as pd
from shapely.geometry import Point

# --- Configurações do Caminho ---
# "C:\Users\valfr\Downloads\csv\Mapas_Tratados\SubSetores_19BPM_GeoJSON.json"
geojson_path = r"C:\Users\valfr\Downloads\csv\Mapas_Tratados\SubSetores_19BPM_GeoJSON.json"

# --- Carregar Dados do Power BI ---
df = dataset  # A tabela 'coordenadas_9k' será carregada automaticamente como 'dataset'

# --- Criar GeoDataFrame para a Tabela 'f_CVPe' ---
df['geometry'] = df.apply(lambda row: Point(row['Longitude'], row['Latitude']), axis=1)
points_gdf = gpd.GeoDataFrame(df, geometry='geometry', crs="EPSG:4326")  # Define EPSG:4326 diretamente

# --- Carregar o GeoJSON ---
polygons_gdf = gpd.read_file(geojson_path)

# Garantir que o GeoJSON está no CRS EPSG:4326
if polygons_gdf.crs != "EPSG:4326":
    polygons_gdf = polygons_gdf.to_crs("EPSG:4326")

# --- Realizar Interseção Geoespacial ---
result_gdf = gpd.sjoin(points_gdf, polygons_gdf, how="left", predicate="within")

# --- Preparar Resultado ---
output_columns = list(df.columns) + ['name', 'PELOTAO', 'CIA_PM', 'municipio']
output = result_gdf[output_columns]

# Renomear as colunas do GeoJSON
output = output.rename(columns={
    'name': 'poligono_intersectado',
    'PELOTAO': 'geojson_pelotao',
    'CIA_PM': 'geojson_cia_pm',
    'NM_MUNICIPIO': 'geojson_municipio'
})

# Ajustar o formato dos números para usar vírgulas como separadores decimais
output['Latitude'] = output['Latitude'].apply(lambda x: f"{x:.6f}".replace('.', ','))
output['Longitude'] = output['Longitude'].apply(lambda x: f"{x:.6f}".replace('.', ','))

# Converter para DataFrame para exportação ao Power BI
output = pd.DataFrame(output)
