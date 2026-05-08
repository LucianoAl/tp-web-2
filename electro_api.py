from flask import Flask, jsonify, request
from flasgger import Swagger

app = Flask(__name__)
swagger = Swagger(app)

# Persistencia inicial en memoria
productos_electro = {
    1: {'nombre': "Heladera Samsung", 'precio': 850000},
    2: {'nombre': "Lavarropas Drean", 'precio': 450000},
    3: {'nombre': "Microondas BGH", 'precio': 120000},
    4: {'nombre': "Licuadora Philips", 'precio': 60000}
}

carrito = []

def obtener_producto(id):
    if id in productos_electro.keys():
        return productos_electro[id]
    else:
        return None

@app.route('/productos', methods=['GET'])
def get_productos():
    """
    Listar productos disponibles
    ---
    responses:
      200:
        description: Lista de electrodomésticos en stock
    """
    return jsonify(productos_electro)

@app.route('/carrito/<int:id>', methods=['POST'])
def post_carrito(id):
    """
    Agregar un electrodoméstico al carrito a través del ID
    ---
    parameters:
      - in: path
        name: id
        required: true
        type: integer
        description: El ID numérico del electrodoméstico
    responses:
      200:
        description: Producto agregado al carrito
      404: 
        description: Producto no encontrado
    """
    prod_elegido = obtener_producto(id)
    if prod_elegido:
        carrito.append(prod_elegido)
        return jsonify({'message': 'Agregado exitosamente', 'carrito': carrito}), 200
    return jsonify({'message': 'Producto no encontrado'}), 404

@app.route('/carrito/<string:nombre>', methods=['DELETE'])
def delete_item(nombre):
    """
    Eliminar un electrodoméstico del carrito mediante su nombre
    ---
    parameters:
      - in: path
        name: nombre
        required: true
        type: string
        description: Nombre exacto del producto a eliminar
    responses:
      200:
        description: Producto eliminado exitosamente
    """
    aux = nombre.replace(" ", "").lower()
    for item in carrito:
        if item['nombre'].replace(" ", "").lower() == aux:
            carrito.remove(item)
            return jsonify({'message': 'Eliminado exitosamente', 'carrito': carrito}), 200
            
    return jsonify({'message': 'No se encontro el producto en el carrito'}), 404

@app.route('/carrito/total', methods=['GET'])
def get_total():
    """
    Calcular el total de la compra
    ---
    responses:
      200:
        description: Suma total de los precios en el carrito
    """
    total = 0
    if len(carrito) > 0:
        for prod in carrito:
            total += prod['precio']
        return jsonify({'message': f'El total de la compra es de ${total}', 'carrito': carrito}), 200
    else: 
        return jsonify({'message': 'El carrito está vacío', 'total': 0}), 200

if __name__ == '__main__':
    app.run(debug=True)