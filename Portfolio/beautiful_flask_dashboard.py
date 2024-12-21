from flask import Flask, render_template
import random
import json
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np 
import seaborn as sns 
import matplotlib.pyplot as plt 
import plotly.figure_factory as ff
import plotly

app = Flask(__name__)

@app.route('/')
def dashboard():
    # Simulating some data for the dashboard
    sales_data = [random.randint(100, 1000) for i in range(7)]
    user_count = random.randint(1000, 5000)
    revenue = sum(sales_data)

    return render_template('beautifull_flask.html', 
                           sales_data=sales_data, 
                           user_count=user_count, 
                           revenue=revenue)
def generate_country_data():
    countries = ['USA', 'China', 'Japan', 'Germany', 'UK', 'France', 'India', 'Italy', 'Brazil', 'Canada']
    return {country: random.randint(1000, 10000) for country in countries}

def generate_scatter_data():
    regions = ['North America', 'Europe', 'Asia', 'South America', 'Africa', 'Oceania']
    return [{'x': random.randint(1000, 10000), 'y': random.randint(50000, 500000), 'r': random.randint(5, 20), 'region': region} for region in regions]


@app.route('/international')
def international():
 # Simulating various types of data for the international dashboard
    monthly_sales = [random.randint(5000, 15000) for _ in range(12)]
    country_sales = generate_country_data()
    product_sales = {
        'Electronics': random.randint(10000, 20000),
        'Clothing': random.randint(8000, 15000),
        'Food': random.randint(5000, 10000),
        'Books': random.randint(3000, 8000),
        'Toys': random.randint(2000, 6000),
        'Computer Science':random.randint(2000,100000)
    }
    customer_satisfaction = random.uniform(3.5, 5.0)
    total_revenue = sum(monthly_sales)
    total_customers = random.randint(100000, 500000)
    scatter_data = generate_scatter_data()
    
    # Sample data for the charts
    df_bar = pd.DataFrame({
        'Category': ['A', 'B', 'C'],
        'Values': [10, 20, 30]
    })
    
    # Create the bar plot
    fig = px.bar(df_bar, x='Category', y='Values', title='Sample Bar Chart')
    bar_chart = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    
    df_line = pd.DataFrame({
        'Date': pd.date_range(start='1/1/2020', periods=10),
        'Values': [1, 3, 2, 5, 7, 8, 6, 9, 11, 12]
    })
    # Create the line plot
    fig = px.line(df_line, x='Date', y='Values', title='Sample Line Chart')
    line_chart = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    
    df_pie = pd.DataFrame({
        'Category': ['A', 'B', 'C', 'D'],
        'Values': [30, 15, 45, 10]
    })
    
    # Scatter plot data
    df_scatter = pd.DataFrame({
        'x': [1, 2, 3, 4, 5],
        'y': [10, 14, 12, 16, 18],
        'size': [40, 60, 80, 100, 120],
        'color': [10, 20, 30, 40, 50]
    })
    
    # Create the pie chart
    fig = px.pie(df_pie, values='Values', names='Category', title='Sample Pie Chart')
    pie_chart = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    
    # Create the scatter plot
    fig_scatter = px.scatter(df_scatter, x='x', y='y', size='size', color='color',
                             title='Sample Scatter Plot',
                             labels={'x': 'X-axis', 'y': 'Y-axis', 'size': 'Size', 'color': 'Color'},
                             hover_data=['x', 'y', 'size', 'color'])
    scatter_chart = json.dumps(fig_scatter, cls=plotly.utils.PlotlyJSONEncoder)
    
    
    
    
    return render_template('international.html',
                           monthly_sales=monthly_sales,
                           country_sales=json.dumps(country_sales),
                           product_sales=json.dumps(product_sales),
                           customer_satisfaction=customer_satisfaction,
                           total_revenue=total_revenue,
                           total_customers=total_customers,
                           scatter_data=json.dumps(scatter_data),
                           bar_chart=bar_chart,
                           line_chart=line_chart,
                           pie_chart=pie_chart,
                           scatter_chart=scatter_chart)

@app.route('/home')
def home():
    
    

    

    # Create Plotly charts
    fig_bar = px.bar(df_bar, x='Category', y='Values', title='Bar Chart')
    fig_line = px.line(df_line, x='Date', y='Values', title='Line Chart')
    fig_pie = px.pie(df_pie, names='Category', values='Values', title='Pie Chart')
    fig_scatter = px.scatter(df_scatter, x='x', y='y', size='size', color='color', title='Scatter Plot')

    # Convert the Plotly figures to JSON
    graphJSON_bar = json.dumps(fig_bar, cls=plotly.utils.PlotlyJSONEncoder)
    graphJSON_line = json.dumps(fig_line, cls=plotly.utils.PlotlyJSONEncoder)
    graphJSON_pie = json.dumps(fig_pie, cls=plotly.utils.PlotlyJSONEncoder)
    graphJSON_scatter = json.dumps(fig_scatter, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template('home.html', graphJSON_bar=graphJSON_bar, graphJSON_line=graphJSON_line, graphJSON_pie=graphJSON_pie, graphJSON_scatter=graphJSON_scatter)



if __name__ =='__main__':
    app.run(debug=True,port=9205)