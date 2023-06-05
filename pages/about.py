import dash
from dash import html, dcc

dash.register_page(__name__, title='RE Forecast About')

layout = html.Div(children=[
    html.H1(children='About'),
    html.Div(children='''
        The forecast is still in development and an estimation of the uncertainties will be added later. 
    '''),

])