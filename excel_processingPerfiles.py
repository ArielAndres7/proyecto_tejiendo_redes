import pandas as pd
import re

def extract_sheet_info(sheet_name):
    # Extraer el año, tipo de escuela y fase de análisis del nombre de la hoja
    # (esta info en se utiliza de momento, solo identifica la hoja)
    match = re.match(r"(\d+)°([A-Z]+)_([A-Z]+)", sheet_name)
    if match:
        year, school, phase = match.groups()
        return {
            "year": year,
            "school": school,
            "phase": phase
        }
    return {}

def extract_sheet_data(sheet):
    # Extraer las columnas relevantes
    # (En algunas columnas se utiliza el .1 ya que existen celdas repetidas con el mismo nombre)
    columns_to_extract = ["No.", "NOMBRE COMPLETO", "ESCUELA", "GRUPO", "AUTODOMINIO.1", "AUTOMOTIVACION.1", "AUTOCONOCIMIENTO.1", "AUTOESTIMA.1"]
    
    # Verificar si "RELACIONES INTERPERSONALES SANAS" existe y agregar si es así
    # (Inconsistencia de datos, algunas hojas no contienen esta columna)
    if "RELACIONES INTERPERSONALES SANAS.1" in sheet.columns:
        columns_to_extract.append("RELACIONES INTERPERSONALES SANAS.1")

    data = sheet[columns_to_extract].copy()

    # Reemplazar el carácter º con ° (evita errores, datos inconsistentes en el archivo excel)
    data['GRUPO'] = data['GRUPO'].str.replace('º', '°')

    # Procesar el campo 'GRUPO' para dividirlo en 'GRADO' y 'GRUPO'
    data['GRADO'] = data['GRUPO'].str.extract(r'(\d+°)').astype(str)
    data['GRUPO'] = data['GRUPO'].str.extract(r'([A-Z]$)').astype(str)

    # Reordenando las columnas para mover GRADO antes de GRUPO
    columns_ordered = [col for col in data.columns if col != "GRADO"]  # obtener todas las columnas excepto GRADO
    grupoidx = columns_ordered.index('GRUPO')  # encontrar índice de GRUPO
    columns_ordered.insert(grupoidx, 'GRADO')  # insertar GRADO justo antes de GRUPO
    data = data[columns_ordered]

    # Dividir los datos por ocurrencias de 'PROMEDIO'
    promedio_rows = data[data['ESCUELA'] == "PROMEDIO"].index
    data['NOMBRE COMPLETO'].fillna('unknown', inplace=True)
    individual_data_list = []
    promedio_data_list = []

    # Extraer datos entre cada fila 'PROMEDIO'
    start_idx = 0
    for end_idx in promedio_rows:
        individual_data_list.extend(data.iloc[start_idx:end_idx].to_dict(orient='records'))
        promedio_data = data.iloc[end_idx].to_dict()
        promedio_data_list.append(promedio_data)
        start_idx = end_idx + 1

    return {
        "individual_data": individual_data_list,
        "promedio": promedio_data_list
    }

def read_perfil_file(file_path):
    # Cargar la hoja de cálculo
    xls = pd.ExcelFile(file_path)
    
    all_data = {}

    # Analizar el rango requerido
    data_range = xls.parse(usecols='B', nrows=4)

    # Extraer valor de B3 (ciclo)
    raw_b3_value = data_range.iloc[2, 0]

    # Imprimir el valor extraído (prueba)
    #print("B3:", raw_b3_value)

    # Extraer el valor de "CICLO"
    if "CICLO ESCOLAR" in str(raw_b3_value):
        ciclo = raw_b3_value.split("CICLO ESCOLAR")[1].strip()
        print("Ciclo extraído:", ciclo)

    # Procesar la primera hoja
    first_sheet = xls.parse(header=5, usecols='B:N')
    # Encontrar la fila donde aparece 'PROMEDIO TOTAL'
    end_row = first_sheet[first_sheet['ESCUELA'] == 'PROMEDIO TOTAL'].index[0]
    
    # Extraer las filas de datos
    main_data = first_sheet.iloc[:end_row]
    main_data = main_data[main_data.iloc[:, 3:].dropna(how='all').notnull().any(axis=1)]
    
    # Extraer datos de la fila 'PROMEDIO TOTAL'
    promedio_total_data = first_sheet.iloc[end_row, 3:].tolist()
    
    # Extraer datos de la fila 'AUTONOMÍA'
    autonomia_row = end_row + 1
    autonomia_initial = first_sheet.iloc[autonomia_row, 3]
    autonomia_final = first_sheet.iloc[autonomia_row, 8]

    # Convertir los datos en una lista de diccionarios
    data_list = main_data.to_dict(orient='records')
    
    # Almacenar los datos para la primera hoja
    all_data["sheet1"] = {
        "ciclo": ciclo,
        "main_data": data_list,
        "promedio_total": promedio_total_data,
        "autonomia": {
            "initial": autonomia_initial,
            "final": autonomia_final
        },
    }
    
    # Procesar otras hojas
    for sheet_name in xls.sheet_names[1:]:
        sheet_data = xls.parse(sheet_name)
        extracted_data = extract_sheet_data(sheet_data)
        all_data[sheet_name] = {
            "info": extract_sheet_info(sheet_name),
            "data": extracted_data
        }

    return all_data
