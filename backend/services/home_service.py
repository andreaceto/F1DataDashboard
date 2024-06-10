import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import base64
from io import BytesIO
from data.model import Results, Races, Drivers, Constructors

def read_csv(name, **kwargs):
    df = pd.read_csv(f'../input/formula-1-race-data/{name}', na_values=r'\N', **kwargs)
    return df

# Your previous data processing functions here...
# For example, race_key, races_subset, etc.

def generate_home_visualizations():
    # Read data (example, adapt as necessary)
    races = read_csv('races.csv', index_col='raceId')
    results = read_csv('results.csv')
    drivers = read_csv('drivers.csv')
    constructors = read_csv('constructors.csv')
    # Additional data processing here...

    # Example visualization: points over time for a specific driver
    fig, ax = plt.subplots()
    driver_results = results[results['driverId'] == 1]  # Example driver ID
    ax.plot(driver_results['raceId'], driver_results['points'])
    ax.set_title('Driver Points Over Time')
    ax.set_xlabel('Race ID')
    ax.set_ylabel('Points')

    # Convert plot to base64 string
    img = BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode('utf8')
    
    return {"plot": plot_url}
