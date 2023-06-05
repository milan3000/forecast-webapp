import dash
from dash import html, Output, Input
import pandas as pd
import json


def load_json():
    df = pd.read_csv('current_prediction.csv')
    json_data = df.to_dict(orient='records')
    return json.dumps(json_data)

dash.register_page(__name__)

layout = html.Div(children=[
    html.Div(load_json())
])