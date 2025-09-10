# routes/tareas.py
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required , get_jwt_identity
from config.db import mysql,get_db_connection

tareas_bp = Blueprint('tareas', __name__)

@tareas_bp.route('/obtener', methods=['GET'])
@jwt_required()
def get():

    #Obtenemos la identidad del dueño del token
    current_user=get_jwt_identity()
    cursor = get_db_connection()
    
    query ='SELECT a.id_usuario, a.descripcion, b.nombre,b.email,a.creado_en FROM tareas  as a INNER JOIN usuarios as b on a.id_usuario=b.id_usuario WHERE a.id_usuario=%s'

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

@tareas_bp.route('/modificar/<int:id_tarea>', methods=['PUT'])
@jwt_required()
def modificar(id_tarea):
  
        #OBtebemos la identidad del dueño dela tarea 
        current_user= get_jwt_identity()

        data = request.get_json()
        descripcion = data.get('descripcion')
        cursor=get_db_connection()
       #verificamos que existe la tarea
        query='select * from tareas where id_tarea = %s'
        cursor.execute(query,(id_tarea,))
        tarea = cursor.fetchone()
        if not tarea:
            cursor.close()
            return  jsonify({"error":"Esa tarea no existe"})
        
        if not tarea[1]== int (current_user):
            cursor.close()
        return jsonify({"error": "Credenciales Incorrectas"}),401
    
        try:
             cursor.execute("update tareas set descripcion = %s where id_tarea=%s",(descripcion,id_tarea))
             cursor.connection.commit()
             return jsonify ({"mensaje": "Datos modificamos correctamentre "}),200
        except Exception as e:
            return jsonify({"error": f"ERROR al actualizar datos:, {str(e)}"})

        finally:
            cursor.close()


        
    
    
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