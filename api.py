from flask import Flask, jsonify, request
import mysql.connector

app = Flask(__name__)

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="12345678",
    database="pyapi_db"
)
mycursor = mydb.cursor()

class UserDTO:
    def __init__(self, id, name, cpf, active):
        self.id = id
        self.name = name
        self.cpf = cpf
        self.active = active

def execute_query(query, params=None):
    mycursor.execute(query, params)
    mydb.commit()
    
@app.route("/user", methods=["POST"])
def create_user():
    user = request.get_json()
    query = "INSERT INTO user (name, cpf) VALUES (%s, %s)"
    params = (user["name"], user["cpf"])
    execute_query(query, params)
    return jsonify({"message": "User created successfuly!"})

@app.route("/user", methods=["GET"])
def get_users():
    mycursor.execute("SELECT * FROM user")
    users = mycursor.fetchall()
    user_list = [UserDTO(user[0], user[1], user[2], user[3]) for user in users]
    return jsonify(user_list)

@app.route("/user/<int:id>", methods=["GET"])
def get_user_by_id(id):
    mycursor.execute("SELECT * FROM user WHERE id = %s", (id,))
    user = mycursor.fetchone()
    return jsonify(UserDTO(user[0], user[1], user[2], user[3]))

@app.route("/user/<int:id>", methods=["PUT"])
def update_user(id):
    user = request.get_json()
    query = "UPDATE user SET name = %s, cpf = %s WHERE id = %s"
    params = (user["name"], user["cpf"], id)
    execute_query(query, params)
    return jsonify({"message": "User updated successfuly"})

@app.route("/user/<int:id>", methods=["DELETE"])
def delete_user(id):
    query = "UPDATE user SET active = 'N' WHERE id = %s"
    params = (id,)
    execute_query(query, params)
    return jsonify({"message": "User deleted successfuly"})

if __name__ == "__main__":
    app.run(port=8080, host="localhost")
