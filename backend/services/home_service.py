import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import base64
from io import BytesIO
from services.common_service import YEAR, TEAM_C, DRIVER_C, DRIVER_LS, LINESTYLES, get_dataframe
from data.model import *
import os
import json

def race_key(race_year, race_round):
    return (race_year * 100) + race_round

def races_subset(df, races, race_ids):
    df = df[df.raceId.isin(race_ids)].copy()
    df = df.join(races[['round', 'raceKey']], on='raceId')
    df['round'] -= df['round'].min()
    return df.set_index('round').sort_index().drop_duplicates()

def add_lap_0(df):
    copy = df.T
    copy.insert(0, 0, 0)
    return copy.T

def driver_tag(driver_df_row):
    return ('<a href="{url}" title="Number: {number:.0f}\n'
            'Nationality: {nationality}">{Driver}</a>').format(**driver_df_row)

def constructor_tag(constructor_df_row):
    return ('<a href="{url}" title="Nationality: {nationality}">'
            '{name}</a>').format(**constructor_df_row)

def formatter(v):
    if type(v) is str:
        return v
    if pd.isna(v) or v <= 0:
        return ''
    if v == int(v):
        return f'{v:.0f}'
    return f'{v:.1f}'

def table_html(table, caption):
    return (f'<h3>{caption}</h3>' +
            table.style.format(formatter).to_html())

# Processing for Drivers & Constructors championship tables
def format_standings(df, results, key):
    df = df.sort_values('position')
    gb = results.groupby(key)
    df['Position'] = df.positionText
    df['scores'] = gb.score.sum()
    df['podiums'] = gb.podium.sum()
    return df

# Drivers championship table
def drivers_standings(df, drivers, results):
    index = 'driverId'
    df = df.set_index(index)
    df = df.join(drivers)
    df = format_standings(df, index)
    df['Team'] = results.groupby(index).Team.last()
    use = ['Position', 'Driver',  'Team', 'points', 'wins', 'podiums', 'scores', 'nationality' ]
    df = df[use].set_index('Position')
    df.columns = df.columns.str.capitalize()
    return df

# Constructors championship table
def constructors_standings(df, constructors, drivers, results):
    index = 'constructorId'
    df = df.set_index(index)
    df = df.join(constructors)
    df = format_standings(df, index)
    
    # add drivers for team
    tmp = results.join(drivers.drop(labels="number", axis=1), on='driverId')
    df = df.join(tmp.groupby(index).Driver.unique().str.join(', ').to_frame('Drivers'))

    use = ['Position', 'name', 'points', 'wins', 'podiums', 'scores', 'nationality', 'Drivers' ]
    df = df[use].set_index('Position')
    df.columns = df.columns.str.capitalize()
    return df

# Race results table
def format_results(df, constructors):
    df['Team'] = df.constructorId.map(constructors.name)
    df['Position'] = df.positionOrder
    use = ['Driver', 'Team', 'grid', 'Position', 'points', 'laps', 'time', 'status' ]
    df = df[use].sort_values('Position')
    df = df.set_index('Position')
    df.columns = df.columns.str.capitalize()
    return df

def generate_base64_image(fig):
    img = BytesIO()
    fig.savefig(img, format='png')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode('utf8')
    plt.close(fig)
    return plot_url

