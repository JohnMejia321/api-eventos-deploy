from flask import Flask, request, jsonify
from conexion import db,app  # Importa 'db' desde 'conexion.py'
from modelo import Evento  # Importa el modelo Evento
from sqlalchemy.exc import NoSuchTableError
from datetime import date
from flask_swagger_ui import get_swaggerui_blueprint
import psycopg2


db_uri = "postgresql://postgres:fredy555@localhost/eventos"


##1) Implementar una API con su respectivo Swagger en el lenguaje Python


SWAGGER_URL = '/api/docs'  # La URL donde se servirá la documentación Swagger
API_URL = '/static/swagger.json'  # La URL de la especificación Swagger JSON

# Crea una instancia de SwaggerUI y especifica las rutas
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,  # La URL de Swagger UI
    API_URL,
    config={  # Configuración de Swagger UI
        'app_name': "Mi API"  
    }
)

app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)




db_params = {
    "dbname": "eventos_6z8p",
    "user": "root",
    "password": "3L2F9EfpPtpakyB3hn7gLi64iE1en2gW",
    "host": "dpg-ckthje6nfb1c73d4t1fg-a.oregon-postgres.render.com",
    "port": "5432",
}

# Establecer la conexión a la base de datos
db_connection = psycopg2.connect(**db_params)

