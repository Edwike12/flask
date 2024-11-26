from flask import Flask, request, jsonify #converts to a json file
import mysql.connector

app = Flask(__name__)

# Database configuration
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',  # Replace with your MySQL username
    'password': 'Nyasuguta@456',  # Replace with your MySQL password
    'database': 'oop_comments'  # The name of your database
}

# Create a database connection
def get_db_connection():
    conn = mysql.connector.connect(**DB_CONFIG)
    return conn

# Create a new post
@app.route('/posts', methods=['POST'])
def create_post():
    data = request.json
    title = data.get('title')
    content = data.get('content')

    if not title or not content:
        return jsonify({'error': 'Title and content are required!'}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO posts (title, content) VALUES (%s, %s)', (title, content))
    conn.commit()
    post_id = cursor.lastrowid
    cursor.close()
    conn.close()

    return jsonify({'id': post_id, 'title': title, 'content': content}), 201

# Get all posts
@app.route('/posts', methods=['GET'])
def get_posts():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM posts')
    posts = cursor.fetchall()
    cursor.close()
    conn.close()

    return jsonify(posts), 200

# Get a single post by ID
@app.route('/posts/<int:post_id>', methods=['GET'])
def get_post(post_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM posts WHERE id = %s', (post_id,))
    post = cursor.fetchone()
    cursor.close()
    conn.close()

    if not post:
        return jsonify({'error': 'Post not found'}), 404

    return jsonify(post), 200

# Update a post
@app.route('/posts/<int:post_id>', methods=['PUT'])
def update_post(post_id):
    data = request.json
    title = data.get('title')
    content = data.get('content')

    if not title or not content:
        return jsonify({'error': 'Title and content are required!'}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('UPDATE posts SET title = %s, content = %s WHERE id = %s', (title, content, post_id))
    conn.commit()
    updated_rows = cursor.rowcount
    cursor.close()
    conn.close()

    if updated_rows == 0:
        return jsonify({'error': 'Post not found'}), 404

    return jsonify({'id': post_id, 'title': title, 'content': content}), 200

# Delete a post
@app.route('/posts/<int:post_id>', methods=['DELETE'])
def delete_post(post_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM posts WHERE id = %s', (post_id,))
    conn.commit()
    deleted_rows = cursor.rowcount
    cursor.close()
    conn.close()

    if deleted_rows == 0:
        return jsonify({'error': 'Post not found'}), 404

    return jsonify({'message': 'Post deleted successfully'}), 200

if __name__ == "__main__":
    app.run(debug=True)
