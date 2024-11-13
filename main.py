from flask import Flask, jsonify, request
app = Flask(__name__)

#Endoind raíz 
@app.route("/")
def root():
    return "Hola mundo"

#Endpoint para obtener un usuario por ID
@app.route("/users/<user_id>")
def get_user(user_id):
    user = {
        "id": user_id,
        "name": "Yeimi",
        "telefono": "55520326"
    }
    query = request.args.get("query")
    if query:
        user["query"] = query
    return jsonify(user), 200

#Endpoint para crear un usuario
@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    data["status"] = "user created"
    return jsonify(data), 201

# Endpoint para actualizar un usuario
@app.route('/users/<user_id>', methods=['PUT'])
def update_user(user_id): 
    data = request.get_json()
    updated_user = {
        "id": user_id,
        "name": data.get("name", "fabiana"),
        "telefono": data.get("telefono", "57993449"),
        "status": "user updated"
    }
    return jsonify(updated_user), 200


if __name__ == '__main__':
    app.run(debug=True)
