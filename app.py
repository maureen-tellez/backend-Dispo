# app.py
from flask import Flask
import os
from dotenv import load_dotenv
from config.db import init_db,mysql
#Importamos la ruta del blueprint
from routes.tareas import tareas_bp
from routes.usuarios import usuarios_bp
from flask_jwt_extended import JWTManager

#Cargar las variables de entorno
load_dotenv()

app = Flask(__name__)

# Configurar e inicializar la base de datos
init_db(app)

# Registrar blueprints
app.register_blueprint(tareas_bp, url_prefix='/tareas')
app.register_blueprint(usuarios_bp, url_prefix='/usuarios')

def create_app(): #Funciòn para crear la app
    #Instnancia de la app
    app=Flask(__name__)
    #Configurar la base de datos
    init_db(app)
    app.config['JWT_SECRET_KEY']=os.getenv('JWT_SECRET')
    jwt=JWTManager(app)
    #Registrar el blue print
    app.register_blueprint(tareas_bp,url_prefix='/tareas')
    app.register_blueprint(usuarios_bp,url_prefix='/usuarios')
    
    return app
#Crear la app
app = create_app()

if __name__ == "_main_":
    #Obtenemos el puerto
    port = int(os.getenv("PORT",8080))
    #Corremos la app
    app.run(host="0.0.0.0",port=port,debug=True)
# Ruta de prueba para verificar conexión
@app.route('/test-db')
def test_db():
    try:
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT 1")
        result = cursor.fetchone()
        cursor.close()
        return {"status": "success", "message": "Conexión a BD exitosa", "data": result}
    except Exception as e:
        return {"status": "error", "message": str(e)}, 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)

