import psycopg2

# Datos de conexión
db_params = {
    "dbname": "eventos_6z8p",
    "user": "root",
    "password": "3L2F9EfpPtpakyB3hn7gLi64iE1en2gW",
    "host": "dpg-ckthje6nfb1c73d4t1fg-a.oregon-postgres.render.com",
    "port": "5432",
}

try:
    # Establece la conexión a la base de datos
    connection = psycopg2.connect(**db_params)

    # Crea un cursor
    cursor = connection.cursor()

    # Ejecuta una consulta de prueba
    cursor.execute("SELECT 'Conexión exitosa'")

    # Recupera el resultado
    resultado = cursor.fetchone()

    print(resultado[0])  # Deberías ver "Conexión exitosa"

    # Cierra el cursor y la conexión
    cursor.close()
    connection.close()

except Exception as error:
    print(f"Error de conexión: {error}")
