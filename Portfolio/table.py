# from flask import Flask
# from flask_sqlalchemy import SQLAlchemy

# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:jroshan@98@localhost/infodb'
# db = SQLAlchemy(app)

# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(80), unique=True, nullable=False)
#     password = db.Column(db.String(120), nullable=False)
#     email = db.Column(db.String(120), unique=True, nullable=False)
#     image = db.Column(db.String(120),nullable=False)

#     # def __repr__(self):
#     #     return f'<User {self.username}>'
    
    
# # @app.before_first_request
# # def create_tables():
# #   db.create_all()
# @app.before_first_request
# def create_tables():
#     db.create_all()

# # with app.app_context():
# #     db.create_all()


# if __name__ == '__main__':

import pymysql

def create_table(table_name):
  try:
    # Connect to MySQL server
    conn = pymysql.connect(
        host='localhost',
        user='root',
        password='jroshan@98',
        database='infodb'
    )
    cursor = conn.cursor()

    # Create database (if not exists)
    cursor.execute(f"CREATE TABLE IF NOT EXISTS {table_name} (id INT AUTO_INCREMENT PRIMARY KEY,username VARCHAR(255) NOT NULL,email VARCHAR(255) NOT NULL,password VARCHAR(255) NOT NULL,image VARCHAR(255) NOT NULL)")

    conn.commit()
    print(f"TABLE '{table_name}' created successfully")
  except pymysql.Error as err:
    print(f"Error creating TABLE: {err}")
  finally:
    conn.close()
    cursor.close()

# Call the function with your desired database name
create_table('informations')