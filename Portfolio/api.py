from flask import Flask,request,jsonify,render_template,abort
# from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__,template_folder='templates')

@app.route('/', methods=['GET'])
def index():
    return 'Welcome to the Flask API!'

# sample Data = 
data = [ {"id": 1, "name": "John Doe", "email": "john@example.com"}, 
        {"id": 2, "name": "Jane Doe", "email": "jane@example.com"} 
       ]
@app.route('/users',methods=['GET'])
def get_users():
    return jsonify(data)

@app.route('/users/<int:id>',methods=['GET'])
def get_user(id):
    user = next((item for item in data if item['id']==id),None)
    #user = list((item for item in data if item['id']==id),None)
    if user is None:
        return jsonify({"error": "User not found"}),404
    return jsonify(user)

@app.route('/users',methods=['POST'])
def add_user():
    new_user = request.get_json()
    if not new_user or not 'id' in new_user or not 'name' in new_user or not 'email' in new_user:
        abort(404)
    data.append(new_user)
    return jsonify(new_user),201

# @app.route('/users/<int:id>',methods=['PUT'])
@app.route('/users/<int:id>',methods=['PUT'])
def update_user(id):
    #update user 
    if id is not None:
        user = next((item for item in data if item['id']==id),None)
        if user is not None:    
            user_update = request.get_json()
            user.update(user_update)
            return jsonify(user),200
        else:
            return jsonify({'error':'You do not have permission to'}),404
    abort(404)
        
@app.route('/users/<int:user_id>', methods=['DELETE']) 
def delete_user(user_id):
    global data 
    data = [user for user in data if user["id"] != user_id] 
    return '', 204

@app.route('/users',methods=['POST'])
def create_user():
    new_user = request.get_json()
    data.append(new_user)
    return jsonify(data),201

if __name__=='__main__':
    app.run(debug=True)
    
    

