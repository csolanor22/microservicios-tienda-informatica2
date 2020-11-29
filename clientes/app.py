from flask import Flask, render_template, json
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///clientes.sqlite3'
app.config['SECRET_KEY'] = "random string"

db = SQLAlchemy(app)

class Clientes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(70), unique=True)
    direccion = db.Column(db.String(20))
    telefono = db.Column(db.String(20))

    def __init__(self, nombre, direccion, telefono):
        self.nombre = nombre
        self.direccion = direccion
        self.telefono = telefono


@app.route("/clientes")
def get_clientes():
    ret = []
    res = Clientes.query.all()
    for cliente in res:
        ret.append(
            {
                'cliente': cliente.nombre,
                'direccion': cliente.direccion,
                'telefono': cliente.telefono
            }
        )
    response = app.response_class(
        response=json.dumps(ret),
        status=200,
        mimetype='application/json'
    )
    return response

@app.route("/clientes/<nombre>")
def get_cliente(nombre):
    ret = []
    res = Clientes.query.all()
    for cliente in res:
        if cliente.nombre == nombre:
            ret.append(
                {
                    'cliente': cliente.nombre,
                    'direccion': cliente.direccion,
                    'telefono': cliente.telefono
                }
            )
    response = app.response_class(
        response=json.dumps(ret),
        status=200,
        mimetype='application/json'
    )
    return response

if __name__ == "__main__":
    app.run(host='0.0.0.0',debug=True)