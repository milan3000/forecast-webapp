import pandas as pd
import json
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def plot_map():
    germany_wind_geojson = json.load(open('map_data/germany_wind_geojson.json'))
    germany_solar_geojson = json.load(open('map_data/germany_solar_geojson.json'))
    # germany_wind_geojson = json.load(open('/home/reforecast/forecast-webapp/map_data/germany_wind_geojson.json'))
    # germany_solar_geojson = json.load(open('/home/reforecast/forecast-webapp/map_data/germany_solar_geojson.json'))

    wind_prediction_df = pd.read_csv('map_data/current_wind_prediction_map.csv', dtype={'plz2': str})
    solar_prediction_df = pd.read_csv('map_data/current_solar_prediction_map.csv', dtype={'plz2': str})
    # wind_prediction_df = pd.read_csv('/home/reforecast/forecast-webapp/map_data/current_wind_prediction_map.csv', dtype={'plz2': str})
    # solar_prediction_df = pd.read_csv('/home/reforecast/forecast-webapp/map_data/current_solar_prediction_map.csv', dtype={'plz2': str})

    fig2 = make_subplots(rows=1, cols=2, subplot_titles=('Onshore Wind Power', 'Solar Power'), specs=[[{'type': 'choropleth'}, {'type': 'choropleth'}]])

    fig2.add_trace(
        go.Choropleth(
            geojson=json.loads(germany_wind_geojson),
            locations=wind_prediction_df['plz2'],
            z=wind_prediction_df['wind_power_output'],
            colorscale = 'Blues',
            showscale = False,
            zmin = 0,
            zmax = 20000,
            name = 'Wind Power',
            hoverinfo='none'
        ),
        row=1,
        col=1
    )

    fig2.add_trace(
        go.Choropleth(
            geojson=json.loads(germany_solar_geojson),
            locations=solar_prediction_df['plz2'],
            z=solar_prediction_df['solar_power_output'],
            colorscale = 'OrRd',
            showscale = False,
            zmin = 0,
            zmax = 20000,
            name = 'Solar Power',
            hoverinfo='none'
        ),
        row=1,
        col=2
    )

    # Update layout
    fig2.update_layout(
        title_text='Spatiotemporal wind and solar power forecast visualisation',
        height = 700,  # px
        showlegend=False,
        geo1=dict(
            showframe=False,
            showcoastlines=False,
            projection_type='orthographic'),
        geo2=dict(
            showframe=False,
            showcoastlines=False,
            projection_type='orthographic'),
        annotations=[
            dict(
                text='Onshore Wind Power',
                x=0.225,
                y=0.95,
                font=dict(size=14),
                showarrow=False,
                xref='paper',
                yref='paper'
            ),
            dict(
                text='Solar Power',
                x=0.775,
                y=0.95,
                font=dict(size=14),
                showarrow=False,
                xref='paper',
                yref='paper'
            )
        ]
    )

    # Create animation frames
    frames = []
    hours = sorted(wind_prediction_df['time'].unique())

    for hour in hours:
        frame_wind_data = wind_prediction_df[wind_prediction_df['time'] == hour]
        frame_solar_data = solar_prediction_df[solar_prediction_df['time'] == hour]
        frame = go.Frame(
            data=[
                go.Choropleth(
                    geojson=json.loads(germany_wind_geojson),
                    locations=frame_wind_data['plz2'],
                    z=frame_wind_data['wind_power_output'],
                    colorscale = 'Blues',
                    showscale = False,
                    zmin = 0,
                    zmax = 20000,
                    name = 'Wind Power',
                    hoverinfo='none'
                ),
                go.Choropleth(
                    geojson=json.loads(germany_solar_geojson),
                    locations=frame_solar_data['plz2'],
                    z=frame_solar_data['solar_power_output'],
                    colorscale = 'OrRd',
                    showscale = False,
                    zmin = 0,
                    zmax = 20000,
                    name = 'Solar Power',
                    hoverinfo='none'
                )
            ],
            name=hour
        )
        frames.append(frame)

    # Add animation to the figure
    fig2.frames = frames

    # Update animation settings
    fig2.update_layout(
        updatemenus=[
            dict(
                type='buttons',
                buttons=[
                    dict(
                        label='&#9658;',
                        method='animate',
                        args=[None, {'frame': {'duration': 150, 'redraw': True}, 'fromcurrent': True, 'transition': {'duration': 150}}],
                    ),
                    dict(
                        label='&#x2759;&#x2759;',
                        method='animate',
                        args=[[None], {'frame': {'duration': 0, 'redraw': False}, 'mode': 'immediate', 'transition': {'duration': 150}}],
                    )
                ],
                direction='left',
                pad={'r': 10, 't': 87},
                showactive=False,
                x=0.1,
                xanchor='right',
                y=0,
                yanchor='top'
            ),
        ],
        sliders=[
            dict(
                active=0,
                steps=[dict(
                        label=pd.to_datetime(hour).strftime('%Y-%m-%d %H:%M'),
                        method='animate',
                        args=[[hour]],
                        )for hour in hours],
                pad={'t': 50, 'b': 10},
                len=0.9,
                x=0.1,
                xanchor='left',
                y=0,
                yanchor='top',
                currentvalue=dict(visible=True, prefix='Time: ', xanchor='right')
            )
        ]
    )

    # Automatically zoom into Country
    fig2.update_geos(fitbounds="locations")
    return fig2