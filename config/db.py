# config/db.py
from flask_mysqldb import MySQL
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Crear instancia de MySQL
mysql = MySQL()

def init_db(app):
    """Configura y inicializa MySQL para la aplicación Flask"""
    # Obtener configuraciones desde variables de entorno
    db_host = os.getenv('DB_HOST', 'localhost')
    db_user = os.getenv('DB_USER', 'maureen')
    db_password = os.getenv('DB_PASSWORD', 'Luna2024')
    db_name = os.getenv('DB_NAME', 'appTareas')
    db_port = int(os.getenv('DB_PORT', 3306))
    
    # Configurar la aplicación Flask
    app.config['MYSQL_HOST'] = db_host
    app.config['MYSQL_USER'] = db_user
    app.config['MYSQL_PASSWORD'] = db_password
    app.config['MYSQL_DB'] = db_name
    app.config['MYSQL_PORT'] = db_port
    app.config['MYSQL_CURSORCLASS'] = 'DictCursor'  # Para obtener resultados como diccionarios
    app.config['MYSQL_CHARSET'] = 'utf8mb4'
    
    # Mensaje de debug (opcional)
    print("✅ Configuración de Base de Datos cargada correctamente")
    print(f"   Base de datos: {db_name}")
    print(f"   Usuario: {db_user}")
    print(f"   Host: {db_host}:{db_port}")
    
    # Inicializar MySQL con la aplicación
    mysql.init_app(app)
    
    return mysql

def get_db():
    """Obtener conexión a la base de datos (para uso en rutas)"""
    try:
        # En Flask-MySQLdb, la conexión se obtiene así:
        connection = mysql.connection
        return connection
    except Exception as e:
        print(f"❌ Error al obtener conexión: {e}")
        raise RuntimeError(f"Error al conectar a la base de datos: {e}")