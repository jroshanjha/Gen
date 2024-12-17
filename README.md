# Gen
This repo Relative Gen and LLM'S Project .......

# Imortant Libraries:- 
from flask import * 
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from transformers import GPT2LMHeadModel, GPT2Tokenizer
from transformers import pipeline # Generate a text givin Prompt:- 
# Initialize text generation pipeline
text_generator = pipeline("text-generation", model="gpt2")

# Language Translation
# use the MarianMT model for translation.
from transformers import MarianMTModel, MarianTokenizer
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

app =Flask(__name__)
app.secret_key = 'your secret key'

if __name__ == '__main__':
    app.run(debug=True,port='8000')

language-translation-app/
│
├── app.py
├── templates/
│   └── translation.html
├── requirements.txt
└── README.md

translation_app/
│-- app.py                # Flask server
│-- templates/
│   └── index.html        # Frontend template
└── requirements.txt      # Dependencies

# pip install sentencepiece
-- SentencePiece is a subword tokenizer library that MarianMT models rely on for tokenizing input text.
-- The tokenizer splits text into smaller units, which makes it efficient for translating various languages.
import sentencepiece
python -c "import sentencepiece; print(sentencepiece.__version__)"