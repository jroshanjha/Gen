from flask import * 
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from transformers import GPT2LMHeadModel, GPT2Tokenizer
import numpy as np
# -- Initialize text generation pipeline
from transformers import pipeline
# -- Language Translation
from transformers import MarianMTModel, MarianTokenizer
import sentencepiece

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
        if request.method == 'POST':
            prompt = request.args.get('prompt')
            generated_text = request.args.get('generated_text')
                                                    
            return render_template('index.html',prompt=prompt,generated_text=generated_text)
        return render_template('index.html')
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
        #return render_template('index.html')
        return redirect(url_for('index'))
    return render_template('login.html')
    
@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('username', None)
    # msg = get_flashed_messages(with_categories=True)
    #return render_template('login.html',msg='You are Logout Now! Please Try Again',title='Login')
    return redirect(url_for('login'))
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
        '''sentiment_analyzer = pipeline("sentiment-analysis") 
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
            print(f"Sentiment: {result['label']}, Score: {result['score']:.4f}\n")'''
            
        ''' GPT-2 (Generative Pre-trained Transformer 2),
        which is known for its ability to generate coherent and contextually relevant text.'''
        # Initialize text generation pipeline
        if request.method == 'POST':
            prompt = request.form['prompt']
            text_generator = pipeline("text-generation", model="gpt2")
            # Generate text
            generated_text = text_generator(prompt, max_length=500, num_return_sequences=1)[0] # 100
            #generated_text = generated_text.split(":")
            return render_template('transformers.html',prompt=prompt,generated_text = generated_text)
        return render_template('transformers.html')
       
    return redirect(url_for('login',title='Login Page'))
def translate(text, model_name):
    tokenizer = MarianTokenizer.from_pretrained(model_name)
    model = MarianMTModel.from_pretrained(model_name)
    inputs = tokenizer(text, return_tensors="pt", padding=True)
    translated = model.generate(**inputs)
    translated_text = tokenizer.batch_decode(translated, skip_special_tokens=True)[0]
    return translated_text

# Example usage
#english_text = "Hello, how are you? I hope you're having a great day!"
#model_name = "Helsinki-NLP/opus-mt-en-fr"  # English to French
# English to Hindi
#translated_text = translate(english_text, model_name)

# Function to load the appropriate model
def load_translation_model(source_lang, target_lang):
    model_name = f"Helsinki-NLP/opus-mt-{source_lang}-{target_lang}"
    tokenizer = MarianTokenizer.from_pretrained(model_name)
    model = MarianMTModel.from_pretrained(model_name)
    return tokenizer, model

# Translate text
def translate_text(tokenizer, model, text):
    inputs = tokenizer.encode(text, return_tensors="pt", padding=True, truncation=True)
    translated = model.generate(inputs, max_length=512)
    return tokenizer.decode(translated[0], skip_special_tokens=True)
# List of available language pairs
LANGUAGE_CODES = {
    "English": "en",
    "French": "fr",
    "Spanish": "es",
    "German": "de",
    "Italian": "it",
    "Russian": "ru",
    "Chinese": "zh",
    "Japanese": "ja",
    "Arabic": "ar",
    "Hindi": "hi",
    "Portuguese": "pt",
    "Dutch": "nl",
    "Swedish": "sv",
    "Finnish": "fi",
    "Turkish": "tr"
}

@app.route('/translation',methods=['GET','POST'])
def translation():
    if session.get('username') and session.get('loggedin'):
        translated_text = ""
        source_lang = LANGUAGE_CODES['Hindi']
        target_lang = LANGUAGE_CODES['English']
        if request.method == 'POST':
            source_lang_name = request.form.get("source_language")
            target_lang_name = request.form.get("target_language")
            input_text = request.form.get("text")
            if source_lang_name and target_lang_name and input_text:
                source_lang = LANGUAGE_CODES[source_lang_name]
                target_lang = LANGUAGE_CODES[target_lang_name]
                # Prevent invalid model names (e.g., en-en)
                if source_lang == target_lang:
                    #translated_text = "Error: Source and target languages cannot be the same."
                    translated_text = translated_text
                else:
                    try:
                        tokenizer, model = load_translation_model(source_lang, target_lang)
                        translated_text = translate_text(tokenizer, model, input_text)
                    except Exception as e:
                        #translated_text = f"Error: {str(e)}"
                        translated_text = translated_text
                    return render_template("translation.html", languages=LANGUAGE_CODES.keys(), translated_text=translated_text)
    return redirect(url_for('login',title='Login Page'))
        
if __name__ == '__main__':
    app.run(debug=True,port='8000')


