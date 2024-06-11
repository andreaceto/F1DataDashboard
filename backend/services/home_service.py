import matplotlib.pyplot as plt
import base64
from io import BytesIO
from data.model import Results, Races, Drivers, Constructors
from services.common_service import get_dataframe  # Import the common utility function

def generate_home_visualizations():
    # Fetch data from MongoDB collections and convert to DataFrames
    results_df = get_dataframe(Results.collection)
    races_df = get_dataframe(Races.collection)
    drivers_df = get_dataframe(Drivers.collection)
    constructors_df = get_dataframe(Constructors.collection)

    # Example visualization: Points over time for a specific driver
    fig, ax = plt.subplots()
    driver_results = results_df[results_df['driverId'] == 1]  # Example driver ID
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
