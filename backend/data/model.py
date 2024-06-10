from pymongo.collection import Collection
from config import get_database

# Get the database instance
db = get_database()

class Results:
    collection: Collection = db['results']

    @staticmethod
    def find(query):
        """
        Finds multiple result documents matching the query.
        
        Args:
            query (dict): The query to match.
        
        Returns:
            documents (Cursor): A cursor to the documents.
        """
        return Results.collection.find(query)

    @staticmethod
    def find_one(query):
        """
        Finds a single result document matching the query.
        
        Args:
            query (dict): The query to match.
        
        Returns:
            document (dict): The matched document.
        """
        return Results.collection.find_one(query)

class Races:
    collection: Collection = db['races']

    @staticmethod
    def find(query):
        """
        Finds multiple race documents matching the query.
        
        Args:
            query (dict): The query to match.
        
        Returns:
            documents (Cursor): A cursor to the documents.
        """
        return Races.collection.find(query)

    @staticmethod
    def find_one(query):
        """
        Finds a single race document matching the query.
        
        Args:
            query (dict): The query to match.
        
        Returns:
            document (dict): The matched document.
        """
        return Races.collection.find_one(query)

class Drivers:
    collection: Collection = db['drivers']

    @staticmethod
    def find(query):
        """
        Finds multiple driver documents matching the query.
        
        Args:
            query (dict): The query to match.
        
        Returns:
            documents (Cursor): A cursor to the documents.
        """
        return Drivers.collection.find(query)

    @staticmethod
    def find_one(query):
        """
        Finds a single driver document matching the query.
        
        Args:
            query (dict): The query to match.
        
        Returns:
            document (dict): The matched document.
        """
        return Drivers.collection.find_one(query)

class Constructors:
    collection: Collection = db['constructors']

    @staticmethod
    def find(query):
        """
        Finds multiple constructor documents matching the query.
        
        Args:
            query (dict): The query to match.
        
        Returns:
            documents (Cursor): A cursor to the documents.
        """
        return Constructors.collection.find(query)

    @staticmethod
    def find_one(query):
        """
        Finds a single constructor document matching the query.
        
        Args:
            query (dict): The query to match.
        
        Returns:
            document (dict): The matched document.
        """
        return Constructors.collection.find_one(query)

class Circuits:
    collection: Collection = db['circuits']

    @staticmethod
    def find(query):
        """
        Finds multiple circuit documents matching the query.
        
        Args:
            query (dict): The query to match.
        
        Returns:
            documents (Cursor): A cursor to the documents.
        """
        return Circuits.collection.find(query)

    @staticmethod
    def find_one(query):
        """
        Finds a single circuit document matching the query.
        
        Args:
            query (dict): The query to match.
        
        Returns:
            document (dict): The matched document.
        """
        return Circuits.collection.find_one(query)

class ConstructorResults:
    collection: Collection = db['constructor_results']

    @staticmethod
    def find(query):
        """
        Finds multiple constructor result documents matching the query.
        
        Args:
            query (dict): The query to match.
        
        Returns:
            documents (Cursor): A cursor to the documents.
        """
        return ConstructorResults.collection.find(query)

    @staticmethod
    def find_one(query):
        """
        Finds a single constructor result document matching the query.
        
        Args:
            query (dict): The query to match.
        
        Returns:
            document (dict): The matched document.
        """
        return ConstructorResults.collection.find_one(query)

class ConstructorStandings:
    collection: Collection = db['constructor_standings']

    @staticmethod
    def find(query):
        """
        Finds multiple constructor standing documents matching the query.
        
        Args:
            query (dict): The query to match.
        
        Returns:
            documents (Cursor): A cursor to the documents.
        """
        return ConstructorStandings.collection.find(query)

    @staticmethod
    def find_one(query):
        """
        Finds a single constructor standing document matching the query.
        
        Args:
            query (dict): The query to match.
        
        Returns:
            document (dict): The matched document.
        """
        return ConstructorStandings.collection.find_one(query)

class DriverStandings:
    collection: Collection = db['driver_standings']

    @staticmethod
    def find(query):
        """
        Finds multiple driver standing documents matching the query.
        
        Args:
            query (dict): The query to match.
        
        Returns:
            documents (Cursor): A cursor to the documents.
        """
        return DriverStandings.collection.find(query)

    @staticmethod
    def find_one(query):
        """
        Finds a single driver standing document matching the query.
        
        Args:
            query (dict): The query to match.
        
        Returns:
            document (dict): The matched document.
        """
        return DriverStandings.collection.find_one(query)

class LapTimes:
    collection: Collection = db['lap_times']

    @staticmethod
    def find(query):
        """
        Finds multiple lap time documents matching the query.
        
        Args:
            query (dict): The query to match.
        
        Returns:
            documents (Cursor): A cursor to the documents.
        """
        return LapTimes.collection.find(query)

    @staticmethod
    def find_one(query):
        """
        Finds a single lap time document matching the query.
        
        Args:
            query (dict): The query to match.
        
        Returns:
            document (dict): The matched document.
        """
        return LapTimes.collection.find_one(query)

class PitStops:
    collection: Collection = db['pit_stops']

    @staticmethod
    def find(query):
        """
        Finds multiple pit stop documents matching the query.
        
        Args:
            query (dict): The query to match.
        
        Returns:
            documents (Cursor): A cursor to the documents.
        """
        return PitStops.collection.find(query)

    @staticmethod
    def find_one(query):
        """
        Finds a single pit stop document matching the query.
        
        Args:
            query (dict): The query to match.
        
        Returns:
            document (dict): The matched document.
        """
        return PitStops.collection.find_one(query)

class Qualifying:
    collection: Collection = db['qualifying']

    @staticmethod
    def find(query):
        """
        Finds multiple qualifying documents matching the query.
        
        Args:
            query (dict): The query to match.
        
        Returns:
            documents (Cursor): A cursor to the documents.
        """
        return Qualifying.collection.find(query)

    @staticmethod
    def find_one(query):
        """
        Finds a single qualifying document matching the query.
        
        Args:
            query (dict): The query to match.
        
        Returns:
            document (dict): The matched document.
        """
        return Qualifying.collection.find_one(query)

class Seasons:
    collection: Collection = db['seasons']

    @staticmethod
    def find(query):
        """
        Finds multiple season documents matching the query.
        
        Args:
            query (dict): The query to match.
        
        Returns:
            documents (Cursor): A cursor to the documents.
        """
        return Seasons.collection.find(query)

    @staticmethod
    def find_one(query):
        """
        Finds a single season document matching the query.
        
        Args:
            query (dict): The query to match.
        
        Returns:
            document (dict): The matched document.
        """
        return Seasons.collection.find_one(query)

class Status:
    collection: Collection = db['status']

    @staticmethod
    def find(query):
        """
        Finds multiple status documents matching the query.
        
        Args:
            query (dict): The query to match.
        
        Returns:
            documents (Cursor): A cursor to the documents.
        """
        return Status.collection.find(query)

    @staticmethod
    def find_one(query):
        """
        Finds a single status document matching the query.
        
        Args:
            query (dict): The query to match.
        
        Returns:
            document (dict): The matched document.
        """
        return Status.collection.find_one(query)
