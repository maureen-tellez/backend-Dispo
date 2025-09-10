from flask import Blueprint, request, jsonify
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt, get_jwt_identity
from flask_bcrypt import Bcrypt
import datetime

from config.db import get_db_connection
import os
from dotenv import load_dotenv

#variables de entorno
load_dotenv()

#Creamos el blueprint
usuarios_bp = Blueprint('usuarios', __name__)

#iniciamos Bcrypt
bcrypt = Bcrypt()

@usuarios_bp.route('/registrar', methods=['POST'])
def registrar():

    #obtenemos los datos del usuario
    data=request.get_json()
    nombre=data.get('nombre')
    email=data.get('email')
    password=data.get('password')

    #validamos
    if not nombre or not email or not password:
        return jsonify({'msg': 'Faltan datos'}), 400
    
    #obtener el cursor 
    cursor = get_db_connection()


    try:
        cursor.execute("SELECT * FROM usuarios WHERE email = %s", (email,))
        existing_user = cursor.fetchone()

        if existing_user:
            return jsonify({'msg': 'El usuario ya existe'}), 400
        
        #hasheamos la contraseña
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        #insertamos el usuario en la base de datos
        cursor.execute("INSERT INTO usuarios (nombre, email, password) VALUES (%s, %s, %s)", (nombre, email, hashed_password))
        cursor.connection.commit()
        return jsonify({'msg': 'Usuario registrado exitosamente'}), 201
    except Exception as e:
        
        return jsonify({'msg': 'Error al registrar usuario'}), 500
    finally:
        cursor.close()

@usuarios_bp.route('/login', methods=['POST'])
def login():
    #obtenemos los datos del usuario
    data=request.get_json()
    email=data.get('email')
    password=data.get('password')

    #validamos
    if not email or not password:
        return jsonify({'msg': 'Faltan datos'}), 400
    
    #obtener el cursor 
    cursor = get_db_connection()
    query="SELECT password, id_usuario FROM usuarios WHERE email= %s"
    cursor.execute(query,(email,))

    usuario =cursor.fetchone()

    if usuario and bcrypt.check_password_hash(usuario[0],password):
        #Generamos el JWT
        expires =datetime.timedelta(minutes=60)

        acces_token= create_access_token(
            identity=str(usuario[1]),
            expires_delta=expires
        )

        cursor.close()
        return jsonify({"acces_token": acces_token}),200 

    else:
        return jsonify({"error":"Credenciales incorrectas"}),401
       

@usuarios_bp.route('/datos', methods=['GET'])
@jwt_required()
def datos():
    current_user= get_jwt_identity()

    cursor = get_db_connection()
    query="SELECT id_usuario,nombre,email FROM USUARIOS where id_usuario =%s"
    cursor.execute(query,(current_user,))
    usuario= cursor.fetchone()

    cursor.close()

    if usuario:
        user_info={
            "id_usuario":usuario[0],
            "nombre": usuario[1],
            "email":usuario[2],
        }
        return jsonify({"datos":user_info}),200

    else:
        return jsonify({"error:Usuario no encontrado"}),400

