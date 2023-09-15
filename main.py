import db_operationsPerfiles as db_opsP
import db_operationsAnalisis as db_opsA
import db_operationsServicios as db_opsS
import db_operationsMapeo as db_opsM
from excel_processingPerfiles import read_perfil_file
from excel_processingAnalisis import read_analisis_file
from excel_processingServicios import read_servicios_file
from excel_processingMapeo import read_mapeo_file
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox

# main.py, aqui se llaman las funciones de los archivos para procesar y luego insertar 
# la informacion en la base de datos. Tambien se contienen las funciones necesarias
# para la GUI de seleccion de archivos.

# Functions
def select_analisis_file():
    filepath = filedialog.askopenfilename(title="Seleccionar archivo de Análisis", filetypes=[('Excel Files', '*.xlsx')])
    analisis_entry.delete(0, tk.END)  # Borrar texto previo
    analisis_entry.insert(0, filepath)  # Insertar la nueva ruta (filepath)

def select_perfil_file():
    filepath = filedialog.askopenfilename(title="Seleccionar archivo de Perfiles", filetypes=[('Excel Files', '*.xlsx')])
    perfil_entry.delete(0, tk.END)
    perfil_entry.insert(0, filepath)

def select_servicios_file():
    filepath = filedialog.askopenfilename(title="Seleccionar archivo de Servicios", filetypes=[('Excel Files', '*.xlsx')])
    servicios_entry.delete(0, tk.END)
    servicios_entry.insert(0, filepath)

def select_mapeo_file():
    filepath = filedialog.askopenfilename(title="Seleccionar archivo de Mapeo", filetypes=[('Excel Files', '*.xlsx')])
    mapeo_entry.delete(0, tk.END)
    mapeo_entry.insert(0, filepath)


