import numpy as np
import pandas as pd
import requests
import pytz
from astral.sun import sun
from astral import LocationInfo
# from datetime import timedelta
from datetime import datetime

def get_variable_df(variable, start_date, end_date):
    #Pointgrid
    extent = [5.87, 15.03, 47.27, 55.06]
    n_points = 20
    x = np.linspace(extent[0], extent[1], n_points)
    y = np.linspace(extent[2], extent[3], n_points)
    xx, yy = np.meshgrid(x, y)
    points = list(zip(yy.flatten(), xx.flatten()))
    
    df = pd.DataFrame(pd.date_range(start=f'{start_date}', end=f'{end_date} 23:00:00', freq='h')).rename(columns={0:'time'})
    for point in points:
        latitude, longitude = point
        url = f'https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&hourly={variable}&windspeed_unit=ms&start_date={start_date}&end_date={end_date}&timezone=Europe%2FBerlin'
        response = requests.get(url)
        data = response.json()
        point_df = pd.DataFrame.from_dict(data['hourly'], orient='columns').rename(columns={variable: point}).drop('time', axis=1)
        df = pd.concat([df, point_df], axis=1)
    df = df.set_index(['time'])
    return df

def get_interpolated_wind_df(variable1, variable2, start_date, end_date):
    df1 = get_variable_df(variable1, start_date, end_date)
    df2 = get_variable_df(variable2, start_date, end_date)
    lin_interpolated_df = (df1 + df2)/2
    return lin_interpolated_df

def createTimeFeatures(start_date, end_date):
    early_start = '2020 01-01'
    time_df = pd.DataFrame(pd.date_range(start=f'{early_start}', end=f'{end_date} 23:00:00', freq='h')).rename(columns={0:'datetime'})
    time_df['year'] = time_df['datetime'].dt.year
    time_df['month'] = time_df['datetime'].dt.month
    time_df['day_of_month'] = time_df['datetime'].dt.day
    time_df['day_of_year'] = time_df['datetime'].dt.dayofyear
    time_df['day_of_week'] = time_df['datetime'].dt.dayofweek
    time_df['hour'] = time_df['datetime'].dt.hour
    time_df = time_df.set_index('datetime')
    
    month_dummies = pd.get_dummies(time_df['month'], prefix='month', drop_first=False)
    dow_dummies = pd.get_dummies(time_df['day_of_week'], prefix='dow', drop_first=False)
    doy_dummies = pd.get_dummies(time_df['day_of_year'], prefix='doy', drop_first=False)
    hour_dummies = pd.get_dummies(time_df['hour'], prefix='hour', drop_first=False)
    time_enc_df = pd.concat([time_df.drop(['month', 'day_of_week', 'day_of_year', 'hour'], axis=1), month_dummies, dow_dummies, doy_dummies, hour_dummies], axis=1)
    
    time_df = time_df.loc[start_date:f'{end_date} 23:00:00']
    time_enc_df = time_enc_df.loc[start_date:f'{end_date} 23:00:00']
    return time_df, time_enc_df

def get_sun_status(latitude, longitude, date):
    city = LocationInfo("Custom Location", "Country", "Region", latitude, longitude)
    s = sun(city.observer, date=date)
    berlin_tz = pytz.timezone('Europe/Berlin')
    s["sunrise"] = s["sunrise"].astimezone(berlin_tz)
    s["sunset"] = s["sunset"].astimezone(berlin_tz)
    return s["sunrise"], s["sunset"]

def create_day_night_df(start, end):
    #Lats and Longs for sun
    east_lat = 51.1508
    east_long = 14.9689
    west_lat = 50.9988
    west_long = 5.8246
    
    day_night_df = pd.DataFrame(pd.date_range(start=start, end=end, freq='H'), columns=['datetime'])
    day_night_df['day_night'] = 0
    days = pd.date_range(start=start, end=end, freq='D')
    for day in days:
        sunrise = get_sun_status(east_lat, east_long, day)[0].hour-1
        sunset = get_sun_status(west_lat, west_long, day)[1].hour+1
        for hour in range(24):
            if sunrise < hour < sunset:
                day_night_df.loc[(day_night_df['datetime'] == f'{day} {hour:02d}:00:00'), 'day_night'] = 1
    day_night_df.set_index('datetime', inplace=True)
    return day_night_df

