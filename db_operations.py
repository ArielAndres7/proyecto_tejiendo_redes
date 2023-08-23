import mysql.connector
from mysql.connector import Error

def create_db_connection(host_name, user_name, user_password, db_name):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
            database=db_name
        )
        print("MySQL Database connection successful")
    except Error as err:
        print(f"Error: '{err}'")

    return connection

def to_numeric_or_zero(value):
    # Converts N/a values to 0.0 for decimal fields
    try:
        return float(value)
    except (ValueError, TypeError):
        return 0.0  # Return 0.0 instead of None

def insert_unique_record(table_name, column_name, primary_key_column, value, connection):
    cursor = connection.cursor()
    cursor.execute(f"SELECT {primary_key_column} FROM {table_name} WHERE {column_name} = %s", (value,))
    result = cursor.fetchone()
    if result:
        return result[0]
    else:
        cursor.execute(f"INSERT INTO {table_name} ({column_name}) VALUES (%s)", (value,))
        connection.commit()
        return cursor.lastrowid


def record_exists(connection, escuela_id, grado_id, grupo_id, ciclo_id):
    cursor = connection.cursor()
    cursor.execute("""
        SELECT 1 FROM PerfilesEscolares
        WHERE id_escuela = %s AND id_grado = %s AND id_grupo = %s AND id_ciclo = %s
    """, (escuela_id, grado_id, grupo_id, ciclo_id))
    result = cursor.fetchone()
    return bool(result)

def insert_promedio_total(connection, data):
    cursor = connection.cursor()
    
    # Convert 'N/a' to 0.0
    data = [to_numeric_or_zero(val) for val in data]
    
    cursor.execute("""
        INSERT INTO PromedioTotal (
            autodominio_inicial, automotivacion_inicial, autoconocimiento_inicial, autoestima_inicial, relaciones_interpersonales_inicial,
            autodominio_final, automotivacion_final, autoconocimiento_final, autoestima_final, relaciones_interpersonales_final
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, (
        data[0], data[1], data[2], data[3], data[4],  # initial values
        data[5], data[6], data[7], data[8], data[9]   # final values
    ))
    
    promediototal_id = cursor.lastrowid
    connection.commit()
    cursor.close()
    
    return promediototal_id


def insert_autonomia(connection, data):
    cursor = connection.cursor()

    # Convert 'N/a' to 0.0 for initial and final autonomia
    autonomia_inicial = to_numeric_or_zero(data["initial"])
    autonomia_final = to_numeric_or_zero(data["final"])

    cursor.execute("""
        INSERT INTO Autonomia (
            autonomia_inicial, autonomia_final
        )
        VALUES (%s, %s)
    """, (autonomia_inicial, autonomia_final))

    autonomia_id = cursor.lastrowid
    connection.commit()
    cursor.close()

    return autonomia_id

def process_record(connection, record, promediototal_id, autonomia_id):
    ciclo = record["ciclo"]
    initial_data, final_data = separate_parameters(record)

    # Convert non-numeric values to 0.0
    numeric_fields = ['AUTODOMINIO', 'AUTOMOTIVACION', 'AUTOCONOCIMIENTO', 'AUTOTESTIMA', 'RELACIONES\nINTERPERSONALES']
    initial_data = {k: (to_numeric_or_zero(v) if k in numeric_fields else v) for k, v in initial_data.items()}
    final_data = {k: (to_numeric_or_zero(v) if k in numeric_fields else v) for k, v in final_data.items()}

    cursor = connection.cursor()

    # Insert School, Grade, Group, Ciclo
    escuela_id = insert_unique_record("escuelas", "nombre_escuela", "id_escuela", initial_data["ESCUELA"].strip(), connection)
    grado_id = insert_unique_record("grados", "nivel_grado", "id_grado", initial_data["GRADO"].strip(), connection)
    grupo_id = insert_unique_record("grupos", "nombre_grupo", "id_grupo", initial_data["GRUPO"].strip(), connection)
    ciclo_id = insert_unique_record("ciclos", "rango_anual", "id_ciclo", ciclo, connection)

    # Check if the record exists in PerfilesEscolares
    cursor.execute("""
        SELECT 1 FROM PerfilesEscolares 
        WHERE id_escuela=%s AND id_grado=%s AND id_grupo=%s AND id_ciclo=%s
    """, (escuela_id, grado_id, grupo_id, ciclo_id))
    
    # If no matching record found, then insert
    if not cursor.fetchone():
        cursor.execute("""
            INSERT INTO PerfilesEscolares (
                id_escuela, id_grado, id_grupo, id_ciclo, 
                autodominio_inicial, automotivacion_inicial, autoconocimiento_inicial, autoestima_inicial, relaciones_interpersonales_inicial, 
                autodominio_final, automotivacion_final, autoconocimiento_final, autoestima_final, relaciones_interpersonales_final,
                id_promedio, id_autonomia
            ) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            escuela_id, grado_id, grupo_id, ciclo_id, 
            initial_data["AUTODOMINIO"], initial_data["AUTOMOTIVACION"], initial_data["AUTOCONOCIMIENTO"],
            initial_data["AUTOTESTIMA"], initial_data["RELACIONES\nINTERPERSONALES"],
            final_data["AUTODOMINIO"], final_data["AUTOMOTIVACION"], final_data["AUTOCONOCIMIENTO"],
            final_data["AUTOTESTIMA"], final_data["RELACIONES\nINTERPERSONALES"],
            promediototal_id, autonomia_id
        ))

        connection.commit()
    else:
        print("Duplicate record detected. Not inserting.")

    cursor.close()


def separate_parameters(record):
    initial_params = {}
    final_params = {}
    for key, value in record.items():
        if ".1" in key:
            final_params[key.replace(".1", "")] = value
        else:
            initial_params[key] = value
    return initial_params, final_params

# You might need more functions here later on for other operations.



'''def test_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print("Query executed successfully")
    except Error as err:
        print(f"Error: '{err}'")


def fetch_query_results(connection, query):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as err:
        print(f"Error: '{err}'")'''