def generate_home_data():

    # Fetch data from MongoDB collections and convert to DataFrames
    circuits = get_dataframe(Circuits.collection)
    constructor_results = get_dataframe(ConstructorResults.collection)
    constructors_standings = get_dataframe(ConstructorStandings.collection)
    constructors = get_dataframe(Constructors.collection)
    driver_standings = get_dataframe(DriverStandings.collection)
    drivers = get_dataframe(Drivers.collection)
    lap_times = get_dataframe(LapTimes.collection)
    pit_stops = get_dataframe(PitStops.collection)
    qualifying = get_dataframe(Qualifying.collection)
    races = get_dataframe(Races.collection)
    results = get_dataframe(Results.collection)
    seasons = get_dataframe(Seasons.collection)
    sprint_results = get_dataframe(SprintResults.collection)
    status = get_dataframe(Status.collection)
    safety_cars = get_dataframe(SafetyCars.collection)
    red_flags = get_dataframe(RedFlags.collection)
    virtual_safety_cars = get_dataframe(VirtualSafetyCarEstimates.collection)

    # To sequence the races if they did not happen in order of raceId (ie. 2021)
    races['raceKey'] = race_key(races['year'], races['round'])

    # For display in HTML tables
    drivers['display'] = drivers.surname
    drivers['Driver'] = drivers['forename'] + " " + drivers['surname']
    # Convert 'number' to numeric, coercing errors to NaN
    drivers['number'] = pd.to_numeric(drivers['number'], errors='coerce')
    drivers['Driver'] = drivers.apply(driver_tag, axis=1)
    constructors['label'] = constructors['name']
    constructors['name'] = constructors.apply(constructor_tag, axis=1)

    # Join fields
    results['status'] = results.statusId.map(status.status)
    results['Team'] = results.constructorId.map(constructors.name)
    results['score'] = results.points > 0

    # Convert 'position' to numeric, coercing errors to NaN
    results['position'] = pd.to_numeric(results['position'], errors='coerce')
    # Perform the comparison
    results['podium'] = results.position <= 3

    races = races.loc[races.year == YEAR].sort_values('round').copy()
    races.index = races['raceId']
    results = results[results.raceId.isin(races.index)].copy()
    lap_times = lap_times[lap_times.raceId.isin(races.index)].copy()
    # Save Ids of races that have actually happened (i.e. have valid lap-times).
    race_ids = np.unique(lap_times.raceId)
    driver_standings = races_subset(driver_standings, races, race_ids)
    constructors_standings = races_subset(constructors_standings, races, race_ids)
    sprint_results = sprint_results[sprint_results.raceId.isin(races.index)].copy()
    lap_times = lap_times.merge(results[['raceId', 'driverId', 'positionOrder']], on=['raceId', 'driverId'])
    lap_times['seconds'] = lap_times.pop('milliseconds') / 1000

    plt.rc("figure", figsize=(16, 12))
    plt.rc("font", size=(14))
    plt.rc("axes", xmargin=0.01)

    # Championship position traces
    champ = driver_standings.groupby("driverId").position.last().to_frame("Pos")
    champ = champ.join(drivers)
    order = np.argsort(champ.Pos)
    color = [DRIVER_C[d] for d in champ.index[order]]
    style = [LINESTYLES[DRIVER_LS[d]] for d in champ.index[order]]
    labels = champ.Pos.astype(str) + ". " + champ.display

    chart = driver_standings.pivot(index="raceKey", columns="driverId", values="points")
    names = races.set_index("raceKey").reindex(chart.index).name
    names = names.str.replace("Grand Prix", "GP").rename("Race")
    chart.index = names
    chart.columns = labels

    # Add origin
    row = chart.iloc[0]
    chart = pd.concat(((row * 0).to_frame("").T, chart))

    fig, ax = plt.subplots()
    chart.iloc[:, order].plot(ax=ax, title=f"F1 Drivers' World Championship — {YEAR}", color=color, style=style)
    ax.set_xticks(range(chart.shape[0]))
    ax.set_xticklabels(chart.index, rotation=45)
    ax.grid(axis="x", linestyle="--")
    ax.set_ylabel("Points")
    legend_opts = dict(bbox_to_anchor=(1.02, 0, 0.2, 1),
                       loc="upper right",
                       ncol=1,
                       shadow=True,
                       edgecolor="black",
                       mode="expand",
                       borderaxespad=0.)
    ax.legend(**legend_opts)

    driver_championship_plot = generate_base64_image(fig)

    return {
        'driver_championship_plot': driver_championship_plot
    }