def get_installed_capacity(start_date, energy_id):
    date_time = datetime.strptime(f'{start_date} 00:00:00', '%Y-%m-%d %H:%M:%S')
    timestamp = int(1000 * date_time.timestamp())
    timestamp_url = f'https://www.smard.de/app/chart_data/{energy_id}/DE/index_hour.json'
    timestamp_list = requests.get(timestamp_url).json()
    timestamp_list = timestamp_list['timestamps']
    closest_timestamp = min(timestamp_list, key=lambda x: abs(x - timestamp))
    url = f'https://www.smard.de/app/chart_data/{energy_id}/DE/{energy_id}_DE_hour_{closest_timestamp}.json'
    response = requests.get(url)
    data = response.json()
    installed_capacity_df = pd.DataFrame.from_dict(data['series'])
    installed_capacity_df = installed_capacity_df.drop([0], axis=1)
    return installed_capacity_df

def get_features(start_date, end_date):
    
    #Now grab all the data to fill the dataframes
    temperature_2m_df = get_variable_df('temperature_2m', start_date, end_date)
    windspeed_100m_df = get_interpolated_wind_df('windspeed_120m', 'windspeed_80m', start_date, end_date)
    winddirection_100m_df = get_interpolated_wind_df('winddirection_120m', 'winddirection_80m', start_date, end_date)
    surface_pressure_df = get_variable_df('surface_pressure', start_date, end_date)
    precipitation_df = get_variable_df('precipitation', start_date, end_date)
    direct_radiation_df = get_variable_df('direct_radiation', start_date, end_date)
    diffuse_radiation_df = get_variable_df('diffuse_radiation', start_date, end_date)
    direct_normal_irradiance_df = get_variable_df('direct_normal_irradiance', start_date, end_date)
    cloudcover_df = get_variable_df('cloudcover', start_date, end_date)
    
    time_df, time_enc_df = createTimeFeatures(start_date, end_date)
    day_night_df = create_day_night_df(f'{start_date} 00:00:00', f'{end_date} 23:00:00')
    
    wind_onshore_id = '186'
    solar_id = '188'
    wind_offshore_id = '4076'
    installed_wind_onshore_df = get_installed_capacity(start_date, wind_onshore_id)
    installed_wind_offshore_df = get_installed_capacity(start_date, wind_offshore_id)
    installed_wind_total_df = installed_wind_onshore_df + installed_wind_offshore_df
    installed_solar_df = get_installed_capacity(start_date, solar_id)
    
    #Concat the dfs to create the prediction dfs
    wind_df_list = [windspeed_100m_df, 
                    winddirection_100m_df, 
                    temperature_2m_df, 
                    surface_pressure_df, 
                    precipitation_df, 
                    installed_wind_total_df, 
                    time_df, 
                    time_enc_df]
    for df in wind_df_list:
        df.reset_index(drop=True, inplace=True)
    wind_prediction_df = pd.concat(wind_df_list, axis=1)
    
    solar_df_list = [day_night_df, 
                     time_df, 
                     time_enc_df, 
                     temperature_2m_df, 
                     direct_radiation_df, 
                     cloudcover_df, 
                     diffuse_radiation_df, 
                     direct_normal_irradiance_df, 
                     precipitation_df, 
                     installed_solar_df]
    for df in solar_df_list:
        df.reset_index(drop=True, inplace=True)
    solar_prediction_df = pd.concat(solar_df_list, axis=1)
    
    demand_df_list = [day_night_df, 
                     time_df, 
                     time_enc_df, 
                     temperature_2m_df]
    for df in demand_df_list:
        df.reset_index(drop=True, inplace=True)
    demand_prediction_df = pd.concat(demand_df_list, axis=1)
    
    biomass_hydropower_df_list = [day_night_df, 
                     time_df, 
                     time_enc_df]
    for df in biomass_hydropower_df_list:
        df.reset_index(drop=True, inplace=True)
    biomass_hydropower_prediction_df = pd.concat(biomass_hydropower_df_list, axis=1)
    
    return wind_prediction_df, solar_prediction_df, demand_prediction_df, biomass_hydropower_prediction_df, biomass_hydropower_prediction_df

def get_map_features(start_date, end_date):
    return