# Crear la tabla "evento" si no existe
with db_connection.cursor() as cursor:
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS eventos_6z8p (
            id SERIAL PRIMARY KEY,
            tipo_evento VARCHAR(50),
            descripcion TEXT,
            fecha DATE,
            estado VARCHAR(20),
            campo_adicional_1 VARCHAR(50),
            campo_adicional_2 VARCHAR(50)
        )
    ''')
    
##2.  El código debe generar de manera automática algunos eventos de ejemplo en una base de datos PostgreSQL.
# Agregar registros por defecto si la tabla está vacía
with db_connection.cursor() as cursor:
    cursor.execute('SELECT COUNT(*) FROM eventos_6z8p')
    count = cursor.fetchone()[0]
    if count == 0:
        cursor.execute('''
            INSERT INTO eventos_6z8p (tipo_evento, descripcion, fecha, estado, campo_adicional_1, campo_adicional_2) VALUES
            ('Evento tipo 1', 'Descripción 1', '2023-10-24', 'Revisado', 'Campo 1 Valor', 'Campo 2 Valor'),
            ('Evento tipo 2', 'Descripción 2', '2023-10-25', 'Pendiente', 'Campo 1 Valor', 'Campo 2 Valor'),
            ('Evento tipo 3', 'Descripción 3', '2023-10-26', 'Revisado', 'Campo 1 Valor', 'Campo 2 Valor')
        ''')
    db_connection.commit()






@app.route('/prueba', methods=['GET'])
def listar_eventos():
    with db_connection.cursor() as cursor:
        cursor.execute('SELECT * FROM eventos_6z8p')
        eventos = cursor.fetchall()

    eventos_list = [
        {
            'id': evento[0],
            'tipo_evento': evento[1],
            'descripcion': evento[2],
            'fecha': evento[3].isoformat(),  # Convierte la fecha a formato ISO
            'estado': evento[4],
            'campo_adicional_1': evento[5],
            'campo_adicional_2': evento[6]
        }
        for evento in eventos
    ]

    return jsonify(eventos_list)





# Función para verificar la conexión a la base de datos
def verificar_conexion_db():
    try:
        with db.engine.connect():
            return True
    except Exception as e:
        return str(e)
    
    


# Ruta para verificar la conexión a la base de datos
@app.route('/verificar_conexion_db')
def verificar_conexion():
    resultado = verificar_conexion_db()
    if resultado is True:
        return 'Conexión exitosa a la base de datos PostgreSQL.'
    else:
        return f'Error de conexión a la base de datos: {resultado}'
    
    




# ...

# Ruta para obtener todos los eventos desde la base de datos
@app.route('/events', methods=['GET'])
def get_events():
    try:
        
        with db_connection.cursor() as cursor:
            cursor.execute('SELECT * FROM eventos_6z8p')
            eventos = cursor.fetchall()

        # Convierte los resultados en un formato JSON para la respuesta
        eventos_json = [
            {
                'id': evento[0],
                'tipo_evento': evento[1],
                'descripcion': evento[2],
                'fecha': evento[3].isoformat(),  # Convierte la fecha a formato ISO
                'estado': evento[4],
                'campo_adicional_1': evento[5],
                'campo_adicional_2': evento[6],
            }
            for evento in eventos
        ]


        return jsonify(eventos_json), 200
    except Exception as e:
        return f'Error al obtener eventos desde la base de datos: {str(e)}', 500




@app.route('/events', methods=['POST'])
def create_event():
    try:
        data = request.get_json()
        tipo_evento = data.get('tipo_evento')
        descripcion = data.get('descripcion')
        fecha = data.get('fecha')
        estado = data.get('estado')
        campo_adicional_1 = data.get('campo_adicional_1')
        campo_adicional_2 = data.get('campo_adicional_2')

       

        with db_connection.cursor() as cursor:
            # Insertar el nuevo evento en la base de datos
            cursor.execute('''
                INSERT INTO eventos_6z8p (tipo_evento, descripcion, fecha, estado, campo_adicional_1, campo_adicional_2)
                VALUES (%s, %s, %s, %s, %s, %s)
                RETURNING id
            ''', (tipo_evento, descripcion, fecha, estado, campo_adicional_1, campo_adicional_2))
            nuevo_evento_id = cursor.fetchone()[0]

            # Confirmar la transacción
            db_connection.commit()

        db_connection.close()  # Cierra la conexión

        respuesta = {'mensaje': f'Evento agregado con ID: {nuevo_evento_id}'}
        return jsonify(respuesta), 201
    except Exception as e:
        respuesta = {'mensaje': f'Error al agregar el evento: {str(e)}'}
        return jsonify(respuesta), 500

    
    


@app.route('/events/<int:event_id>', methods=['GET'])
def get_event_by_id(event_id):
    try:
        with db_connection.cursor() as cursor:
            cursor.execute('SELECT * FROM eventos_6z8p WHERE id = %s', (event_id,))
            evento = cursor.fetchone()

        if evento:
            evento_json = {
                'id': evento[0],
                'tipo_evento': evento[1],
                'descripcion': evento[2],
                'fecha': evento[3].isoformat(),
                'estado': evento[4],
                'campo_adicional_1': evento[5],
                'campo_adicional_2': evento[6]
            }
            return jsonify(evento_json), 200
        else:
            return jsonify({'mensaje': 'Evento no encontrado'}), 404
    except Exception as e:
        return jsonify({'mensaje': f'Error al obtener el evento: {str(e)}'}), 500
    



# Ruta para editar un evento por su ID
@app.route('/events/<int:event_id>', methods=['PUT'])
def update_event(event_id):
    try:
        data = request.get_json()
        
        # Verifica si el evento existe
        with db_connection.cursor() as cursor:
            cursor.execute('SELECT COUNT(*) FROM eventos_6z8p WHERE id = %s', (event_id,))
            count = cursor.fetchone()[0]
            if count == 0:
                return jsonify({'mensaje': 'Evento no encontrado'}), 404
        
        # Actualiza el evento
        with db_connection.cursor() as cursor:
            cursor.execute('''
                UPDATE eventos_6z8p
                SET tipo_evento = %s, descripcion = %s, fecha = %s, estado = %s, campo_adicional_1 = %s, campo_adicional_2 = %s
                WHERE id = %s
            ''', (data.get('tipo_evento'), data.get('descripcion'), data.get('fecha'), data.get('estado'), data.get('campo_adicional_1'), data.get('campo_adicional_2'), event_id))

        db_connection.commit()

        respuesta = {'mensaje': 'Evento actualizado exitosamente'}
        return jsonify(respuesta), 200
    except Exception as e:
        respuesta = {'mensaje': f'Error al editar el evento: {str(e)}'}
        return jsonify(respuesta), 500


# Ruta para eliminar un evento por su ID
@app.route('/events/<int:event_id>', methods=['DELETE'])
def delete_event(event_id):
    try:
        # Verifica si el evento existe
        with db_connection.cursor() as cursor:
            cursor.execute('SELECT COUNT(*) FROM eventos_6z8p WHERE id = %s', (event_id,))
            count = cursor.fetchone()[0]
            if count == 0:
                return jsonify({'mensaje': 'Evento no encontrado'}), 404
        
        # Elimina el evento
        with db_connection.cursor() as cursor:
            cursor.execute('DELETE FROM eventos_6z8p WHERE id = %s', (event_id,))
        
        db_connection.commit()

        respuesta = {'mensaje': 'Evento eliminado exitosamente'}
        return jsonify(respuesta)
    except Exception as e:
        respuesta = {'mensaje': f'Error al eliminar el evento: {str(e)}'}
        return jsonify(respuesta), 500


if __name__ == '__main__':
    app.run(debug=True)
