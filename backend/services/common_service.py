import pandas as pd

TEAM_C = {
# ConstructorId : Color Hex Code
    9: "#3671C6", # Red Bull
    131: "#27F4D2", # Mercedes
    6: "#E8002D", # Ferrari
    1: "#FF8000", # McLaren
    117: "#229971", # Aston Martin
    214: "#FF87BC", # Alpine
    3: "#64C4FF", # Williams
    215: "#6692FF", # Racing Bulls
    15: "#52E252", # Sauber
    210: "#B6BABD"  # Haas
}

DRIVER_C = {
# DriverId : Color Hex Code
                  # Red Bull
    830: "#3671C6", # Verstappen 
    815: "#3671C6", # Perez

                  # Mercedes
    1: "#27F4D2", # Hamilton
    847: "#27F4D2", # Russell

                  # Ferrari
    844: "#E8002D", # Leclerc
    832: "#E8002D", # Sainz
    860: "#E8002D", # Bearman

                  # McLaren
    846: "#FF8000", # Norris
    857: "#FF8000", # Piastri

                  # Aston Martin
    4: "#229971", # Alonso
    840: "#229971", # Stroll

                  # Alpine
    842: "#FF87BC", # Gasly
    839: "#FF87BC", # Ocon

                  # Williams
    848: "#64C4FF", # Albon
    858: "#64C4FF", # Sargeant

                  # Racing Bulls
    852: "#6692FF", # Tsunoda
    817: "#6692FF", # Ricciardo

                  # Sauber
    822: "#52E252", # Bottas
    855: "#52E252", # Zhou

                  # Haas
    807: "#B6BABD", # Hulkenberg
    825: "#B6BABD"  # Magnussen
}

DRIVER_LS= {
# DriverId : Line Style
                  # Red Bull
    830: "solid", # Verstappen 
    815: "dashdot", # Perez

                  # Mercedes
    1: "solid", # Hamilton
    847: "dashdot", # Russell

                  # Ferrari
    844: "solid", # Leclerc
    832: "dashdot", # Sainz
    860: "dashed", # Bearman

                  # McLaren
    846: "solid", # Norris
    857: "dashdot", # Piastri

                  # Aston Martin
    4: "solid", # Alonso
    840: "dashdot", # Stroll

                  # Alpine
    842: "solid", # Gasly
    839: "dashdot", # Ocon

                  # Williams
    848: "solid", # Albon
    858: "dashdot", # Sargeant

                  # Racing Bulls
    852: "solid", # Tsunoda
    817: "dashdot", # Ricciardo

                  # Sauber
    822: "solid", # Bottas
    855: "dashdot", # Zhou

                  # Haas
    807: "solid", # Hulkenberg
    825: "dashdot", # Magnussen
}

LINESTYLES = {
    "solid": '-',
    "dashdot": '-.',
    "dashed": '--'
}

def get_dataframe(collection):
    """
    Convert MongoDB collection to pandas DataFrame.
    
    Args:
        collection (Collection): The MongoDB collection.
    
    Returns:
        DataFrame: The resulting pandas DataFrame.
    """
    data = list(collection.find())
    return pd.DataFrame(data)
