from flask import Blueprint, request, jsonify

#Crear el BluePrint
tareas_bp = Blueprint('tareas', __name__)

#Crear un endpoint para obtener tareas

@tareas_bp.route('/obtener',methods=['GET'])
def get():
    return jsonify({"mensaje":"Estas son tus tareas"})