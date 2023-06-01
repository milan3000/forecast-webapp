import numpy as np
import pandas as pd
import datetime as dt
import pytz

from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from keras.models import load_model
import xgboost as xgb
from joblib import load

from get_features import get_features

scaler_wind = load('models/scaler_wind.joblib')
scaler_solar = load('models/scaler_solar.joblib')
pca_wind = load('models/pca_wind.joblib')
pca_solar = load('models/pca_solar.joblib')
model_wind = load_model('models/wind_model.h5')
model_solar = load_model('models/solar_model.h5')
model_demand = xgb.Booster()
model_demand.load_model('models/demand_model.model')
model_biomass = xgb.Booster()
model_biomass.load_model('models/biomass_model.model')
model_hydropower = xgb.Booster()
model_hydropower.load_model('models/hydropower_model.model')

# scaler_wind = load('/home/reforecast/forecast-webapp/models/scaler_wind.joblib')
# scaler_solar = load('/home/reforecast/forecast-webapp/models/scaler_solar.joblib')
# pca_wind = load('/home/reforecast/forecast-webapp/models/pca_wind.joblib')
# pca_solar = load('/home/reforecast/forecast-webapp/models/pca_solar.joblib')
# model_wind = load_model('/home/reforecast/forecast-webapp/models/wind_model.h5')
# model_solar = load_model('/home/reforecast/forecast-webapp/models/solar_model.h5')
# model_demand = xgb.Booster()
# model_demand.load_model('/home/reforecast/forecast-webapp/models/demand_model.model')
# model_biomass = xgb.Booster()
# model_biomass.load_model('/home/reforecast/forecast-webapp/models/biomass_model.model')
# model_hydropower = xgb.Booster()
# model_hydropower.load_model('/home/reforecast/forecast-webapp/models/hydropower_model.model')

start_date = str(dt.datetime.now(pytz.timezone('Europe/Berlin')).date()+ dt.timedelta(days=1))
end_date = str(dt.datetime.now(pytz.timezone('Europe/Berlin')).date() + dt.timedelta(days=7))

X_wind, X_solar, X_demand, X_biomass, X_hydropower = get_features(start_date, end_date)

X_wind = X_wind.fillna(0)
X_solar = X_solar.fillna(0)

X_wind_std = scaler_wind.transform(np.asarray(X_wind))
X_wind_pca = pca_wind.transform(X_wind_std)
X_solar_std = scaler_solar.transform(np.asarray(X_solar))
X_solar_pca = pca_solar.transform(X_solar_std)

y_wind = model_wind.predict(X_wind_pca)
y_solar = model_solar.predict(X_solar_pca)
y_demand = model_demand.predict(xgb.DMatrix(np.asarray(X_demand)))
y_biomass = model_biomass.predict(xgb.DMatrix(np.asarray(X_biomass)))
y_hydropower = model_hydropower.predict(xgb.DMatrix(np.asarray(X_hydropower)))
y_renewables = (y_biomass+y_hydropower+y_wind.squeeze()+y_solar.squeeze())
y_residual = y_demand - y_renewables

time_axis = pd.date_range(start=f'{start_date}', end=f'{end_date} 23:00:00', freq='H')
time_axis_ticks = pd.date_range(start=f'{start_date}', end=f'{end_date} 23:00:00', freq='D')

prediction_df = pd.DataFrame(np.column_stack((y_demand, y_biomass, y_hydropower, y_wind.squeeze(), y_solar.squeeze()))).rename(columns={0: "demand", 1: "biomass", 2: "hydropower", 3: "wind", 4:"solar"})
prediction_df = pd.concat([pd.DataFrame(time_axis), prediction_df], axis=1).rename(columns={0: "time"})
prediction_df = prediction_df.set_index('time')
prediction_df.to_csv(f'uncertainty_estimation/predictions/{start_date}.csv')
# prediction_df.to_csv(f'/home/reforecast/forecast-webapp/uncertainty_estimation/predictions/{start_date}.csv')

prediction_df.to_csv('current_prediction.csv')
# prediction_df.to_csv('/home/reforecast/forecast-webapp/current_prediction.csv')