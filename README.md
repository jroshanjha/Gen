# Gen
This repo Relative Gen and LLM'S Project .......

# Imortant Libraries:- 
from flask import * 
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from transformers import GPT2LMHeadModel, GPT2Tokenizer


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