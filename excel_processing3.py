import pandas as pd
import re

def read_servicios_file(file_path):
    # Load the spreadsheet
    xls = pd.read_excel(file_path, header=0)  # Assumes the first row as the header
    
    # A list to store processed data
    processed_data = []

    # Iterate over each row in the dataframe
    for _, row in xls.iterrows():
        # Split 'Escuela y ciclo' into 'Escuela' and 'Ciclo'
        escuela, ciclo = row['Escuela y ciclo'].split()

        # Split 'Participantes' based on commas to get individual names
        participantes = [name.strip() for name in row['Participantes'].split(",")]

        # Prepare the processed data
        data = {
            "Tipo": row["Tipo"],
            "Modalidad": row["Modalidad"],
            "Fecha": row["Fecha"],
            "Escuela": escuela,
            "Ciclo": ciclo,
            "Grupo": row["Grupo"],
            "Participantes": participantes
        }

        # Append the processed data to the list
        processed_data.append(data)

    return processed_data
