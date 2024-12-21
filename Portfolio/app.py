from flask import Flask, render_template, request, redirect, url_for, session,flash,get_flashed_messages,make_response
from flask_mysqldb import MySQL
import MySQLdb.cursors as conn
import MySQLdb
import re
from werkzeug.utils import secure_filename
import os
import imghdr
import bcrypt

app = Flask(__name__)

app.secret_key = 'your secret key'

# DB CONNECTION :- 

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'jroshan@98'
app.config['MYSQL_DB'] = 'infodb'

mysql = MySQL(app)
#app.config['UPLOAD_FOLDER'] = 'image'  # Replace with your desired path
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')

# Create a bcrypt object
# bcrypt = bcrypt.Hashingtools(app)

# Create the uploads folder if it doesn't exist
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
    
# Allowed image extensions
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif','pdf'}

def allowed_file(filename):
    """Check if the uploaded file is an allowed image"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/setcookie')
def set_cookie():
    # response = make_response('Cookie set!')
    # response.set_cookie('username', 'bard', max_age=60*60*24)  # Expires in 1 day
    # return response
    
    # Set the cookie
    resp = make_response("Technologies!!!")
    resp.set_cookie("Jroshan", "Technical Educator!!!",max_age=60, secure=True)
    cookie_value = request.cookies.get("Jroshan")
    return resp
    #return f"This is cookies value{cookie_value}"
    
@app.route('/getcookie')
def get_cookie():
    username = request.cookies.get('Jroshan')
    if username:
        return f'Welcome, {username}!'
    else:
        return 'No cookie found!'

@app.route('/', methods=['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        try:
            # Connect to the MySQL database
            conn = MySQLdb.connect(host="localhost", user="root", password="jroshan@98", database="infodb")

            # Create a cursor if connection is successful
            if conn:
                cursor = conn.cursor(MySQLdb.cursors.DictCursor)
                # cursor = mysql.connection.cursor(conn.DictCursor)
                cursor.execute('SELECT * FROM informations WHERE username = % s', (username, ))
                account = cursor.fetchone()
                if account:
                    # Account exists, so verify the password
                    password_bytes = password.encode('utf-8')
                    account['password'] = account['password'].encode('utf-8')
                    if not bcrypt.checkpw(password_bytes,account['password']):
                        #checkpw
                        msg='Incorrect Password / !'
                    else:
                        session['loggedin'] = True
                        session['id'] = account['id']
                        session['username'] = account['username']
                        msg = 'Logged in successfully !'
                        return render_template('index.html', msg = msg,title='Welcome page!')
                else:
                    msg = 'Incorrect username /!'
                        # ... rest of your code using the cursor
        except MySQLdb.Error as err:
            print(f"Error connecting to MySQL: {err}")
        finally:
            # Close the connection if it exists
            if conn:
                conn.close()
    resp = make_response("Technologies!!!")
    resp.set_cookie("Jroshan", "Technical Educator!!!",max_age=60, secure=True)
    cookie_value = request.cookies.get("Jroshan")
    return render_template('login.html', msg = msg,title='Login',cookie_value=cookie_value)
 
@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    msg = get_flashed_messages(with_categories=True)
    return render_template('login.html',msg='You are Logout Now! Please Try Again',title='Login')

@app.route('/register', methods =['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        
        username = request.form['username']
        password = request.form['password']
        # password = bcrypt.generate_password_hash(password)
        password_bytes = password.encode('utf-8')
        salt = bcrypt.gensalt()
        password = bcrypt.hashpw(password_bytes, salt)
        email = request.form['email']
        file = request.files['image']
        file_ext = imghdr.what(file)
        filename = secure_filename(file.filename)
        # filename = secrets.token_hex(10) + '.' + uploaded_file.filename.split('.')[-1]
        # uploaded_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        # return f"Image{image}"
        # return f"Name: {username}, Email: {email}"
        # if not username or not email:
        #     flash('Name and email are required!')
        #     return redirect(url_for('form'))
    
        #     # Process the data (e.g., save to a database)
    
        #     flash('Form submitted successfully!')
        #     return redirect(url_for('form'))
        # Create a cursor
        # cursor = mysql.connection.cursor()
        conn = MySQLdb.connect(host="localhost", user="root", password="jroshan@98", database="infodb")
        cursor = conn.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM informations WHERE username = % s', (username, ))
        account = cursor.fetchone()
        if account:
            msg = 'Account already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address !'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers !'
        elif not username or not password or not email:
            msg = 'Please fill out the form !'
        # Check if the file is present
        elif file_ext not in ALLOWED_EXTENSIONS:
            # Check if the file is a valid image
            msg ='Please Fill Image with png,jpg,jpeg,gif,PDF'
            
            if file and not allowed_file(file.filename):
                msg ='Plase select correct file'
        else:
            # Save the file in the uploads folder 
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            cursor.execute('INSERT INTO informations VALUES (NULL, % s, % s, % s, % s)', (username, email, password, filename ))
            conn.commit()
            msg = 'You have successfully registered !'
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return render_template('register.html', msg = msg,title='Register')

# @app.route('/')
# def home():
#     return render_template('index.html', title='Home Page')

@app.route('/about')
def about():
    return render_template('about.html', title='About Us')

@app.route('/contact')
def contact():
    return render_template('contact.html', title='Contact Us')

if __name__ == '__main__':
    app.run(debug=True)