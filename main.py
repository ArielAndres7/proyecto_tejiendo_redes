import db_operations as db_ops
from excel_processing import read_excel_file
from excel_processing2 import read_perfil_file
from excel_processing3 import read_servicios_file
import tkinter as tk
from tkinter import filedialog


'''def select_file():
    file_path = filedialog.askopenfilename()
    # You can now pass this file_path to your read functions
    print("Selected File:", file_path)

# Create the main window
root = tk.Tk()
root.title("Data Mining Tool")

# Create and pack a button onto the window
btn = tk.Button(root, text="Select File", command=select_file)
btn.pack(pady=20)

root.mainloop()'''

# Establish a connection to the database
connection = db_ops.create_db_connection("127.0.0.1", "root", "admin1234", "test_db_5")

(
    escuela, 
    ciclo, 
    grupo, 
    relationship, 
    tipo_red, 
    num_actores, 
    actores_map, 
    num_relaciones, 
    densidad, 
    diametro, 
    cercania,
    ge_nombres,
    ge_valores,
    gs_nombres,
    gs_valores,
    prom_grado,
    ayuda_niveles,
    ayuda_porcentajes,
    conf_niveles,
    conf_porcentajes,
    total_comunidades,
    comunidad_cuenta,
    comunidad_tam
) = read_excel_file('analisis.xlsx')
    
# print variables
print(
    f'Escuela: {escuela},\n' 
    f'Ciclo: {ciclo},\n'
    f'Grupo: {grupo},\n'
    f'Relacion: {relationship},\n'
    f'Tipo de red: {tipo_red},\n'
    f'Numero de actores: {num_actores}\n'
    f'Actores mapeados: {actores_map}\n'
    f'Numero de relaciones: {num_relaciones}\n'
    f'Densidad: {densidad}\n' 
    f'Diametro: {diametro}\n' 
    f'Cercania: {cercania}\n' 
    f'Modularidad (Total comunidades): {total_comunidades}\n' 
    f'Modularidad (Com. cuenta): {comunidad_cuenta}\n' 
    f'Modularidad (Com. tamaño): {comunidad_tam}\n' 
    f'Grado entrada (nombres): {ge_nombres}\n' 
    f'Grado entrada (valores): {ge_valores}\n' 
    f'Grado salida (nombres): {gs_nombres}\n' 
    f'Grado salida (valores): {gs_valores}\n' 
    f'Promedio grado: {prom_grado}\n' 
    f'Ayuda percibida (niveles): {ayuda_niveles}\n' 
    f'Ayuda percibida (porcentajes): {ayuda_porcentajes}\n' 
    f'Confianza percibida (niveles): {conf_niveles}\n' 
    f'Confianza percibida (porcentajes): {conf_porcentajes}\n' 
    )

print("-----DATA PERFIL-----")
# Extract data from the Excel file

extracted_data = read_perfil_file('perfil.xlsx')

# Print the main data from the first sheet
print("Main Data:")

# Extract promedio_total and autonomia from the data.
promedio_total_data = extracted_data['sheet1']['promedio_total']
autonomia_data = extracted_data['sheet1']['autonomia']

# Insert promedio_total and autonomia outside the loop and capture their respective IDs.
promediototal_id = db_ops.insert_promedio_total(connection, promedio_total_data)
autonomia_id = db_ops.insert_autonomia(connection, autonomia_data)

ciclo = extracted_data["sheet1"]["ciclo"]
for record in extracted_data['sheet1']['main_data']:
    record["ciclo"] = ciclo
    db_ops.process_record(connection, record, promediototal_id, autonomia_id)
    print(record)

# Print the 'PROMEDIO TOTAL' data
print("\nPROMEDIO TOTAL Data:")
print(extracted_data['sheet1']['promedio_total'])

# Print the 'AUTONOMÍA' data
print("\nAUTONOMÍA Data:")
print(f"Initial: {extracted_data['sheet1']['autonomia']['initial']}")
print(f"Final: {extracted_data['sheet1']['autonomia']['final']}")

# Print the sheet info and data for the other sheets
'''for sheet_name, data in extracted_data.items():
    if sheet_name != "sheet1":
        print(f"\nInfo for {sheet_name}:")
        print(data["info"])
        
        # Print the extracted data for the sheet
        print("\nData for the sheet:")
        
        # Loop through individual data
        for student_data in data["data"]["individual_data"]:
            print(student_data)
        
        # Print the PROMEDIO data for each group in the sheet
        for prom_data in data["data"]["promedio"]:
            print(prom_data)'''


print("-----DATA SERVICIOS-----")
data_list = read_servicios_file('servicios.xlsx')
for data in data_list:
    print(data)
# QUERIES 

'''insert_query = """
INSERT INTO Estudiantes (PrimerNombre, PrimerApellido) VALUES ('PruebaNombre', 'PruebaApellido');
"""
db_ops.test_query(connection, insert_query)'''

# FETCH
'''select_query = "SELECT * FROM Estudiantes;"
results = db_ops.fetch_query_results(connection, select_query)
for result in results:
    print(result)

connection.close()
print("Connection closed")'''