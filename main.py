from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configuración de la base de datos SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializa la base de datos
db = SQLAlchemy(app)

# Define el modelo de usuario
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    telefono = db.Column(db.String(20), nullable=False)

# Crea las tablas en la base de datos (solo la primera vez)
with app.app_context():
    db.create_all()

# Endpoint raíz
@app.route("/")
def root():
    return "root"

# Endpoint para obtener un usuario por ID
@app.route("/users/<int:user_id>", methods=['GET'])
def get_user(user_id):
    user = User.query.get(user_id)
    if user:
        return jsonify({"id": user.id, "name": user.name, "telefono": user.telefono}), 200
    return jsonify({"error": "User not found"}), 404

# Endpoint para crear un usuario
@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    new_user = User(name=data['name'], telefono=data['telefono'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"id": new_user.id, "name": new_user.name, "telefono": new_user.telefono, "status": "user created"}), 201

# Endpoint para actualizar un usuario
@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    data = request.get_json()
    user.name = data.get("name", user.name)
    user.telefono = data.get("telefono", user.telefono)
    db.session.commit()
    return jsonify({"id": user.id, "name": user.name, "telefono": user.telefono, "status": "user updated"}), 200

# Endpoint para borrar un usuario
@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    db.session.delete(user)
    db.session.commit()
    return jsonify({"id": user.id, "status": "user deleted"}), 200

if __name__ == '__main__':
    app.run(debug=True)
