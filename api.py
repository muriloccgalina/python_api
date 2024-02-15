from flask import Flask, jsonify, request, make_response
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
    try:
        user = request.get_json()
        query = "INSERT INTO user (name, cpf) VALUES (%s, %s)"
        params = (user["name"], user["cpf"])
        execute_query(query, params)
        return make_response(jsonify({"message": "User created successfully"}), 201)
    except Exception as e:
        return make_response(jsonify({"error": str(e)}), 500)

@app.route("/user", methods=["GET"])
def get_users():
    try:
        mycursor.execute("SELECT * FROM user")
        users = mycursor.fetchall()
        user_list = [UserDTO(user[0], user[1], user[2], user[3]).__dict__ for user in users]
        return make_response(jsonify(user_list))
    except Exception as e:
        return make_response(jsonify({"error": str(e)}), 500)

@app.route("/user/<int:id>", methods=["GET"])
def get_user_by_id(id):
    try:
        mycursor.execute("SELECT * FROM user WHERE id = %s", (id,))
        user = mycursor.fetchone()
        if user:
            user_dto = UserDTO(user[0], user[1], user[2], user[3])
            return make_response(jsonify(user_dto.__dict__))
        else:
            return make_response(jsonify({"message": "User not found"}), 404)
    except Exception as e:
        return make_response(jsonify({"error": str(e)}), 500)

@app.route("/user/<int:id>", methods=["PUT"])
def update_user(id):
    try:
        if get_user_by_id(id).status_code != 404:
            user_data = request.get_json()
            query = "UPDATE user SET name = %s, cpf = %s WHERE id = %s"
            params = (user_data["name"], user_data["cpf"], id)
            execute_query(query, params)
            return make_response(jsonify({"message": "User updated successfully"}))
        else:
            return make_response(jsonify({"message": "User didn't exists"}), 404)
    except Exception as e:
        return make_response(jsonify({"error": str(e)}), 500)

@app.route("/user/<int:id>", methods=["DELETE"])
def delete_user(id):
    try:
        if get_user_by_id(id).status_code != 404:
            query = "UPDATE user SET active = 'N' WHERE id = %s"
            params = (id,)
            execute_query(query, params)
            return make_response(jsonify({"message": "User deleted successfully"}))
        else:
            return make_response(jsonify({"message": "User didn't exists"}), 404)
    except Exception as e:
        return make_response(jsonify({"error": str(e)}), 500)

if __name__ == "__main__":
    app.run(port=8080, host="localhost", debug=True)
