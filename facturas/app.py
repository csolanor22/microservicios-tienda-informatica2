from flask import Flask, json
import requests

app = Flask(__name__)

items_factura_list = []

class producto_item():
    def __init__(self, producto, precio):
        self.producto = producto
        self.precio = precio

class cliente_factura():
    def __init__(self, nombre, direccion, telefono):
        self.nombre = nombre
        self.direccion = direccion
        self.telefono = telefono

@app.route("/facturas/<producto>/<cantidad>")
def agregar_producto(producto, cantidad):
    try:
        cliente_factura_res
    except:
        response = app.response_class(
                response=json.dumps({'error': 'Debe seleccionar primero un cliente.'}),
                status=400,
                mimetype='application/json'
            )
        return response

    r = requests.get('http://productos:5000/productos/'+producto)

    item = r.json()
    producto_it = producto_item('producto', 0)

    item_object = item[0]
    for key, value in item_object.items():
        if key == 'producto':
            producto_it.producto = value
        if key == 'precio':
            producto_it.precio = value

    items_factura_list.append(
        {
            'producto': producto_it.producto,
            'cantidad': cantidad,
            'precio_unitario': producto_it.precio,
            'precio_total': producto_it.precio*int(cantidad)
        }
    )
    
    total = 0

    for item in items_factura_list:
       total = total + int(item['precio_total'])

    factura = {
        'cliente': cliente_factura_res,
        'productos': [items_factura_list],
        'valor_total': total
    }

    response = app.response_class(
            response=json.dumps(factura),
            status=200,
            mimetype='application/json'
        )
    return response

@app.route("/facturas/nueva-factura/<cliente>")
def nueva_factura(cliente):
    global cliente_factura_res
    r = requests.get('http://clientes:5000/clientes/'+cliente)

    item = r.json()
    item_object = item[0]
    cliente_new = cliente_factura("","","")

    for key, value in item_object.items():
        if key == 'cliente':
            cliente_new.nombre = value
        if key == 'direccion':
            cliente_new.direccion = value
        if key == 'telefono':
            cliente_new.telefono = value


    cliente_factura_res = {
        'cliente': cliente_new.nombre,
        'direccion': cliente_new.direccion,
        'telefono': cliente_new.telefono
    }

    response = {
        'Mensaje': 'Nueva factura creada. Ingrese items',
        'Cliente': cliente_factura_res
    }
    items_factura_list.clear()
    response = app.response_class(
        response= json.dumps(response),
        status=200,
        mimetype='application/json'
        )
    return response

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)