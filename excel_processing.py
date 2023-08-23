import pandas as pd
import re

def read_excel_file(file_path):
    # Cargar archivo excel
    xls = pd.read_excel(file_path, header=None)
    
    # ESCUELA Y CICLO
    escuela_y_ciclo = xls.iat[1, 1]
    # Separar escuela y ciclo
    escuela, ciclo = escuela_y_ciclo.split()

    # GRUPO
    grupo = xls.iat[2, 1]

    # RELACION Y TIPO DE RED
    relacion_y_tipo_red = xls.iat[4, 1]
    # Separar relacion y tipo de red
    relacion, tipo_red = relacion_y_tipo_red.split(", ")

    # NUMERO DE ACTORES
    num_actores = xls.iat[5, 1]

    # ACTORES MAPEADOS
    actores_map = xls.iat[6, 1]

    # NUMERO DE RELACIONES
    num_relaciones = xls.iat[7, 1]

    # DENSIDAD
    densidad = xls.iat[8, 1]

    # DIAMETRO
    diametro = xls.iat[9, 1]

    # CERCANIA
    cercania = xls.iat[10, 1]

    #MODULARIDAD
    modularidad_texto = xls.iat[11, 1]
    total_pattern = r"Se detectan (\d+) comunidades"
    total_comunidades = int(re.search(total_pattern, modularidad_texto).group(1))
    detail_pattern = r"(\d+) comunidades de (\d+) miembros"
    matches = re.findall(detail_pattern, modularidad_texto)
    comunidad_cuenta = [int(m[0]) for m in matches]
    comunidad_tam = [int(m[1]) for m in matches]

    #GRADO ENTRADA
    grado_entrada_texto = xls.iat[12, 1]

    ge_nombres = []
    ge_valores = []

    for line in grado_entrada_texto.split("\n"):
        # Use a regular expression to look for lines that contain a name and score
        match = re.match(r"(\w+)\s+(\d+)", line.strip())
    
        # If a match was found, add the name and score to the respective lists
        if match:
            name, score = match.groups()
            ge_nombres.append(name)
            ge_valores.append(int(score))

    #GRADO SALIDA
    grado_salida_texto = xls.iat[13, 1]

    # Initialize lists to hold students' names and scores for exit degree
    gs_nombres = []
    gs_valores = []
    
    # Split the text into lines and iterate over each line
    for line in grado_salida_texto.split("\n"):
        # Use a regular expression to look for lines that contain a name and score
        match = re.match(r"(\w+)\s+(\d+)", line.strip())
        
        # If a match was found, add the name and score to the respective lists
        if match:
            name, score = match.groups()
            gs_nombres.append(name)
            gs_valores.append(int(score))

    prom_grado = xls.iat[14, 1]

    #AYUDA PERCIBIDA
    ayuda_perc_texto = xls.iat[15, 1]
    pattern = r"(\d+) - \(([\d.]+)%\)"
    matches = re.findall(pattern, ayuda_perc_texto)
    ayuda_niveles = [int(m[0]) for m in matches]
    ayuda_porcentajes = [float(m[1]) for m in matches]

    #CONFIANZA PERCIBIDA
    conf_perc_texto = xls.iat[16, 1]
    pattern = r"(\d+) - \(([\d.]+)%\)"
    matches = re.findall(pattern, conf_perc_texto)
    conf_niveles = [int(m[0]) for m in matches]
    conf_porcentajes = [float(m[1]) for m in matches]
    
    return (
        escuela, 
        ciclo, 
        grupo, 
        relacion, 
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
        conf_porcentajes
    )
