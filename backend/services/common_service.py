import pandas as pd

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
