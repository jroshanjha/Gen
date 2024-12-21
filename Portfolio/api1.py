from flask import Flask, request, jsonify

app = Flask(__name__)

# Sample data
users = [
    {"id": 1, "name": "jroshan", "email": "jroshan@gmail.com"},
    {"id": 2, "name": "interveiew", "email": "interveiew@gmail.com"}
]

# GET all users
@app.route('/users', methods=['GET'])
def get_users():
    return jsonify(users)

# GET user by ID
@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = next((user for user in users if user['id'] == user_id), None)
    return jsonify(user) if user else ('', 404)

# POST new user
@app.route('/users', methods=['POST'])
def create_user():
    new_user = request.json
    new_user['id'] = len(users) + 1
    users.append(new_user)
    return jsonify(new_user), 201

# PUT update user
@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    user = next((user for user in users if user['id'] == user_id), None)
    if user:
        user.update(request.json)
        return jsonify(user)
    return ('', 404)

# DELETE user
@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    global users
    users = [user for user in users if user['id'] != user_id]
    return ('', 204)

if __name__ == '__main__':
    app.run(debug=True)