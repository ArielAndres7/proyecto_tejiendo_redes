import mysql.connector
from mysql.connector import Error
import unicodedata

def create_db_connection_Servicios(host_name, user_name, user_password, db_name):
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

def get_or_insert_id(connection, table_name, column_name, value, primary_key='id'):
    cursor = connection.cursor()

    # Verifica si el valor existe
    query_check = f"SELECT {primary_key} FROM {table_name} WHERE {column_name} = %s"
    cursor.execute(query_check, (value,))
    result = cursor.fetchone()

    # Si el valor existe, devuelve su ID
    if result:
        cursor.close()
        return result[0]
    
    # Si el valor no existe, inserta y devuelve su ID
    query_insert = f"INSERT INTO {table_name} ({column_name}) VALUES (%s)"
    cursor.execute(query_insert, (value,))
    connection.commit()
    last_id = cursor.lastrowid
    cursor.close()

    return last_id

def convert_to_canonical(name):
    name = unicodedata.normalize('NFKD', name).encode('ASCII', 'ignore').decode('utf-8')
    canonical_name = ''.join(e for e in name if e.isalnum()).upper()
    return canonical_name

def insert_or_get_student_id(connection, student_name, escuela_id, ciclo_id, grado_id, grupo_id):
    cursor = connection.cursor()

    canonical_name = convert_to_canonical(student_name)
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
        cursor.execute(query_insert, (student_name, canonical_name, escuela_id, ciclo_id, grado_id, grupo_id))
        connection.commit()
        return cursor.lastrowid

def insert_servicio(connection, tipo, modalidad, fecha, escuela, ciclo, grado, grupo, participantes):
    cursor = connection.cursor()

    # Obtener o insertar las foreign keys
    escuela_id = get_or_insert_id(connection, 'Escuelas', 'nombre_escuela', escuela, primary_key='id_escuela')
    ciclo_id = get_or_insert_id(connection, 'Ciclos', 'rango_anual', ciclo, primary_key='id_ciclo')
    grado_id = get_or_insert_id(connection, 'Grados', 'nivel_grado', grado, primary_key='id_grado')
    grupo_id = get_or_insert_id(connection, 'Grupos', 'nombre_grupo', grupo, primary_key='id_grupo')

    # Insertar en Servicios
    query = """
    INSERT INTO Servicios (tipo, modalidad, fecha, id_escuela, id_ciclo, id_grado, id_grupo)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    values = (tipo, modalidad, fecha, escuela_id, ciclo_id, grado_id, grupo_id)
    cursor.execute(query, values)
    connection.commit()

    servicio_id = cursor.lastrowid

    # Enlazar estudiantes al servicio
    for student_name in participantes:
        estudiante_id = insert_or_get_student_id(connection, student_name, escuela_id, ciclo_id, grado_id, grupo_id)
        query_link = """
            INSERT INTO ServicioEstudiantes (id_servicio, id_estudiante) 
            VALUES (%s, %s)
        """
        cursor.execute(query_link, (servicio_id, estudiante_id))
        connection.commit()

    cursor.close()

    return servicio_id
