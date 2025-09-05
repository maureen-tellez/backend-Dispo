# app.py
from flask import Flask
from config.db import init_db, mysql
from routes.tareas import tareas_bp
from routes.usuarios import usuarios_bp

app = Flask(__name__)

# Configurar e inicializar la base de datos
init_db(app)

# Registrar blueprints
app.register_blueprint(tareas_bp, url_prefix='/tareas')
app.register_blueprint(usuarios_bp, url_prefix='/usuarios')

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