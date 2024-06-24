import csv
from config import get_databases

# Get the database instances
databases = get_databases()

def import_csv_to_collection(csv_file_path, database_name, collection_name):
    """
    Imports data from a CSV file into a MongoDB collection.

    Args:
        csv_file_path (str): The path to the CSV file.
        database_name (str): The name of the database to use.
        collection_name (str): The name of the collection to import data into.
    """
    db = databases[database_name]
    collection = db[collection_name]
    with open(csv_file_path, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            collection.insert_one(row)
    print(f"Imported data from {csv_file_path} to {database_name}.{collection_name}")

def export_collection_to_csv(database_name, collection_name, csv_file_path):
    """
    Exports data from a MongoDB collection to a CSV file.

    Args:
        database_name (str): The name of the database to use.
        collection_name (str): The name of the collection to export data from.
        csv_file_path (str): The path to the CSV file to export data to.
    """
    db = databases[database_name]
    collection = db[collection_name]
    documents = collection.find()
    with open(csv_file_path, 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=documents[0].keys())
        writer.writeheader()
        for document in documents:
            writer.writerow(document)
    print(f"Exported data from {database_name}.{collection_name} to {csv_file_path}")
