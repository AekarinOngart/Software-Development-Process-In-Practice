from flask import Flask, request, jsonify
from flask_mysqldb import MySQL

app = Flask(__name__)

# กำหนดค่าเชื่อมต่อกับ MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'fbxDB'

mysql = MySQL(app)

# Route สำหรับเพิ่มโพสต์ลงในฐานข้อมูล
@app.route('/post', methods=['POST'])
def create_post():
    data = request.get_json()
    user_id = data['user_id']
    content = data['content']
    location_id = data['location_id']
    
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO posts (user_id, content, location_id) VALUES (%s, %s, %s)", (user_id, content, location_id))
    mysql.connection.commit()
    cur.close()
    
    return jsonify(message='Post created successfully'), 201

# Route สำหรับดึงโพสต์ทั้งหมด
@app.route('/view', methods=['GET'])
def get_all_posts():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM posts")
    result = cur.fetchall()
    cur.close()
    
    posts = [{'post_id': row[0], 'user_id': row[1], 'content': row[2], 'location_id': row[3]} for row in result]
    
    return jsonify(posts)

# Route สำหรับดึงโพสต์จาก user_id ที่ระบุ
@app.route('/view/user/<int:user_id>', methods=['GET'])
def get_posts_by_user(user_id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM posts WHERE user_id = %s", (user_id,))
    result = cur.fetchall()
    cur.close()
    
    posts = [{'post_id': row[0], 'user_id': row[1], 'content': row[2], 'location_id': row[3]} for row in result]
    
    return jsonify(posts)

# Route สำหรับดึงโพสต์จาก location_id ที่ระบุ
@app.route('/view/location/<int:location_id>', methods=['GET'])
def get_posts_by_location(location_id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM posts WHERE location_id = %s", (location_id,))
    result = cur.fetchall()
    cur.close()
    
    posts = [{'post_id': row[0], 'user_id': row[1], 'content': row[2], 'location_id': row[3]} for row in result]
    
    return jsonify(posts)

if __name__ == '__main__':
    app.run(debug=True)
