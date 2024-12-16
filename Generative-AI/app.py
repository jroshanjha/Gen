from flask import * 
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from transformers import GPT2LMHeadModel, GPT2Tokenizer

app =Flask(__name__)
app.secret_key = 'your secret key'

'''
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'mysecretkey'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)
# db.create_all()
class User(db.Model):
    pass
'''

@app.route('/')
def index():
    if 'username' in session and session.get('loggedin'):
        return render_template('index.html')
    
    return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        # user = User.query.filter_by(username=username).first()
        session['loggedin'] = True
        session['username'] =username
        return render_template('index.html')
    return render_template('login.html')
    
@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('username', None)
    # msg = get_flashed_messages(with_categories=True)
    return render_template('login.html',msg='You are Logout Now! Please Try Again',title='Login')

@app.route('/predict', methods=['POST'])
def predict():
    prompt = request.form['prompt']
    # model = GPT2LMHeadModel.from_pretrained('gpt2-medium')
    # tokenizer = GPT2Tokenizer.from_pretrained('gpt2-medium')
    tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
    model = GPT2LMHeadModel.from_pretrained("gpt2")
    
    # input_ids = tokenizer.encode(text, return_tensors="pt")
    # output = model.generate(input_ids, max_length=100)
    input_ids = tokenizer.encode(prompt, return_tensors='pt')
    output = model.generate(input_ids, max_length=100, num_return_sequences=1)
    generated_text = tokenizer.decode(output[0], skip_special_tokens=True)
    # print(generated_text)
    # return str(output)
    return render_template('index.html',prompt=prompt,generated_text=generated_text)

if __name__ == '__main__':
    app.run(debug=True,port='8000')


