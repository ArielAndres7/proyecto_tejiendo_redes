import mysql.connector
from mysql.connector import Error
import unicodedata

def create_db_connection_Analisis(host_name, user_name, user_password, db_name):
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


def insert_analisis(connection, escuela, ciclo, grado, grupo, num_actores, actores_map, num_relaciones, densidad, diametro, cercania, prom_grado):
    # Recuperar o insertar IDs para los valores con foreign key
    escuela_id = get_or_insert_id(connection, 'Escuelas', 'nombre_escuela', escuela, primary_key='id_escuela') 
    ciclo_id = get_or_insert_id(connection, 'Ciclos', 'rango_anual', ciclo, primary_key='id_ciclo') 
    grado_id = get_or_insert_id(connection, 'Grados', 'nivel_grado', grado, primary_key='id_grado')
    grupo_id = get_or_insert_id(connection, 'Grupos', 'nombre_grupo', grupo, primary_key='id_grupo')

    cursor = connection.cursor()

    query = """
    INSERT INTO Analisis (fecha, id_escuela, id_ciclo, id_grado, id_grupo, num_total_actores, actores_mapeados, num_relaciones, densidad, diametro, cercania, promedio_grado)
    VALUES (NOW(), %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    values = (escuela_id, ciclo_id, grado_id, grupo_id, num_actores, actores_map, num_relaciones, densidad, diametro, cercania, prom_grado)
    cursor.execute(query, values)
    connection.commit()

    last_id = cursor.lastrowid
    cursor.close()

    return last_id


def insert_modularidad(connection, id_analisis, total_comunidades, comunidad_cuenta, comunidad_tam):
    cursor = connection.cursor()

    for cuenta, tam in zip(comunidad_cuenta, comunidad_tam):
        query = """
        INSERT INTO ModularidadAux (id_analisis, total_comunidades, comunidad_cuenta, comunidad_tam)
        VALUES (%s, %s, %s, %s)
        """
        values = (id_analisis, total_comunidades, cuenta, tam)
        cursor.execute(query, values)

    connection.commit()
    cursor.close()


def insert_grado(connection, id_analisis, ge_nombres, ge_valores, gs_nombres, gs_valores):
    cursor = connection.cursor()

    for name_e, value_e, name_s, value_s in zip(ge_nombres, ge_valores, gs_nombres, gs_valores):
        query = """
        INSERT INTO GradoAux (id_analisis, nombre_entrada, grado_entrada, nombre_salida, grado_salida)
        VALUES (%s, %s, %s, %s, %s)
        """
        values = (id_analisis, name_e, value_e, name_s, value_s)
        cursor.execute(query, values)

    connection.commit()
    cursor.close()


def insert_ayuda_confianza(connection, id_analisis, ayuda_niveles, ayuda_porcentajes, conf_niveles, conf_porcentajes):
    cursor = connection.cursor()

    for level, percentage in zip(ayuda_niveles, ayuda_porcentajes):
        query = """
        INSERT INTO AyudaPercibidaAux (id_analisis, valor, porcentaje)
        VALUES (%s, %s, %s)
        """
        values = (id_analisis, level, percentage)
        cursor.execute(query, values)

    for level, percentage in zip(conf_niveles, conf_porcentajes):
        query = """
        INSERT INTO ConfianzaPercibidaAux (id_analisis, valor, porcentaje)
        VALUES (%s, %s, %s)
        """
        values = (id_analisis, level, percentage)
        cursor.execute(query, values)

    connection.commit()
    cursor.close()
