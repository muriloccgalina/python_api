from flask import Flask, jsonify, request

app = Flask(__name__)

#future database
users = [
    {
        "id": 1,
        "name": "teste",
        "cpf": "12345678909"
    },
    {
        "id": 2,
        "name": "teste2",
        "cpf": "99999999999"
    },
    {
        "id": 3,
        "name": "teste3",
        "cpf": "11111111111"
    },
]
    
@app.route("user", methods=["POST"])
def create_user(id):
    user = request.get_json()
    ...

@app.route("/user", methods=["GET"])
def get_users():
    return jsonify(users)

@app.route("/user/<int:id>", methods=["GET"])
def get_user_by_id(id):
    ...

@app.route("user/<int:id>", methods=["PUT"])
def update_user(id):
    update_user = request.get_json()
    ...

@app.route("user/<int:id>", methods=["DELETE"])
def delete_user(id):
    ...

app.run(port=8080, host="localhost")
