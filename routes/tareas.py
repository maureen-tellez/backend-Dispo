from flask import Blueprint, request, jsonify

#Crear el BluePrint
tareas_bp = Blueprint('tareas', __name__)

#Crear un endpoint para obtener tareas

@tareas_bp.route('/obtener',methods=['GET'])
def get():
    return jsonify({"mensaje":"Estas son tus tareas"})

#crear endpoint con post, recibiendo datos desde el body
@tareas_bp.route('/crear',methods=['POST'])
def crear():

    #obtener los datos del body
    data=request.get_json()

    nombre = data.get('nombre')
    apellido = data.get('apellido')
    return  jsonify({"saludos":f"Hola {nombre} {apellido} como estas"})

#endpoint usando put y pasando dato spor le body y el url

@tareas_bp.route('/modificar/<int:user_id>',methods=['PUT'])
def modificar(user_id):
    #obtenemos loas datos del body 
    data = request.get_json()
    nombre = data.get('nombre')
    apellido = data.get('apellido')
    mensaje = f"Usuario con el id: {user_id} y nombre: {nombre} {apellido}"
    
    return jsonify ({"saludo": mensaje})

    