def process_files():
    # Aqui se integra la logica para procesar los archivos
    analisis_filepath = analisis_entry.get()
    perfil_filepath = perfil_entry.get()
    servicios_filepath = servicios_entry.get()
    mapeo_filepath = mapeo_entry.get()

    # Verificar si no se selecciona ningun archivo
    if not (analisis_filepath or perfil_filepath or servicios_filepath or mapeo_filepath):
        messagebox.showwarning("No Files", "Selecciona al menos un archivo para procesar.")
        return
    
    # Procesando archivo Perfiles
    if perfil_filepath:

        connection = db_opsP.create_db_connection("127.0.0.1", "root", "admin1234", "test_db_7")

        print("-----DATA PERFIL-----")
        # Extraer data del archivo
        extracted_data = read_perfil_file(perfil_filepath)

        # Print data principal de la primera pagina
        print("Main Data:")

        # Extraer promedio_total y autonomia de la data
        promedio_total_data = extracted_data['sheet1']['promedio_total']
        autonomia_data = extracted_data['sheet1']['autonomia']

        # Insertar promedio_total y autonomia fuera del loop y capturar sus IDs
        promediototal_id = db_opsP.insert_promedio_total(connection, promedio_total_data)
        autonomia_id = db_opsP.insert_autonomia(connection, autonomia_data)

        ciclo_p = extracted_data["sheet1"]["ciclo"]
        for record in extracted_data['sheet1']['main_data']:
            record["ciclo"] = ciclo_p
            db_opsP.process_record(connection, record, promediototal_id, autonomia_id)
            #print(record)

        # Print 'PROMEDIO TOTAL'
        print("\nPROMEDIO TOTAL Data:")
        print(extracted_data['sheet1']['promedio_total'])

        # Print 'AUTONOMÍA'
        print("\nAUTONOMÍA Data:")
        print(f"Initial: {extracted_data['sheet1']['autonomia']['initial']}")
        print(f"Final: {extracted_data['sheet1']['autonomia']['final']}")

        # Print info de pagina y data 
        for sheet_name, data in extracted_data.items():
            if sheet_name != "sheet1":
                #print(f"\nInfo for {sheet_name}:")
                #print(data["info"])
                z = 1 # dummy data
                #print("\nData:")
                
                # Loop de la data individual
                for student_data in data["data"]["individual_data"]:
                    # Se procesa el perfil de cada estudiante para su insercion en la DB
                    db_opsP.insert_student_profile(connection, student_data, ciclo_p)
                    #print(student_data)
                    x = 1 # dummy data
                
                # Print PROMEDIO data por cada grupo en la pagina
                for prom_data in data["data"]["promedio"]:
                    #print('PROMEDIO SEPARADO')
                    #print(prom_data)
                    y = 1 # dummy data

        connection.close()
        print("Perfil Connection closed")
        #pass  
    
    # Procesando archivo Analisis
    if analisis_filepath:

        connection_Analisis = db_opsA.create_db_connection_Analisis("127.0.0.1", "root", "admin1234", "test_db_7")

        # variables
        (
            escuela, 
            ciclo,
            grado, 
            grupo, 
            relationship, 
            tipo_red, 
            num_actores, 
            actores_map, 
            num_relaciones, 
            densidad, 
            diametro, 
            cercania,
            total_comunidades,
            comunidad_cuenta,
            comunidad_tam,
            ge_nombres,
            ge_valores,
            gs_nombres,
            gs_valores,
            prom_grado,
            ayuda_niveles,
            ayuda_porcentajes,
            conf_niveles,
            conf_porcentajes,

        ) = read_analisis_file(analisis_filepath)
            
        # print variables (prueba)
        '''print(
            f'Escuela: {escuela},\n' 
            f'Ciclo: {ciclo},\n'
            f'Grado: {grado},\n'
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
            )'''

        # Inserta data en la tabla Analisis
        analisis_id = db_opsA.insert_analisis(
            connection_Analisis, 
            escuela, ciclo, grado, grupo, num_actores, actores_map, num_relaciones, densidad, diametro, cercania, prom_grado
        )

        # Inserta data en la tabla ModularidadAux
        db_opsA.insert_modularidad(connection_Analisis, analisis_id, total_comunidades, comunidad_cuenta, comunidad_tam)

        # Inserta data en la tabla GradoAux
        db_opsA.insert_grado(connection_Analisis, analisis_id, ge_nombres, ge_valores, gs_nombres, gs_valores)

        # Inserta data en AyudaPercibidaAux y ConfianzaPercibidaAux
        db_opsA.insert_ayuda_confianza(connection_Analisis, analisis_id, ayuda_niveles, ayuda_porcentajes, conf_niveles, conf_porcentajes)
        print('Finished inserting Analisis')

        connection_Analisis.close()
        print("Analisis Connection closed")
        #pass

    # Procesando archivo Servicios
    if servicios_filepath:

        connection_Servicios = db_opsS.create_db_connection_Servicios("127.0.0.1", "root", "admin1234", "test_db_7")

        print("-----DATA SERVICIOS-----")
        data_list = read_servicios_file(servicios_filepath)
        for data in data_list:
            servicio_id = db_opsS.insert_servicio(
                connection_Servicios,
                data['Tipo'],
                data['Modalidad'],
                data['Fecha'],
                data['Escuela'],
                data['Ciclo'],
                data['Grado'],
                data['Grupo'],
                data['Participantes']
            )

        connection_Servicios.close()
        
        print("Servicios Connection closed") # Terminar la conexion con la database

        #pass

    # Procesando archivo Mapeo
    if mapeo_filepath:

        connection_Mapeo = db_opsM.create_db_connection_Mapeo("127.0.0.1", "root", "admin1234", "test_db_7")

        print("-----DATA MAPEO-----")
        mapeo_data = read_mapeo_file(mapeo_filepath)
        
        # mapeo_data se inserta en la base de datos
        for record in mapeo_data:
            db_opsM.insert_mapeo(
                connection_Mapeo,
                record['ID'],            # extra_id
                record['Nombre'],        # estudiante
                record['Escuela'],       # escuela
                record['Ciclo'],         # ciclo
                record['GRADO'],         # grado
                record['Grupo'],         # grupo
                record['GRADO ENTRADA'], # grado_entrada
                record['GRADO SALIDA'],  # grado_salida
                record['CENTRALIDAD'],   # centralidad
                record['PERCEPCIÓN RELACIONAL'],    # percepcion_relacional
                record['PERCEPCIÓN CONDUCTUAL'],    # percepcion_conductual
                record['PERCEPCIÓN ACADÉMICA']      # percepcion_academica
            )

        connection_Mapeo.close()
        print("Mapeo Connection closed")


# GUI
root = tk.Tk()
root.title("Seleccionar Archivos Excel")

# Analisis
tk.Label(root, text="Archivo Análisis:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
analisis_entry = tk.Entry(root, width=50)
analisis_entry.grid(row=0, column=1, padx=10, pady=5)
tk.Button(root, text="Browse", command=select_analisis_file).grid(row=0, column=2, padx=10, pady=5)

# Perfil
tk.Label(root, text="Archivo Perfiles:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
perfil_entry = tk.Entry(root, width=50)
perfil_entry.grid(row=1, column=1, padx=10, pady=5)
tk.Button(root, text="Browse", command=select_perfil_file).grid(row=1, column=2, padx=10, pady=5)

# Servicios
tk.Label(root, text="Archivo Servicios:").grid(row=2, column=0, padx=10, pady=5, sticky="w")
servicios_entry = tk.Entry(root, width=50)
servicios_entry.grid(row=2, column=1, padx=10, pady=5)
tk.Button(root, text="Browse", command=select_servicios_file).grid(row=2, column=2, padx=10, pady=5)

# Mapeo
tk.Label(root, text="Archivo Mapeo:").grid(row=3, column=0, padx=10, pady=5, sticky="w")
mapeo_entry = tk.Entry(root, width=50)
mapeo_entry.grid(row=3, column=1, padx=10, pady=5)
tk.Button(root, text="Browse", command=select_mapeo_file).grid(row=3, column=2, padx=10, pady=5)

# Boton Procesar
tk.Button(root, text="Procesar Archivos", command=process_files).grid(row=4, column=0, columnspan=3, pady=20)

root.mainloop()