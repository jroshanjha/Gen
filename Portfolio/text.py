@app.route('/images/<int:image_id>/edit', methods=['GET', 'POST'])
def edit_image(image_id):
    image = Image.query.get(image_id)
    if not image:
        return 'Image not found', 404

    # Create a form pre-populated with existing data
    edit_form = UploadForm(title=image.title)

    if edit_form.validate_on_submit():
        # Update image details and save changes
        image.title = edit_form.title.data
        db.session.commit()
        return redirect(url_for('list_images'))

    return render_template('edit_image.html', form=edit_form, image=image)

@app.route('/images/<int:image_id>/delete', methods=['POST'])
def delete_image(image_id):
    image = Image.query.get(image_id)
    if not image



import os
from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'

# Create
@app.route('/upload', methods=['GET', 'POST'])
def upload_image():
    if request.method == 'POST':
        file = request.files['image']
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return redirect(url_for('display_images'))
    return render_template('upload.html')

# Read
@app.route('/')
def display_images():
    images = os.listdir(app.config['UPLOAD_FOLDER'])
    return render_template('images.html', images=images)

# Update
# No update operation for images

# Delete
@app.route('/delete/<filename>')
def delete_image(filename):
    os.remove(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    return redirect(url_for('display_images'))

if __name__ == '__main__':
    app.run(debug=True)

.........

from flask import Flask, request, redirect, url_for
from werkzeug.utils import secure_filename
import os
import imghdr

app = Flask(__name__)

# Set the upload folder path
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')

# Create the uploads folder if it doesn't exist
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Allowed image extensions
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    """Check if the uploaded file is an allowed image"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['POST'])
def upload_file():
    # Get the file from the request
    file = request.files['file']

    # Check if the file is present
    if file and allowed_file(file.filename):
        # Check if the file is a valid image
        file_ext = imghdr.what(file)
        if file_ext in ALLOWED_EXTENSIONS:
            # Get the filename and extension
            filename = secure_filename(file.filename)

            # Save the file in the uploads folder
            file_path = os.path.join(UPLOAD_FOLDER, filename)
            file.save(file_path)

            return f'File {filename} uploaded successfully!'
        else:
            return 'Invalid image file'
    else:
        return 'No file or invalid file extension'

if __name__ == '__main__':
    app.run(debug=True)
    
    
.........


stored_hash = b'$2b$12$...' # Replace with the stored hash from your database
password = "mypassword"

if bcrypt.check_password_hash(stored_hash, password):
    print("Password is correct!")
else:
    print("Password is incorrect.")
    
    
stored_hash = b'$2b$12$...' # Replace with the stored hash from your database
password = "mypassword"
password_bytes = password.encode('utf-8')

if bcrypt.checkpw(password_bytes, stored_hash):
    print("Password is correct!")
else:
    print("Password is incorrect.")
    















<!DOCTYPE html>
<html>
<head>
    <title>Images</title>
</head>
<body>
    <h1>Images</h1>
    <a href="{{ url_for('upload_image') }}">Upload New Image</a>
    <br><br>
    {% for image in images %}
    <img src="{{ url_for('static', filename='uploads/' + image) }}" alt="{{ image }}" width="200">
    <a href="{{ url_for('delete_image', filename=image) }}">Delete</a>
    <br>
    {% endfor %}
</body>
</html>


.............................................................

.............................................................

from flask import Flask, render_template
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import io
import base64

app = Flask(__name__)

# Generate some sample data
data = pd.DataFrame(np.random.rand(50,3), columns=["A", "B", "C"]) 

@app.route('/')
def dashboard():
    # Create plots
    plot_a = create_plot(data["A"])
    plot_b = create_plot(data["B"])
    
    # Encode plots and pass to template
    img_a = encode_image(plot_a)
    img_b = encode_image(plot_b)
    return render_template('dashboard.html', plot_a=img_a, plot_b=img_b)

def create_plot(data):
    plt.figure(figsize=(5,3))
    plt.plot(data)
    plt.ylabel("Y Label")
    plt.xlabel("X Label")
    img = io.BytesIO()
    plt.savefig(img, format='png')
    return img
    
def encode_image(img):
    img.seek(0)
    base64_img = base64.b64encode(img.getvalue()).decode('utf8')

    return base64_img

if __name__ == "__main__":
   app.run(debug=True)
........................................................................................
........................................................................................
........................................................................................

from flask import Flask, render_template
import psycopg2
import pandas as pd
import matplotlib.pyplot as plt
import io
import base64

app = Flask(__name__)

# Connect to PostgreSQL database
conn = psycopg2.connect("dbname=mydb user=postgres password=dbpass")

@app.route('/') 
def dashboard():

    # Execute query and fetch data from PostgreSQL database 
    df = pd.read_sql("""SELECT * FROM sales""", con=conn) 
    
    # Create plots
    plot_revenue = create_plot(df, x="date", y="revenue")
    plot_sales = create_plot(df, x="date", y="units_sold")
    
    # Encode plots and pass to template
    revenue_plot = encode_image(plot_revenue)
    sales_plot = encode_image(plot_sales)

    return render_template('dashboard.html', revenue_plot=revenue_plot, sales_plot=sales_plot)
  
def create_plot(df, x, y):
    
    plt.figure(figsize=(5,3)) 
    plt.plot(df[x], df[y])
    plt.ylabel(y)
    plt.xlabel(x)
    
    img = io.BytesIO()
    plt.savefig(img, format='png')
    return img

# Rest of encoder and main loop similar to previous example

...............................................................................

pip install flask 

python -m venv /path/to/new/virtual/environment 


pip install virtualenv

venv\Scripts\activate


...............................................................................

import folium

# Define the latitude and longitude of the center of India
center_lat = 20.5937
center_lon = 78.9629

# Create a map object centered on India
india_map = folium.Map(location=[center_lat, center_lon], zoom_start=5)

# Add a marker for the capital city, New Delhi
folium.Marker(
    location=[28.6139, 77.2090],
    popup="New Delhi",
    icon=folium.Icon(color="green")
).add_to(india_map)

# Display the map
india_map