from flask import Blueprint, request, jsonify
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt
from flask_bcrypt import Bcrypt

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

    try:
        cursor.execute("SELECT * FROM usuarios WHERE email = %s", (email,))
        user = cursor.fetchone()

        if not user or not bcrypt.check_password_hash(user[3], password):
            return jsonify({'msg': 'Credenciales inválidas'}), 401
        
        #creamos el token
        access_token = create_access_token(identity={'id': user[0], 'nombre': user[1], 'email': user[2]}, additional_claims={'is_admin': user[4]})
        return jsonify({'access_token': access_token}), 200
    except Exception as e:
        return jsonify({'msg': 'Error al iniciar sesión'}), 500
    finally:
        cursor.close()