# routes/tareas.py
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required , get_jwt_identity
from config.db import mysql,get_db_connection

tareas_bp = Blueprint('tareas', __name__)

@tareas_bp.route('/obtener', methods=['GET'])
@jwt_required()
def obtener():

    #Obtenemos la identidad del dueño del token
    current_user=get_jwt_identity()
    cursor = get_db_connection()
    
    query ='SELECT a.id_usuario, a.descripcion, b.nombre,b.email,a.creado_en FROM tareas  as a INNER JOIN usuarios as b WHERE a.id_usuario=%s'

    cursor.execute(query,(current_user,))
    lista= cursor.fetchall ()
    cursor.close()

    if not lista:
        return jsonify({"error":"El usuario no tiene tareaaaas"}),404
    
    else:
        return jsonify({"lista":lista}),200

@tareas_bp.route('/crear', methods=['POST'])
@jwt_required()
def crear():
    current_user= get_jwt_identity()
    try:
        data = request.get_json()
        descripcion = data.get('descripcion')
        
        if not descripcion:
            return jsonify({"error": "Debes teclear una descripción"}), 400
        
        cursor= get_db_connection()
        cursor.execute(
            "INSERT INTO tareas (descripcion,id_usuario) VALUES (%s,%s)",
            (descripcion,current_user)
        )
        cursor.connection.commit()
        
        id_tarea = cursor.lastrowid
        cursor.close()
        
        return jsonify({
            "message": "Tarea creada exitosamente",
            "id_tarea": id_tarea
        }), 201
        
    except Exception as e:
        return jsonify({"error": f"No se pudo crear la tarea: {str(e)}"}), 500

@tareas_bp.route('/modificar/<int:tarea_id>', methods=['PUT'])
def modificar(tarea_id):
    try:
        data = request.get_json()
        nueva_descripcion = data.get('descripcion')
        
        cursor = mysql.connection.cursor()
        cursor.execute(
            "UPDATE tareas SET descripcion = %s, modificado_en = NOW() WHERE id_tarea = %s",
            (nueva_descripcion, tarea_id)
        )
        mysql.connection.commit()
        cursor.close()
        
        return jsonify({"message": "Tarea actualizada exitosamente"})
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@tareas_bp.route('/eliminar/<int:tarea_id>', methods=['DELETE'])
def eliminar(tarea_id):
    try:
        cursor = mysql.connection.cursor()
        cursor.execute("DELETE FROM tareas WHERE id_tarea = %s", (tarea_id,))
        mysql.connection.commit()
        cursor.close()
        
        return jsonify({"message": "Tarea eliminada exitosamente"})
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500