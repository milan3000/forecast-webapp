import numpy as np
import pandas as pd
import requests
import json
import datetime as dt
import pytz

germany_regions_wind_df = pd.read_csv('map_data/germany_regions_wind.csv', dtype = {'plz2': str})
germany_regions_solar_df = pd.read_csv('map_data/germany_regions_solar.csv', dtype = {'plz2': str})
germany_regions_wind_df.set_index('plz2', inplace=True)
germany_regions_solar_df.set_index('plz2', inplace=True)
# germany_regions_wind_df = pd.read_csv('/home/reforecast/forecast-webapp/map_data/germany_regions_wind.csv', dtype = {'plz2': str})
# germany_regions_solar_df = pd.read_csv('/home/reforecast/forecast-webapp/map_data/germany_regions_solar.csv', dtype = {'plz2': str})

start_date = str(dt.datetime.now(pytz.timezone('Europe/Berlin')).date()+ dt.timedelta(days=1))
end_date = str(dt.datetime.now(pytz.timezone('Europe/Berlin')).date() + dt.timedelta(days=7))

def get_variable_df(germany_df, variable, start_date, end_date):
    df = pd.DataFrame()
    for index, row in germany_df.iterrows():
        latitude, longitude = row['lat'], row['lon']
        url = f'https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&hourly={variable}&windspeed_unit=ms&start_date={start_date}&end_date={end_date}&timezone=Europe%2FBerlin'
        response = requests.get(url)
        data = response.json()
        point_df = pd.DataFrame.from_dict(data['hourly'], orient='columns')
        plz_df = pd.DataFrame({'plz2': [index]*168})
        inst_df = pd.DataFrame({'installed': [row['installed']]*168})
        point_df = pd.concat([inst_df, plz_df, point_df], axis=1)
        df = pd.concat([df, point_df], axis=0)
    return df

wind_prediction_df = get_variable_df(germany_regions_wind_df, 'windspeed_80m', start_date, end_date).reset_index(drop=True)
solar_prediction_df = get_variable_df(germany_regions_solar_df, 'direct_radiation', start_date, end_date).reset_index(drop=True)

def wind_power_factor(windspeed):
    if windspeed < 2.5:
        return 0
    if windspeed < 5:
        return 0.06*windspeed - 0.15
    if windspeed < 10:
        return 0.09*windspeed - 0.3
    else:
        return 0.6

wind_prediction_df['wind_power_output'] = wind_prediction_df['windspeed_80m'].apply(wind_power_factor)*wind_prediction_df['installed']
wind_prediction_df['plz2'] = wind_prediction_df['plz2'].astype('str')
wind_prediction_df.to_csv('map_data/current_wind_prediction_map.csv', index=False)
# wind_prediction_df.to_csv('/home/reforecast/forecast-webapp/map_data/current_wind_prediction_map.csv', index=False)

def solar_power_factor(direct_radiation):
    if direct_radiation < 250:
        return 0.001212*direct_radiation
    else:
        return 0.000606*direct_radiation + 0.15

solar_prediction_df['solar_power_output'] = solar_prediction_df['direct_radiation'].apply(solar_power_factor)*solar_prediction_df['installed']
solar_prediction_df['plz2'] = solar_prediction_df['plz2'].astype('str')
solar_prediction_df.to_csv('map_data/current_solar_prediction_map.csv', index=False)
# solar_prediction_df.to_csv('/home/reforecast/forecast-webapp/map_data/current_solar_prediction_map.csv', index=False)

print(wind_prediction_df)