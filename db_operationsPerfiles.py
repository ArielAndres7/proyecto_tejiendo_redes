import mysql.connector
from mysql.connector import Error
import unicodedata


# ARCHIVO PERFILES DE AUTONOMIA, SOLO PAGINA 1

def create_db_connection(host_name, user_name, user_password, db_name):
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

def to_numeric_or_zero(value):
    # Convierte los valores N/a a 0.0 para campos decimales
    try:
        return float(value)
    except (ValueError, TypeError):
        return 0.0  # Devuelve 0.0 en lugar de None

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
    
    # Convierte 'N/a' a 0.0
    data = [to_numeric_or_zero(val) for val in data]
    
    cursor.execute("""
        INSERT INTO PromedioTotal (
            autodominio_inicial, automotivacion_inicial, autoconocimiento_inicial, autoestima_inicial, relaciones_interpersonales_inicial,
            autodominio_final, automotivacion_final, autoconocimiento_final, autoestima_final, relaciones_interpersonales_final
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, (
        data[0], data[1], data[2], data[3], data[4],  # valores iniciales
        data[5], data[6], data[7], data[8], data[9]   # valores finales
    ))
    
    promediototal_id = cursor.lastrowid
    connection.commit()
    cursor.close()
    
    return promediototal_id

def insert_autonomia(connection, data):
    cursor = connection.cursor()

    # Convierte 'N/a' a 0.0 para autonomía inicial y final
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

    # Convierte valores no numéricos a 0.0
    numeric_fields = ['AUTODOMINIO', 'AUTOMOTIVACION', 'AUTOCONOCIMIENTO', 'AUTOTESTIMA', 'RELACIONES\nINTERPERSONALES']
    initial_data = {k: (to_numeric_or_zero(v) if k in numeric_fields else v) for k, v in initial_data.items()}
    final_data = {k: (to_numeric_or_zero(v) if k in numeric_fields else v) for k, v in final_data.items()}

    cursor = connection.cursor()

    # Inserta Escuela, Grado, Grupo, Ciclo
    escuela_id = insert_unique_record("escuelas", "nombre_escuela", "id_escuela", initial_data["ESCUELA"].strip(), connection)
    grado_id = insert_unique_record("grados", "nivel_grado", "id_grado", initial_data["GRADO"].strip(), connection)
    grupo_id = insert_unique_record("grupos", "nombre_grupo", "id_grupo", initial_data["GRUPO"].strip(), connection)
    ciclo_id = insert_unique_record("ciclos", "rango_anual", "id_ciclo", ciclo, connection)

    # Verifica si el registro existe en PerfilesEscolares
    cursor.execute("""
        SELECT 1 FROM PerfilesEscolares 
        WHERE id_escuela=%s AND id_grado=%s AND id_grupo=%s AND id_ciclo=%s
    """, (escuela_id, grado_id, grupo_id, ciclo_id))
    
    # Si no se encuentra un registro coincidente, entonces inserta
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
        # Se intenta detectar data duplicada, si es el caso no se inserta
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









# ARCHIVO PERFILES DE AUTONOMIA, PAGINAS 2 EN ADELANTE

def create_canonical_name(name):
    """
    Crea un nombre canónico a partir del nombre dado.
    Este nombre no tiene espacios, está en letras mayúsculas y no tiene tildes.
    """
    # Convierte el nombre a cadena en caso de que no lo sea ya
    name = str(name)

    # Normaliza el nombre para eliminar tildes o diacríticos y convertirlo a mayúsculas
    name = unicodedata.normalize('NFKD', name).encode('ASCII', 'ignore').decode('ASCII').upper()
    # Elimina espacios
    name = name.replace(" ", "")
    return name


def get_or_insert_school(connection, school_name):
    """
    Verifica si la escuela ya existe. Si no, inserta y devuelve el nuevo id.
    """
    cursor = connection.cursor()
    query = "SELECT id_escuela FROM Escuelas WHERE nombre_escuela = %s"
    cursor.execute(query, (school_name,))
    result = cursor.fetchone()
    
    if result:
        return result[0]  # Devuelve el id de la escuela
    else:
        insert_query = "INSERT INTO Escuelas (nombre_escuela) VALUES (%s)"
        cursor.execute(insert_query, (school_name,))
        connection.commit()
        return cursor.lastrowid  # Devuelve el id de la escuela insertada

def get_or_insert_student(connection, student_name, school_id, ciclo_id, grado_id, grupo_id):
    """
    Verifica si el estudiante ya existe basándose en el nombre canónico y la información de la escuela. Si no, inserta y devuelve el nuevo id.
    """
    canonical_name = create_canonical_name(student_name)

    cursor = connection.cursor()
    query = ("SELECT id_estudiante FROM Estudiantes WHERE nombre_canonico = %s "
             "AND id_escuela = %s AND id_ciclo = %s AND id_grado = %s AND id_grupo = %s")
    cursor.execute(query, (canonical_name, school_id, ciclo_id, grado_id, grupo_id))
    result = cursor.fetchone()
    
    if result:
        return result[0]
    else:
        insert_query = ("INSERT INTO Estudiantes (nombre_completo, nombre_canonico, id_escuela, id_ciclo, "
                        "id_grado, id_grupo) VALUES (%s, %s, %s, %s, %s, %s)")
        cursor.execute(insert_query, (student_name, canonical_name, school_id, ciclo_id, grado_id, grupo_id))
        connection.commit()
        return cursor.lastrowid

def insert_student_profile(connection, student_data, ciclo):
    # Paso 1: Verificar o insertar escuela, grado, grupo...
    school_id = get_or_insert_school(connection, student_data['ESCUELA'])
    ciclo_id = get_ciclo_id(connection, ciclo)
    grado_id = get_or_insert_grade(connection, student_data['GRADO'])
    grupo_id = get_or_insert_group(connection, student_data['GRUPO'])

    # Paso 2: Verificar o insertar al estudiante
    student_id = get_or_insert_student(connection, student_data['NOMBRE COMPLETO'], school_id, ciclo_id, grado_id, grupo_id)

    # Paso 3: Insertar los datos del perfil del estudiante
    cursor = connection.cursor()
    insert_query = ("INSERT INTO PerfilesEstudiantiles (id_estudiante, autodominio, automotivacion, autoconocimiento, autoestima) "
                    "VALUES (%s, %s, %s, %s, %s)")
    cursor.execute(insert_query, (student_id, student_data['AUTODOMINIO.1'], student_data['AUTOMOTIVACION.1'], 
                                  student_data['AUTOCONOCIMIENTO.1'], student_data['AUTOESTIMA.1']))
    connection.commit()

def get_ciclo_id(connection, ciclo):
    """Obtiene el ID para un ciclo dado."""
    try:
        with connection.cursor() as cursor:
            # Consulta la tabla Ciclos
            query = "SELECT id_ciclo FROM Ciclos WHERE rango_anual = %s"
            cursor.execute(query, (ciclo,))
            
            # Obtiene el resultado
            result = cursor.fetchone()
            if result:
                return result[0]
            else:
                # Si no se encuentra una entrada para el ciclo, se lanza una excepción o se maneja este escenario según su requerimiento
                raise ValueError(f"No se encontró una entrada para el ciclo: {ciclo}")

    except Exception as e:
        print(f"Error al obtener el ID del ciclo: {e}")
        return None


def get_or_insert_grade(connection, grado):
    """Obtiene el ID para un grado dado o lo inserta si no existe."""
    try:
        with connection.cursor() as cursor:
            # Consulta para obtener el grado
            query = "SELECT id_grado FROM Grados WHERE nivel_grado = %s"
            cursor.execute(query, (grado,))
            result = cursor.fetchone()
            if result:
                return result[0]
            else:
                # Si no se encuentra una entrada para el grado, insértalo
                insert_query = "INSERT INTO Grados (grado) VALUES (%s)"
                cursor.execute(insert_query, (grado,))
                connection.commit()
                return cursor.lastrowid  # Devuelve el ID del grado recién insertado

    except Exception as e:
        print(f"Error al manejar el grado {grado}: {e}")
        return None

def get_or_insert_group(connection, grupo):
    """Obtiene el ID para un grupo dado o lo inserta si no existe."""
    try:
        with connection.cursor() as cursor:
            # Consulta para obtener el grupo
            query = "SELECT id_grupo FROM Grupos WHERE nombre_grupo = %s"
            cursor.execute(query, (grupo,))
            result = cursor.fetchone()
            if result:
                return result[0]
            else:
                # Si no se encuentra una entrada para el grupo, insértalo
                insert_query = "INSERT INTO Grupos (grupo) VALUES (%s)"
                cursor.execute(insert_query, (grupo,))
                connection.commit()
                return cursor.lastrowid  # Devuelve el ID del grupo recién insertado

    except Exception as e:
        print(f"Error al manejar el grupo {grupo}: {e}")
        return None
