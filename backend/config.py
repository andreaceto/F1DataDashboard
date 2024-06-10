import os
from pymongo import MongoClient

def get_database():
    """
    Establishes a connection to the MongoDB database using an environment variable and returns the database object.
    
    Returns:
        db: The MongoDB database object.
    """
    # Get the MongoDB connection string from an environment variable
    mongo_connection_string = os.getenv('MONGO_URI', 'Error in gathering the Connection string')
    
    # Create a MongoDB client
    client = MongoClient(mongo_connection_string)
    
    # Return the 'F1DataDashboard' database
    return client['F1DataDashboard']
