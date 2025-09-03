# routes/tareas.py
from flask import Blueprint, request, jsonify
from config.db import mysql

tareas_bp = Blueprint('tareas', __name__)

@tareas_bp.route('/obtener', methods=['GET'])
def get():
    try:
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM tareas")
        tareas = cursor.fetchall()
        cursor.close()
        
        return jsonify({
            "mensaje": "Tareas obtenidas exitosamente",
            "tareas": tareas
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@tareas_bp.route('/crear', methods=['POST'])
def crear():
    try:
        data = request.get_json()
        descripcion = data.get('descripcion')
        
        if not descripcion:
            return jsonify({"error": "Debes teclear una descripción"}), 400
        
        cursor = mysql.connection.cursor()
        cursor.execute(
            "INSERT INTO tareas (descripcion) VALUES (%s)",
            (descripcion,)
        )
        mysql.connection.commit()
        
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