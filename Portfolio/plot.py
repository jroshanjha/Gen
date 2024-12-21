from flask import Flask, render_template
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import json
import numpy as np
import matplotlib.pyplot as plt 
import seaborn as sns
from plotly.subplots import make_subplots
import plotly

app = Flask(__name__)

# Load your data here
# df = pd.read_csv('your_data.csv')

@app.route('/')
def dashboard():
    # Create your charts here
    charts = create_charts()
    return render_template('dashboard.html', charts=charts) # charts1=charts1

# Simulating data - replace this with your actual data source
def get_data():
    return pd.DataFrame({
        'date': pd.date_range(start='2023-01-01', periods=30),
        'value1': range(30),
        'value2': [i*2 for i in range(30)],
        'category': ['A', 'B', 'C', 'D'] * 7 + ['A', 'B']
    })
def create_charts():
    df = get_data()
    charts = []

    # Ensure 'date' is in datetime format
    df['date'] = pd.to_datetime(df['date'])

    # Slider chart (top-left)
    slider = go.Figure(data=[go.Scatter(x=df['date'], y=df['value1'])])
    slider.update_layout(
        title='Slider Chart',
        xaxis=dict(
            rangeslider=dict(visible=True),
            type="date"
        )
    )
    charts.append({'id': 'slider-chart', 'figure': slider.to_json()})

    # Pie chart (middle-left)
    pie_data = df.groupby('category')['value1'].sum().reset_index()
    pie = px.pie(pie_data, names='category', values='value1', title='Pie Chart')
    charts.append({'id': 'pie-chart', 'figure': pie.to_json()})

    # Line chart (top-middle)
    line = px.line(df, x='date', y=['value1', 'value2'], title='Line Chart')
    charts.append({'id': 'line-chart', 'figure': line.to_json()})

    # Bar chart (right)
    bar_data = df.groupby('category')['value1'].sum().reset_index()
    bar = px.bar(bar_data, x='category', y='value1', title='Bar Chart')
    charts.append({'id': 'bar-chart', 'figure': bar.to_json()})

    # Area chart (bottom)
    area = px.area(df, x='date', y='value1', title='Area Chart')
    charts.append({'id': 'area-chart', 'figure': area.to_json()})
    
    # slice = [12, 25, 50, 36, 19]
    # activities = ['NLP','Neural Network', 'Data analytics', 'Quantum Computing', 'Machine Learning']
    # cols = ['r','b','c','g', 'orange']
    # lan_pie = px.pie(slice,
    # labels =activities,
    # colors = cols,
    # startangle = 90,
    # shadow = True,
    # explode =(0,0.1,0,0,0),
    # autopct ='%1.1f%%')
    # plt.title('Training Subjects')
    
    # charts.append({'id':'language-chart','figure':lan_pie.to_json()})
    
    charts1=[]
    # Language pie chart
    slice_values = [12, 25, 50, 36, 19]
    activities = ['NLP', 'Neural Network', 'Data analytics', 'Quantum Computing', 'Machine Learning']
    colors = ['red', 'blue', 'cyan', 'green', 'orange']

    lan_pie = px.pie(
        values=slice_values,
        names=activities,
        title='Training Subjects',
        color_discrete_sequence=colors,
    )

    lan_pie.update_traces(
        textposition='inside',
        textinfo='percent+label',
        pull=[0, 0.1, 0, 0, 0],
        marker=dict(colors=colors, line=dict(color='#000000', width=2))
    )

    lan_pie.update_layout(
        title_x=0.5,
        showlegend=False
    )
    charts1.append({'id': 'language-chart', 'figure': json.dumps(lan_pie.to_dict(), cls=PlotlyJSONEncoder)})

    # Assuming you have other charts in charts1, process them similarly
    # for chart in charts1:
    #     if 'figure' in chart:
    #         chart['figure'] = json.dumps(chart['figure'], cls=PlotlyJSONEncoder)
    return charts1

# Custom JSON encoder to handle NumPy types
class PlotlyJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        else:
            return super(PlotlyJSONEncoder, self).default(obj)
        
# In your Flask app
def create_charts1():
    charts = []
    
    # Pie chart
    pie_data = go.Pie(labels=['A', 'B', 'C', 'D'], values=[30, 20, 25, 25])
    pie_chart = go.Figure(data=[pie_data])
    charts.append({'id': 'pie-chart', 'figure': pie_chart.to_json()})
    
    # Line chart
    line_data = go.Scatter(x=[1, 2, 3, 4, 5], y=[1, 3, 2, 4, 3])
    line_chart = go.Figure(data=[line_data])
    charts.append({'id': 'line-chart', 'figure': line_chart.to_json()})
    
    # Bar chart
    bar_data = go.Bar(x=['A', 'B', 'C', 'D'], y=[20, 14, 23, 25])
    bar_chart = go.Figure(data=[bar_data])
    charts.append({'id': 'bar-chart', 'figure': bar_chart.to_json()})
    
    # Add more charts as needed
    return charts


@app.route('/line')
def line_plot():
    fig = create_line_charts()
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return render_template('line_plot.html', graphJSON=graphJSON)
def create_line_charts():
    data = {
            'date': ['2024-01-01', '2024-02-01', '2024-03-01', '2024-04-01', '2024-05-01'],
            'sales': [1000, 1200, 800, 1500, 900],
            'visits': [500, 600, 400, 700, 450]
        }
    df = pd.DataFrame(data)
    df['date'] = pd.to_datetime(df['date'])

    # Line chart for sales
    fig_line = px.line(data, x='date', y='sales', title='Sales Trend')

    # Bar chart for visits
    fig_bar = px.bar(data, x='date', y='visits', title='Website Visits')

    # Create subplots
    fig = make_subplots(rows=1, cols=2, subplot_titles=["Sales", "Visits"], shared_xaxes=True)

    # Update layout
    fig.update_layout(
    margin={'t': 20, 'l': 20, 'r': 20, 'b': 20},
    height=500,  # Adjust as needed
    width=1000   # Adjust as needed
    )
    # Add traces to subplots
    fig.add_trace(fig_line.data[0], row=1, col=1)
    fig.add_trace(fig_bar.data[0], row=1, col=2)

    # return fig.to_json()
    return render_template('line_plot.html', chart=fig.to_json())


if __name__ == '__main__':
    app.run(debug=True,port='8000')