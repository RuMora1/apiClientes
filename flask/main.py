# pip install Flask Flask-SQLAlchemy pyodbc 

from flask import Flask, jsonify, request, render_template
from flask_sqlalchemy import SQLAlchemy
import webbrowser
from flask_cors import CORS
from collections import OrderedDict
import pyodbc

app = Flask(__name__)
CORS(app, resources={r"/clientes/*": {"origins": "http://127.0.0.1:5000"}})
# CORS(app)

# Configuración de la conexión a SQL Server con credenciales Windows
app.config['SQLALCHEMY_DATABASE_URI'] = (
    'mssql+pyodbc://sa:admin123@localhost/DB_CLIENTES?driver=ODBC+Driver+17+for+SQL+Server'
)

# usuario: ?? contraseña: ?? Las que hayas puesto en SQL Server
# servidor : localhost

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Definir el modelo de la base de datos para la tabla 'clientes'
class Cliente(db.Model):
    __tablename__ = 'clientes'
    id = db.Column(db.Integer, primary_key=True)
    rut = db.Column(db.String(12), nullable=False)  # Rut
    nombre = db.Column(db.String(100), nullable=False)
    apellido = db.Column(db.String(100), nullable=False)
    region = db.Column(db.String(100), nullable=False)  # Region
    cantidad_compras = db.Column(db.Integer, nullable=False, default=0)  # Cantidad de compras

@app.route('/')
def index():
    return render_template('index.html')

def open_browser():
    webbrowser.open_new("http://127.0.0.1:5000/")

# Método GET: Obtener todos los clientes
#@app.route('/clientes', methods=['GET'])
#def get_clientes():
#    clientes = Cliente.query.all()
#    return jsonify([{'id': cliente.id, 'nombre': cliente.nombre} for cliente in clientes])

@app.route('/clientes', methods=['GET'])
@app.route('/clientes/<int:id>', methods=['GET'])
def get_clientes(id=None):
    if id is None:
        # Obtener todos los clientes
        clientes = Cliente.query.all()
        return jsonify([{
            'id': cliente.id,
            'rut': cliente.rut,
            'nombre': cliente.nombre,
            'apellido': cliente.apellido,
            'region': cliente.region,
            'cantidad_compras': cliente.cantidad_compras
        } for cliente in clientes])
    else:
        # Obtener un solo cliente por id
        cliente = Cliente.query.get(id)
        if cliente:
            return jsonify(OrderedDict([
                ('id', cliente.id),
                ('nombre', cliente.nombre),
                ('apellido', cliente.apellido),
                ('rut', cliente.rut),
                ('region', cliente.region),
                ('cantidad_compras', cliente.cantidad_compras)
            ]))
        else:
            return jsonify({'mensaje': 'Cliente no encontrado'}), 404

# Método POST: Crear un nuevo cliente
@app.route('/clientes', methods=['POST'])
def create_cliente():
    data = request.get_json()
    
    # Obtener los valores desde el cuerpo de la solicitud
    rut = data.get('rut')
    nombre = data.get('nombre')
    apellido = data.get('apellido')
    region = data.get('region')
    cantidad_compras = data.get('cantidad_compras')

    if not rut or not nombre or not apellido or not region or cantidad_compras is None:
        return jsonify({'message': 'Todos los campos son requeridos'}), 400

    # Crear nuevo cliente
    new_cliente = Cliente(rut=rut, nombre=nombre, apellido=apellido, region=region, cantidad_compras=cantidad_compras)
    db.session.add(new_cliente)
    db.session.commit()

    return jsonify({
        'message': 'Cliente creado exitosamente',
        'cliente': {
            'id': new_cliente.id,
            'rut': new_cliente.rut,
            'nombre': new_cliente.nombre,
            'apellido': new_cliente.apellido,
            'region': new_cliente.region,
            'cantidad_compras': new_cliente.cantidad_compras
        }
    }), 201

# Método PUT: Actualizar un cliente existente
@app.route('/clientes/<int:id>', methods=['PUT'])
def update_cliente(id):
    data = request.get_json()
    cliente = Cliente.query.get(id)

    if not cliente:
        return jsonify({'mensaje': 'Cliente no encontrado'}), 404

    # Actualizar los campos del cliente con los nuevos valores proporcionados
    cliente.rut = data.get('rut', cliente.rut)
    cliente.nombre = data.get('nombre', cliente.nombre)
    cliente.apellido = data.get('apellido', cliente.apellido)
    cliente.region = data.get('region', cliente.region)
    cliente.cantidad_compras = data.get('cantidad_compras', cliente.cantidad_compras)

    db.session.commit()

    return jsonify({
        'message': {'Cliente actualizado exitosamente'},
        'cliente': {
            'id': cliente.id,
            'rut': cliente.rut,
            'nombre': cliente.nombre,
            'apellido': cliente.apellido,
            'region': cliente.region,
            'cantidad_compras': cliente.cantidad_compras
        }
    })

# Método DELETE: Eliminar un cliente
@app.route('/clientes/<int:id>', methods=['DELETE'])
def delete_cliente(id):
    cliente = Cliente.query.get(id)

    if not cliente:
        return jsonify({'message': 'Cliente no encontrado'}), 404

    db.session.delete(cliente)
    db.session.commit()

    return jsonify({'mensaje': 'Cliente eliminado exitosamente'})

if __name__ == '__main__':
    app.run(debug=True)
