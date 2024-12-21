from flask import Flask ,render_template , jsonify
import json

import folium

app = Flask(__name__)

# Function to load data from a JSON file
def load_data():
    with open('data/data.json') as f:
        return json.load(f)

@app.route('/display')
def display():
    data = load_data()  # Load data from JSON file
    return render_template('display.html', data=data)
@app.route('/api/data')
def get_data():
    data = load_data()
    return jsonify(data)

@app.route('/temp')
def temp():
    m = folium.Map(location=[45.5236, -122.6750], zoom_start=13)
    m.save('templates/map.html')
    return render_template('temp.html')

@app.route('/map')
def map():
    return render_template('map.html')    

@app.route('/education')
def education():
    data = {
        'india': [6, 8, 7, 12, 9, 14, 10, 11, 13, 15],
        'sri': [4, 7, 9, 8, 11, 10, 12, 9, 14, 13],
        'overs': list(range(1, 11))
    }
    return render_template('education.html',data=data)
@app.route('/calculator')
def calculator():
    return render_template('calculator.html')
if __name__ =='__main__':
    app.run(debug=True,port=9205)