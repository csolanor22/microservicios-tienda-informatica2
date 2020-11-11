from flask import Flask, render_template, json
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///productos.sqlite3'
app.config['SECRET_KEY'] = "random string"

db = SQLAlchemy(app)

class Productos(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(70), unique=True)
    precio = db.Column(db.Integer)

    def __init__(self, nombre, precio):
        self.nombre = nombre
        self.precio = precio


@app.route("/productos")
def get_productos():
    ret = []
    res = Productos.query.all()
    for producto in res:
        ret.append(
            {
                'producto': producto.nombre,
                'precio': producto.precio
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