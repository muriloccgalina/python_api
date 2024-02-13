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
    

@app.route("/users")
def get_users():
    return jsonify(users)

app.run(port=5000, host="localhost", debug=True)
