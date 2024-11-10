from flask import Flask, request, jsonify, session
import random
import string

app = Flask(__name__)
app.secret_key = 'your_secretflaskey'  # Secret key for session management

# In-memory data storage
users_data = {
    "user1": {"username": "user1", "password": "password1", "name": "John Doe", "email": "john@example.com"},
    "user2": {"username": "user2", "password": "password2", "name": "Jane Smith", "email": "jane@example.com"},
    "user3": {"username": "user3", "password": "password3", "name": "Alice Brown", "email": "alice@example.com"},
    "user4": {"username": "user4", "password": "password4", "name": "Bob White", "email": "bob@example.com"},
    "user5": {"username": "user5", "password": "password5", "name": "Charlie Black", "email": "charlie@example.com"},
    "user6": {"username": "user6", "password": "password6", "name": "Eve Green", "email": "eve@example.com"},
    "user7": {"username": "user7", "password": "password7", "name": "David Blue", "email": "david@example.com"},
    "user8": {"username": "user8", "password": "password8", "name": "Grace Yellow", "email": "grace@example.com"},
    "user9": {"username": "user9", "password": "password9", "name": "Hannah Red", "email": "hannah@example.com"},
    "user10": {"username": "user10", "password": "password10", "name": "Ian Purple", "email": "ian@example.com"},
}

# CRUD Operations
@app.route('/users', methods=['GET'])
def get_users():
    return jsonify(users_data), 200

@app.route('/users/<username>', methods=['GET'])
def get_user(username):
    user = users_data.get(username)
    if user:
        return jsonify(user), 200
    else:
        return jsonify({"error": "User not found"}), 404

@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    name = data.get('name')
    email = data.get('email')

    if username in users_data:
        return jsonify({"error": "User already exists"}), 400``

    users_data[username] = {
        "username": username,
        "password": password,
        "name": name,
        "email": email
    }
    return jsonify({"message": "User created successfully"}), 201

@app.route('/users/<username>', methods=['PUT'])
def update_user(username):
    data = request.get_json()
    user = users_data.get(username)
    if not user:
        return jsonify({"error": "User not found"}), 404

    user['name'] = data.get('name', user['name'])
    user['email'] = data.get('email', user['email'])
    return jsonify({"message": "User updated successfully"}), 200

@app.route('/users/<username>', methods=['DELETE'])
def delete_user(username):
    if username in users_data:
        del users_data[username]
        return jsonify({"message": "User deleted successfully"}), 200
    else:
        return jsonify({"error": "User not found"}), 404

# Login Route
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = users_data.get(username)
    if user and user['password'] == password:
        session['user'] = username
        return jsonify({"message": "Login successful"}), 200
    else:
        return jsonify({"error": "Invalid username or password"}), 401

# Protecting a Route with Session
@app.route('/profile', methods=['GET'])
def profile():
    if 'user' not in session:
        return jsonify({"error": "You must be logged in to view this page"}), 403
    username = session['user']
    user = users_data.get(username)
    if user:
        return jsonify(user), 200
    else:
        return jsonify({"error": "User not found"}), 404

# Logout Route
@app.route('/logout', methods=['POST'])
def logout():
    session.pop('user', None)
    return jsonify({"message": "Logged out successfully"}), 200

# Index Route
@app.route('/', methods=['GET'])
def index():
    return jsonify({"message": "Initial route"}), 200


if __name__ == '__main__':
    app.run(debug=True)
