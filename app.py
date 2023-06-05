import dash
from dash import dcc
from dash import html
from plot_prediction import plot_prediction
from plot_map import plot_map

app = dash.Dash(__name__, assets_folder='assets', use_pages=True)
app.title = 'Renewable Energy Forecast Germany'
server = app.server

# create the layout of the app
app.layout = html.Div(children=[
    dash.page_container
])

if __name__ == '__main__':
    app.run_server(debug=True, use_reloader=False)