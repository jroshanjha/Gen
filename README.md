# Gen
This repo Relative Gen and LLM'S Project .......

venv\Scripts\activate
python -m venv venv

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

pip install -r requirements.txt
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

#Expanded Language:- 
Key Enhancements
Language Support:

Added an expanded set of languages with LANGUAGE_CODES for better usability.
Model Caching:

Used Python's functools.lru_cache to cache up to 10 models. This avoids reloading the model each time a request is made, improving performance.
Error Handling:

Checks for identical source and target languages.
Provides error messages for invalid or unsupported language pairs.
Retaining Previous Input:

Dropdowns will retain their selected values after form submission.
The user's input text is translated and displayed on the page.

from functools import lru_cache
pip install Flask transformers sentencepiece torch


pip install flask-bootstrap5