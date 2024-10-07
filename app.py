from flask import Flask, render_template, request, jsonify
import pandas as pd
import plotly.graph_objs as go
import plotly.offline as pyo

app = Flask(__name__)

# Read the CSV file into a pandas DataFrame
df = pd.read_csv('data.csv')

# Extract unique country names from the "country" column
countries = df['country'].unique()

@app.route('/')
def index():
    return render_template('index3.html', countries=countries)

@app.route('/plot', methods=['POST'])
def plot():
    # Get the selected country from the request
    country = request.json['country']

    # Filter the data based on the selected country
    filtered_df = df[df['country'] == country]

    # Create the plot
    trace1 = go.Scatter(
        x=filtered_df['year'],
        y=filtered_df['Observed Education Participation Ratio'],
        mode='lines+markers',
        name='Observed Ratio'
    )
    trace2 = go.Scatter(
        x=filtered_df['year'],
        y=filtered_df['Predicted Education Participation Ratio'],
        mode='lines+markers',
        name='Predicted Ratio'
    )

    data = [trace1, trace2]
    layout = go.Layout(title=f'Education Participation Ratio in {country}',
                       xaxis=dict(title='year'),
                       yaxis=dict(title='Participation Ratio'))

    fig = go.Figure(data=data, layout=layout)

    # Convert the plotly figure to an HTML div
    graph_div = pyo.plot(fig, output_type='div')

    return jsonify({'graph': graph_div})

# if __name__ == '__main__':
#     app.run(debug=True)
