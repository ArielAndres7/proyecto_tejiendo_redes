import pandas as pd
import re

def extract_grado_grupo(data_column):
    # Separa 'Grupo' en 'Grado' y 'Grupo'
    data_column = data_column.str.replace('º', '°')
    grado = data_column.str.extract(r'(\d+°)').astype(str)
    grupo = data_column.str.extract(r'([A-Z]$)').astype(str)
    return grado, grupo

def extract_mapeo_data(sheet):
    # Extrayendo las columnas requeridas
    data = sheet[["Escuela", "Grupo", "Ciclo", "ID", "Label", "Nombre", "Apellido", "GRADO ENTRADA", "GRADO SALIDA", "CENTRALIDAD", "PERCEPCIÓN RELACIONAL", "PERCEPCIÓN CONDUCTUAL", "PERCEPCIÓN ACADÉMICA"]].copy()

    # Procesa el campo 'Grupo' para dividirlo en 'GRADO' y 'GRUPO'
    data['GRADO'] = data['Grupo'].str.extract(r'(\d+)').astype(str) + '°'
    data['Grupo'] = data['Grupo'].str.extract(r'([A-Z]$)').astype(str)
    
    # Combina 'Nombre' y 'Apellido' en un único campo 'Nombre'
    data['Nombre'] = data['Nombre'] + ' ' + data['Apellido']
    data.drop(columns=['Apellido'], inplace=True)

    # Reordena las columnas para mover 'GRADO' junto a 'Grupo'
    columns_ordered = ["Escuela", "Grupo", "GRADO", "Ciclo", "ID", "Label", "Nombre", "GRADO ENTRADA", "GRADO SALIDA", "CENTRALIDAD", "PERCEPCIÓN RELACIONAL", "PERCEPCIÓN CONDUCTUAL", "PERCEPCIÓN ACADÉMICA"]
    data = data[columns_ordered]

    # Reemplaza todos los valores NaN por None (evita errores en la DB)
    data = data.where(pd.notna(data), None)

    # Convierte los datos a una lista de diccionarios
    data_list = data.to_dict(orient='records')

    return data_list

def read_mapeo_file(file_path):
    # Lee el archivo 'mapeo' y extrae los datos relevantes
    xls = pd.ExcelFile(file_path)

    # Extrae los datos de la hoja de mapeo
    mapeo_sheet = xls.parse(0)
    mapeo_data = extract_mapeo_data(mapeo_sheet)
    
    return mapeo_data
