import dash
from dash import dcc
from dash import html
from plot_prediction import plot_prediction
from plot_map import plot_map

dash.register_page(__name__, path='/', title='Renewable Energy Forecast Germany')

fig1 = plot_prediction()
fig2 = plot_map()

# create the layout of the app
layout = html.Div(children=[
    html.Div([dcc.Graph(id='graph1',figure=fig1)]),
    html.Div([dcc.Graph(id='graph2',figure=fig2)]),
])