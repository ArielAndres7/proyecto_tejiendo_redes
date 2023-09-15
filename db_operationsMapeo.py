import mysql.connector
from mysql.connector import Error
import unicodedata

def create_db_connection_Mapeo(host_name, user_name, user_password, db_name):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
            database=db_name
        )
        print("Conexión exitosa a la base de datos MySQL")
    except Error as err:
        print(f"Error: '{err}'")

    return connection

def convert_to_canonical(name):
    name = unicodedata.normalize('NFKD', name).encode('ASCII', 'ignore').decode('utf-8')
    canonical_name = ''.join(e for e in name if e.isalnum()).upper()
    return canonical_name

def get_or_insert_id(connection, table_name, column_name, value, primary_key='id'):
    cursor = connection.cursor()

    # Verificar si el valor existe
    query_check = f"SELECT {primary_key} FROM {table_name} WHERE {column_name} = %s"
    cursor.execute(query_check, (value,))
    result = cursor.fetchone()

    # Si el valor existe, retornar su ID
    if result:
        cursor.close()
        return result[0]
    
    # Si el valor no existe, insertar y retornar su ID
    query_insert = f"INSERT INTO {table_name} ({column_name}) VALUES (%s)"
    cursor.execute(query_insert, (value,))
    connection.commit()
    last_id = cursor.lastrowid
    cursor.close()

    return last_id

def insert_or_get_estudiante_id(connection, estudiante_name, escuela_id, ciclo_id, grado_id, grupo_id):
    cursor = connection.cursor()

    canonical_name = convert_to_canonical(estudiante_name)
    query_check = """
        SELECT id_estudiante 
        FROM Estudiantes 
        WHERE nombre_canonico = %s AND id_escuela = %s AND id_ciclo = %s AND id_grado = %s AND id_grupo = %s
    """
    cursor.execute(query_check, (canonical_name, escuela_id, ciclo_id, grado_id, grupo_id))
    result = cursor.fetchone()

    if result:
        return result[0]
    else:
        query_insert = """
            INSERT INTO Estudiantes (nombre_completo, nombre_canonico, id_escuela, id_ciclo, id_grado, id_grupo) 
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query_insert, (estudiante_name, canonical_name, escuela_id, ciclo_id, grado_id, grupo_id))
        connection.commit()
        return cursor.lastrowid

def insert_mapeo(connection, extra_id, estudiante, escuela, ciclo, grado, grupo, grado_entrada, grado_salida, centralidad, percepcion_relacional, percepcion_conductual, percepcion_academica):
    # Obtener o insertar IDs para los valores de las foreign keys
    escuela_id = get_or_insert_id(connection, 'Escuelas', 'nombre_escuela', escuela, primary_key='id_escuela')
    ciclo_id = get_or_insert_id(connection, 'Ciclos', 'rango_anual', ciclo, primary_key='id_ciclo')
    grado_id = get_or_insert_id(connection, 'Grados', 'nivel_grado', grado, primary_key='id_grado')
    grupo_id = get_or_insert_id(connection, 'Grupos', 'nombre_grupo', grupo, primary_key='id_grupo')

    estudiante_id = insert_or_get_estudiante_id(connection, estudiante, escuela_id, ciclo_id, grado_id, grupo_id)

    cursor = connection.cursor()

    query = """
    INSERT INTO EstudiantesMapeo (extra_id, id_estudiante, id_escuela, id_ciclo, id_grado, id_grupo, grado_entrada, grado_salida, centralidad, percepcion_relacional, percepcion_conductual, percepcion_academica)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    values = (extra_id, estudiante_id, escuela_id, ciclo_id, grado_id, grupo_id, grado_entrada, grado_salida, centralidad, percepcion_relacional, percepcion_conductual, percepcion_academica)
    cursor.execute(query, values)
    connection.commit()

    last_id = cursor.lastrowid
    cursor.close()

    return last_id
