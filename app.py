import dash
import json
import pandas as pd
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
from plot_prediction import plot_prediction
from plot_map import plot_map

app = dash.Dash(__name__, assets_folder='assets', use_pages=True)
app.title = 'Renewable Energy Forecast Germany'
server = app.server

# Define an API endpoint that returns the JSON data
@app.server.route('/api/data')
def api_data():
    df = pd.read_csv('current_prediction.csv')
    json_data = df.to_dict(orient='records')
    return json.dumps(json_data)

app.layout = html.Div(children=[
    dash.page_container
])

if __name__ == '__main__':
    app.run_server(debug=True, use_reloader=False)