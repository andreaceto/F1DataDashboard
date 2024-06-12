import csv
from config import get_database

# Get the database instance
db = get_database()

def import_csv_to_collection(csv_file_path, collection_name):
    """
    Imports data from a CSV file into a MongoDB collection.
    
    Args:
        csv_file_path (str): The path to the CSV file.
        collection_name (str): The name of the collection to import data into.
    """
    collection = db[collection_name]
    with open(csv_file_path, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            collection.insert_one(row)

def export_collection_to_csv(collection_name, csv_file_path):
    """
    Exports data from a MongoDB collection to a CSV file.
    
    Args:
        collection_name (str): The name of the collection to export data from.
        csv_file_path (str): The path to the CSV file to export data to.
    """
    collection = db[collection_name]
    documents = collection.find()
    with open(csv_file_path, 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=documents[0].keys())
        writer.writeheader()
        for document in documents:
            writer.writerow(document)
