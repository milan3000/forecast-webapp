import numpy as np
import pandas as pd
import dash
from dash import dcc
from dash import html
import plotly.graph_objs as go

prediction_df = pd.read_csv('current_prediction.csv', parse_dates=['time'])
# prediction_df = pd.read_csv('/home/reforecast/forecast-webapp/current_prediction.csv', parse_dates=['time'])

time_axis = prediction_df['time']
y_biomass = np.asarray(prediction_df['biomass'])
y_hydropower = np.asarray(prediction_df['hydropower'])
y_wind = np.asarray(prediction_df['wind'])
y_solar = np.asarray(prediction_df['solar'])
y_demand = np.asarray(prediction_df['demand'])
y_residual = y_demand - (y_biomass + y_hydropower + y_wind + y_solar)

color_biomass = (80.988, 178.985, 80.988, 0.8)
color_hydropower = (166.005, 225.981, 255, 0.8)
color_wind = (89.9895, 102.995, 255, 0.8)
color_solar = (255, 242.99, 63.9795, 0.8)
color_demand = (255, 64, 0, 0.8)
color_residual = (116.994, 127.985, 116.994, 0.8)

app = dash.Dash(__name__, assets_folder='assets')
app.title = 'RE Forecast'
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
    name='Biomass',
    fillcolor=f'rgba{(color_biomass)}'
))
fig.add_trace(go.Scatter(
    x=time_axis, y=y_hydropower,
    hoverinfo='x+y',
    mode='lines',
    line=dict(width=0.5, color=f'rgb{(color_hydropower)}'),
    stackgroup='one',
    name='Hydropower',
    fillcolor=f'rgba{(color_hydropower)}'
))
fig.add_trace(go.Scatter(
    x=time_axis, y=y_wind,
    hoverinfo='x+y',
    mode='lines',
    line=dict(width=0.5, color=f'rgb{(color_wind)}'),
    stackgroup='one',
    name='Wind',
    fillcolor=f'rgba{(color_wind)}'
))
fig.add_trace(go.Scatter(
    x=time_axis, y=y_solar,
    hoverinfo='x+y',
    mode='lines',
    line=dict(width=0.5, color=f'rgb{(color_solar)}'),
    stackgroup='one',
    name='Solar',
    fillcolor=f'rgba{(color_solar)}'
))
fig.add_trace(go.Scatter(
    x=time_axis, y=y_residual,
    hoverinfo='x+y',
    mode='lines',
    line=dict(width=0.5, color=f'rgb{(color_residual)}'),
    stackgroup='one',
    name='Residual Load',
    fillcolor=f'rgba{(color_residual)}'
))
fig.add_trace(go.Scatter(
    x=time_axis, y=y_demand,
    hoverinfo='x+y',
    mode='lines',
    line=dict(width=1.25, color=f'rgb{(color_demand)}'),
    name='Demand'
))

fig.update_xaxes(showgrid=True, gridwidth=0.2, gridcolor='rgba(0, 0, 0, 0.3)')
fig.update_yaxes(showgrid=True, gridwidth=0.2, gridcolor='rgba(0, 0, 0, 0.3)')
fig.update_traces(hovertemplate='%{x}<br>%{y:.2f} MWh')

fig.update_layout(xaxis_title="Time", 
                  yaxis_title="[MWh]", 
                  title="Forecast Electricity generation and consumption in Germany",
                  plot_bgcolor='rgba(255, 255, 255, 1)', # set background color with lower alpha value
                  paper_bgcolor='rgba(255, 255, 255, 1)',
                  legend=dict(orientation="h", yanchor="top", y=1.1, xanchor="center", x=0.5)          
)

# create the layout of the app
app.layout = html.Div(children=[
    dcc.Graph(id='forecast-graph', figure=fig)
    ]
)

if __name__ == '__main__':
    app.run_server(debug=True, use_reloader=False)