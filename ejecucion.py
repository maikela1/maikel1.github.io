from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import mysql.connector
import json
from datetime import datetime, date, timedelta
from decimal import Decimal

# --- Configuración ---
app = Flask(__name__, static_folder='static', static_url_path='/static')
CORS(app)  # Habilita CORS para todas las rutas

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'cafeteria'
}

# --- Función auxiliar para conexión a BD ---
def get_db_connection():
    try:
        conn = mysql.connector.connect(**db_config)
        conn.autocommit = False
        return conn
    except mysql.connector.Error as err:
        print(f"Error de conexión a la BD: {err}")
        return None

# --- Función auxiliar para convertir Decimal a float para JSON ---
def default_serializer(obj):
    if isinstance(obj, Decimal):
        return float(obj)
    raise TypeError(f"Objeto de tipo {type(obj)} no es serializable por JSON")

@app.route('/')
def serve_index():
    return send_from_directory(app.static_folder, 'index.html')


def guardar_cliente(conn, correo, clave):
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO Usuarios (Correo, Clave)
            VALUES (%s, %s)
        """, (correo,clave))
        conn.commit()
        return cursor.lastrowid
    except mysql.connector.Error as e:
        conn.rollback()
        print(f"Error al guardar cliente: {e}")
        return None
    finally:
        cursor.close()

@app.route('/agregar_cliente', methods = ['POST'])
def agregar_cliente_db():
    data = request.get_json()
    correo = data.get('correo')
    clave = data.get('clave')
    if not all([correo, clave]):
        return jsonify("Complete todas las tablas")
    conn = None
    try:
        conn = get_db_connection()
        if conn:
            cliente= guardar_cliente(conn, correo,clave)
            conn.close()
            if cliente:
                return jsonify({'mensaje': 'Guardado exitosamente'}) # Mejor incluir una clave descriptiva
            else:
                return jsonify({'error': 'Error al guardar cliente'}) # Mejor incluir una clave descriptiva
        else:
            return jsonify({'error': 'Error al conectar a la base de datos'}) # Corregí la ortografía
    except Exception as e:
        print(f"Error al conectar o interactuar con la base de datos: {e}")
        return jsonify({'error': f'Ocurrió un error: {str(e)}'}) # Devolvemos un error en JSON
        
            
def agregar_reserva(conn, fecha, hora,mesa,comensales):
    cursor =  conn.cursor()
    try:
        cursor.execute("""
        insert into reservas (Fecha,Horas, Id_mesa,comensales) values(%s,%s,%s,%s)""",
        (fecha,hora, mesa, comensales))
        conn.commit()
        return cursor.lastrowid
    except mysql.connector.Error as e:
        conn.rollback()
        print(f"error :{e}")
        return None
    finally:
        cursor.close()

@app.route('/agregar_reserva', methods=["POST"])
def agregarr_reserba_db():
    data = request.get_json()
    fecha = data.get("Fecha")
    hora = data.get("Hora")
    mesa = data.get("Id_mesa")
    comensales = data.get("comensales")
    if not all([fecha, hora, mesa, comensales]):
        return jsonify({'error': 'Por favor, asegúrese de completar todos los detalles de la reserva.'})  # Retorna un objeto JSON

    conn = None
    try:
        conn = get_db_connection()
        if conn:
            reserva = agregar_reserva(conn, fecha, hora, mesa, comensales)
            conn.close()
            if reserva:
                return jsonify({'guardado': 'Reserva guardada con éxito'})  # Retorna un objeto JSON
            else:
                return jsonify({'error': 'Hubo un problema al guardar la reserva.'})  # Retorna un objeto JSON
        else:
            return jsonify({'error': 'Error al conectar con la base de datos.'})  # Retorna un objeto JSON
    except Exception as e:
        print(f"Error al conectar o interactuar con la base de datos: {e}")
        return jsonify({'error': 'Ocurrió un error inesperado al procesar su reserva.'})  # Retorna un objeto JSON
            

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)