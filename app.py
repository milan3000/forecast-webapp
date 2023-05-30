import dash
from dash import dcc
from dash import html
from plot_prediction import plot_prediction
from plot_map import plot_map

app = dash.Dash(__name__, assets_folder='assets')
app.title = 'Renewable Energy Forecast Germany'
server = app.server

fig1 = plot_prediction()
fig2 = plot_map()

# create the layout of the app
app.layout = html.Div(children=[
    html.Div([dcc.Graph(id='graph1',figure=fig1)]),
    html.Div([dcc.Graph(id='graph2',figure=fig2)]),
])

if __name__ == '__main__':
    app.run_server(debug=True, use_reloader=False)