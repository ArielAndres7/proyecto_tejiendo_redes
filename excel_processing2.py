import pandas as pd
import re

def extract_sheet_info(sheet_name):
    # Extract year, school type, and analysis phase from the sheet name
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
    # Extracting the relevant columns
    #print(sheet.columns)
    columns_to_extract = ["No.", "NOMBRE COMPLETO", "ESCUELA", "GRUPO", "AUTODOMINIO.1", "AUTOMOTIVACION.1", "AUTOCONOCIMIENTO.1", "AUTOESTIMA.1"]
    
    # Check for "RELACIONES INTERPERSONALES SANAS" and add if it exists
    if "RELACIONES INTERPERSONALES SANAS.1" in sheet.columns:
        columns_to_extract.append("RELACIONES INTERPERSONALES SANAS.1")

    data = sheet[columns_to_extract]
    print(data.head())
    input("Press Enter to continue...")

    # Splitting the data by 'PROMEDIO' occurrences
    promedio_rows = data[data['ESCUELA'] == "PROMEDIO"].index
    individual_data_list = []
    promedio_data_list = []

    # Extracting data between each 'PROMEDIO' row
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
    # Load the spreadsheet
    xls = pd.ExcelFile(file_path)
    
    all_data = {}

    # Parse the required range
    data_range = xls.parse(usecols='B', nrows=4)

    # Extract value from B3
    raw_b3_value = data_range.iloc[2, 0]

    # Print the extracted value
    print("B3:", raw_b3_value)

    # Extract the "CICLO" value
    if "CICLO ESCOLAR" in str(raw_b3_value):
        ciclo = raw_b3_value.split("CICLO ESCOLAR")[1].strip()
        print("Extracted ciclo:", ciclo)

    # Handle the first sheet
    first_sheet = xls.parse(header=5, usecols='B:N')
        # Find the row where 'PROMEDIO TOTAL' appears
    end_row = first_sheet[first_sheet['ESCUELA'] == 'PROMEDIO TOTAL'].index[0]
    
    # Extract the main rows of data
    main_data = first_sheet.iloc[:end_row]
    main_data = main_data[main_data.iloc[:, 3:].dropna(how='all').notnull().any(axis=1)]
    
    # Extract 'PROMEDIO TOTAL' row data
    promedio_total_data = first_sheet.iloc[end_row, 3:].tolist()
    
    # Extract 'AUTONOMÍA' row data
    autonomia_row = end_row + 1
    autonomia_initial = first_sheet.iloc[autonomia_row, 3]
    autonomia_final = first_sheet.iloc[autonomia_row, 8]

    # Convert the main data to a list of dictionaries
    data_list = main_data.to_dict(orient='records')
    
    # Store the data for the first sheet
    all_data["sheet1"] = {
        "ciclo": ciclo,
        "main_data": data_list,
        "promedio_total": promedio_total_data,
        "autonomia": {
            "initial": autonomia_initial,
            "final": autonomia_final
        },
    }
    
    # Process other sheets
    for sheet_name in xls.sheet_names[1:]:
        sheet_data = xls.parse(sheet_name)
        extracted_data = extract_sheet_data(sheet_data)
        all_data[sheet_name] = {
            "info": extract_sheet_info(sheet_name),
            "data": extracted_data
        }

    return all_data