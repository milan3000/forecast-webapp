import numpy as np
import pandas as pd
import dash
from dash import dcc
from dash import html
import plotly.graph_objs as go

prediction_df = pd.read_csv('current_prediction.csv', parse_dates=['time'])

time_axis = prediction_df['time']
y_biomass = np.asarray(prediction_df['biomass'])
y_hydropower = np.asarray(prediction_df['hydropower'])
y_wind = np.asarray(prediction_df['wind'])
y_solar = np.asarray(prediction_df['solar'])
y_demand = np.asarray(prediction_df['demand'])
y_residual = y_demand - (y_biomass + y_hydropower + y_wind + y_solar)

color_biomass = (80.988, 178.985, 80.988)
color_hydropower = (166.005, 225.981, 255)
color_wind = (89.9895, 102.995, 255)
color_solar = (255, 242.99, 63.9795)
color_demand = (255, 64, 0)
color_residual = (116.994, 127.985, 116.994, 0.5)

app = dash.Dash(__name__)
server = app.server

# create the figure object
fig = go.Figure()
# add traces to the figure
fig.add_trace(go.Scatter(
    x=time_axis, y=y_biomass,
    hoverinfo='x+y',
    mode='lines',
    line=dict(width=0.5, color=f'rgb{(color_biomass)}'),
    stackgroup='one', # define stack group
    name='Biomass'
))
fig.add_trace(go.Scatter(
    x=time_axis, y=y_hydropower,
    hoverinfo='x+y',
    mode='lines',
    line=dict(width=0.5, color=f'rgb{(color_hydropower)}'),
    stackgroup='one',
    name='Hydropower'
))
fig.add_trace(go.Scatter(
    x=time_axis, y=y_wind,
    hoverinfo='x+y',
    mode='lines',
    line=dict(width=0.5, color=f'rgb{(color_wind)}'),
    stackgroup='one',
    name='Wind'
))
fig.add_trace(go.Scatter(
    x=time_axis, y=y_solar,
    hoverinfo='x+y',
    mode='lines',
    line=dict(width=0.5, color=f'rgb{(color_solar)}'),
    stackgroup='one',
    name='Solar'
))
fig.add_trace(go.Scatter(
    x=time_axis, y=y_residual,
    hoverinfo='x+y',
    mode='lines',
    line=dict(width=0.5, color=f'rgb{(color_residual)}'),
    stackgroup='one',
    name='Residual Load'
))
fig.add_trace(go.Scatter(
    x=time_axis, y=y_demand,
    hoverinfo='x+y',
    mode='lines',
    line=dict(width=0.5, color=f'rgb{(color_demand)}'),
    name='Demand'
))

fig.update_layout(xaxis_title="Time", yaxis_title="[MWh]")

# create the layout of the app
app.layout = html.Div(children=[
    html.H1(children='Germany Electricity Generation Forecast'),
    dcc.Graph(id='example-graph', figure=fig)
])

if __name__ == '__main__':
    app.run_server(debug=True, use_reloader=False)