import numpy as np
import pandas as pd
import ipywidgets as widgets
import matplotlib.pyplot as plt

prediction_df = pd.read_csv('current_prediction.csv', parse_dates=['time'])

time_axis = prediction_df['time']
y_biomass = np.asarray(prediction_df['biomass'])
y_hydropower = np.asarray(prediction_df['hydropower'])
y_wind = np.asarray(prediction_df['wind'])
y_solar = np.asarray(prediction_df['solar'])
y_demand = np.asarray(prediction_df['demand'])
y_residual = y_demand - (y_biomass + y_hydropower + y_wind + y_solar)

color_biomass = (0.3176, 0.7019, 0.3176)
color_hydropower = (0.6510, 0.8862, 1)
color_wind = (0.3529,0.4039,1)
color_solar = (1, 0.9529, 0.2509)
color_demand = (1, 0.2509, 0)
color_residual = (0.4588, 0.5019, 0.4588, 0.5)

def plot_prediction(detail_index):
    fig, ax = plt.subplots(figsize=(8,5))     
    ax.stackplot(time_axis, y_biomass, y_hydropower, y_wind, y_solar, y_residual, colors = [color_biomass, color_hydropower, color_wind, color_solar, color_residual])
    ax.plot(time_axis, y_demand, color = color_demand)
    plt.xticks(rotation=45)
    ax.grid(alpha=0.3)
    ax.set_ylabel('[MWh]')
    ax.text(ax.get_xlim()[1]+0.1, ax.get_ylim()[1], f'Date: {time_axis[detail_index].date()}')
    ax.text(ax.get_xlim()[1]+0.1, ax.get_ylim()[1]-5000, f'Time: {time_axis[detail_index].time()}')
    ax.text(ax.get_xlim()[1]+0.1, ax.get_ylim()[1]-10000, f'■', color=color_demand)
    ax.text(ax.get_xlim()[1]+0.25, ax.get_ylim()[1]-10000, f'Demand: {round(y_demand[detail_index])} MWh')
    ax.text(ax.get_xlim()[1]+0.1, ax.get_ylim()[1]-15000, f'■', color=color_residual)
    ax.text(ax.get_xlim()[1]+0.25, ax.get_ylim()[1]-15000, f'Residual Load: {round(y_residual[detail_index])} MWh')
    ax.text(ax.get_xlim()[1]+0.1, ax.get_ylim()[1]-20000, f'■', color=color_solar)
    ax.text(ax.get_xlim()[1]+0.25, ax.get_ylim()[1]-20000, f'Solar: {round(y_solar[detail_index])} MWh')
    ax.text(ax.get_xlim()[1]+0.1, ax.get_ylim()[1]-25000, f'■', color=color_wind)
    ax.text(ax.get_xlim()[1]+0.25, ax.get_ylim()[1]-25000, f'Wind: {round(y_wind[detail_index])} MWh')
    ax.text(ax.get_xlim()[1]+0.1, ax.get_ylim()[1]-30000, f'■', color=color_hydropower)
    ax.text(ax.get_xlim()[1]+0.25, ax.get_ylim()[1]-30000, f'Hydropower: {round(y_hydropower[detail_index])} MWh')
    ax.text(ax.get_xlim()[1]+0.1, ax.get_ylim()[1]-35000, f'■', color=color_biomass)
    ax.text(ax.get_xlim()[1]+0.25, ax.get_ylim()[1]-35000, f'Biomass: {round(y_biomass[detail_index])} MWh')
    plt.axvline(x = time_axis[detail_index], color = 'black', ymin=0, ymax=y_demand[detail_index]/ax.get_ylim()[1], alpha=0.5)
    plt.plot(time_axis[detail_index], y_demand[detail_index], 'o', color=color_demand, alpha=0.6)
    plt.plot(time_axis[detail_index], y_solar[detail_index]+y_wind[detail_index]+y_hydropower[detail_index]+y_biomass[detail_index], 'o', color=color_solar, alpha=0.6)
    plt.plot(time_axis[detail_index], y_wind[detail_index]+y_hydropower[detail_index]+y_biomass[detail_index], 'o', color=color_wind, alpha=0.6)
    plt.plot(time_axis[detail_index], y_hydropower[detail_index]+y_biomass[detail_index], 'o', color=color_hydropower, alpha=0.6)
    plt.plot(time_axis[detail_index], y_biomass[detail_index], 'o', color=color_biomass, alpha=0.6)
    plt.show()


interactive_plot = widgets.interact(plot_prediction, detail_index=widgets.IntSlider(0,0,167,1, layout=widgets.Layout(width='50%')), continuous_update=False)
interactive_plot