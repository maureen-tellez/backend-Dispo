from flask import Flask
import os
from dotenv import load_dotenv
from routes.tareas import tareas_bp


#cargar las variables de entorno
load_dotenv()

def create_app():  #<- Funcion para crear la app
    
    #instancia de la app
    app=Flask(__name__) 

    #registrar el blueprint

    app.register_blueprint(tareas_bp, url_prefix='/tareas')

    return app

#crear app
app=create_app()

if __name__ =="__main__":

    #obtenemos el puerto
    port = int(os.getenv("PORT",8080))

    #corremos la app
    app.run(host="0.0.0.0",port=port, debug=True)