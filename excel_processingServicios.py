import pandas as pd
import re

def read_servicios_file(file_path):
    # Cargar la hoja
    xls = pd.read_excel(file_path, header=0)
    
    # lista para almacenar los datos procesados
    processed_data = []

    # Iterar sobre cada fila en el dataframe
    for _, row in xls.iterrows():
        # Dividir 'Participantes' basándose en las comas para obtener nombres individuales
        participantes = [name.strip() for name in row['Participantes'].split(",")]

        # Preparar los datos procesados
        data = {
            "Tipo": row["Tipo"],
            "Modalidad": row["Modalidad"],
            "Fecha": row["Fecha"],
            "Escuela": row["Escuela"],
            "Ciclo": row["Ciclo"],
            "Grado": row["Grado"],
            "Grupo": row["Grupo"],
            "Participantes": participantes
        }

        # Agregar los datos procesados a la lista
        processed_data.append(data)

    return processed_data

