from flask import Flask, jsonify, request
from flask_mysqldb import MySQL

app = Flask(__name__)

# MySQL configurations
app.config['MYSQL_USER'] = 'admin'
app.config['MYSQL_PASSWORD'] = 'db4dev$'
app.config['MYSQL_DB'] = 'userdatabase'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(app)

@app.route('/users', methods=['GET'])
def get_users():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM USERS")
    users = cur.fetchall()
    cur.close()
    return jsonify(users)

@app.route('/users', methods=['POST'])
def add_user():
    data = request.json
    name = data['name']
    age = data['age']

    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO USERS(name, age) VALUES(%s, %s)", (name, age))
    mysql.connection.commit()
    cur.close()

    return jsonify({"message": "User added successfully!"}), 201

@app.route('/users/<int:uid>', methods=['PUT'])
def update_user(uid):
    data = request.json
    name = data['name']
    age = data['age']

    cur = mysql.connection.cursor()
    cur.execute("UPDATE USERS SET name=%s, age=%s WHERE uid=%s", (name, age, uid))
    mysql.connection.commit()
    cur.close()

    return jsonify({"message": "User updated successfully!"})

@app.route('/users/<int:uid>', methods=['DELETE'])
def delete_user(uid):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM USERS WHERE uid=%s", [uid])
    mysql.connection.commit()
    cur.close()

    return jsonify({"message": "User deleted successfully!"})

@app.route('/users/<int:uid>', methods=['GET'])
def get_user_by_id(uid):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM USERS WHERE uid=%s", [uid])
    user = cur.fetchone()
    cur.close()

    if user:
        return jsonify(user)
    else:
        return jsonify({"message": "User not found!"}), 404

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8081)
