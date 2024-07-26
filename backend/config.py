import os
from pymongo import MongoClient

def get_databases():
    """
    Establishes a connection to the MongoDB database using an environment variable and returns the database object.
    
    Returns:
        db: The MongoDB database object.
    """
    
    # Get the MongoDB connection string from an environment variable
    mongo_connection_string = os.getenv('MONGO_URI', 'Error in gathering the Connection string')
    
    # Create a MongoDB client
    client = MongoClient(mongo_connection_string)

    # Return the 'F1_Race_Data' and 'F1_Race_Events' databases
    return {
        'F1_Race_Data': client['F1_Race_Data'],
        'F1_Race_Events': client['F1_Race_Events']
    }
