from flask import * 
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from transformers import GPT2LMHeadModel, GPT2Tokenizer
import numpy as np
# -- 
from transformers import pipeline

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
        prompt = request.args.get('prompt')
        generated_text = request.args.get('generated_text')
                                                  
        return render_template('index.html',prompt=prompt,generated_text=generated_text)
    return redirect(url_for('login',title='Login Page'))
    #return render_template('login.html')

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
    output = model.generate(input_ids, max_length=1000, num_return_sequences=1)
    generated_text = tokenizer.decode(output[0], skip_special_tokens=True)
    # print(generated_text)
    # return str(output)
    # Redirect to an external URL
    # Redirect to another route within the app
    return redirect(url_for('index',prompt=prompt,generated_text=generated_text))
    #return redirect("https://www.google.com")
    #return render_template('index.html',prompt=prompt,generated_text=generated_text)

@app.route('/transformers',methods=['GET','POST'])
def transformers():
    if session.get('username') and session.get('loggedin'): 
        # Initialize sentiment analysis pipeline
        sentiment_analyzer = pipeline("sentiment-analysis") 
        # Get text from the form
        #text = request.form.get('text')
        # Example texts
        texts = [
            "I love this product! It's amazing and works perfectly.",
            "This movie was terrible. I wouldn't recommend it to anyone.",
            "The weather is okay today, not great but not bad either."
        ]
        output =dict()
        for text in texts:
            result = sentiment_analyzer(text)[0]
            # new_arr = np.array([text,result])
            # np.vstack([output,new_arr])
            #output.update()
            print(f"Text: {text}")
            print(f"Sentiment: {result['label']}, Score: {result['score']:.4f}\n")
        return render_template('transformers.html',output = output)
    return redirect(url_for('login',title='Login Page'))

if __name__ == '__main__':
    app.run(debug=True,port='8000')


