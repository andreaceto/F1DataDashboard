from pymongo.collection import Collection
from config import get_databases

# Get the database instances
databases = get_databases()

# Access the individual databases
db_race_data = databases['F1_Race_Data']
db_race_events = databases['F1_Race_Events']

# F1_Race_Data collections
class Circuits:
    collection: Collection = db_race_data['circuits']

    @staticmethod
    def find(query):
        return Circuits.collection.find(query)

    @staticmethod
    def find_one(query):
        return Circuits.collection.find_one(query)

class ConstructorResults:
    collection: Collection = db_race_data['constructor_results']

    @staticmethod
    def find(query):
        return ConstructorResults.collection.find(query)

    @staticmethod
    def find_one(query):
        return ConstructorResults.collection.find_one(query)

class ConstructorStandings:
    collection: Collection = db_race_data['constructor_standings']

    @staticmethod
    def find(query):
        return ConstructorStandings.collection.find(query)

    @staticmethod
    def find_one(query):
        return ConstructorStandings.collection.find_one(query)

class Constructors:
    collection: Collection = db_race_data['constructors']

    @staticmethod
    def find(query):
        return Constructors.collection.find(query)

    @staticmethod
    def find_one(query):
        return Constructors.collection.find_one(query)

class DriverStandings:
    collection: Collection = db_race_data['driver_standings']

    @staticmethod
    def find(query):
        return DriverStandings.collection.find(query)

    @staticmethod
    def find_one(query):
        return DriverStandings.collection.find_one(query)

class Drivers:
    collection: Collection = db_race_data['drivers']

    @staticmethod
    def find(query):
        return Drivers.collection.find(query)

    @staticmethod
    def find_one(query):
        return Drivers.collection.find_one(query)

class LapTimes:
    collection: Collection = db_race_data['lap_times']

    @staticmethod
    def find(query):
        return LapTimes.collection.find(query)

    @staticmethod
    def find_one(query):
        return LapTimes.collection.find_one(query)

class PitStops:
    collection: Collection = db_race_data['pit_stops']

    @staticmethod
    def find(query):
        return PitStops.collection.find(query)

    @staticmethod
    def find_one(query):
        return PitStops.collection.find_one(query)

class Qualifying:
    collection: Collection = db_race_data['qualifying']

    @staticmethod
    def find(query):
        return Qualifying.collection.find(query)

    @staticmethod
    def find_one(query):
        return Qualifying.collection.find_one(query)

class Races:
    collection: Collection = db_race_data['races']

    @staticmethod
    def find(query):
        return Races.collection.find(query)

    @staticmethod
    def find_one(query):
        return Races.collection.find_one(query)

class Results:
    collection: Collection = db_race_data['results']

    @staticmethod
    def find(query):
        return Results.collection.find(query)

    @staticmethod
    def find_one(query):
        return Results.collection.find_one(query)

class Seasons:
    collection: Collection = db_race_data['seasons']

    @staticmethod
    def find(query):
        return Seasons.collection.find(query)

    @staticmethod
    def find_one(query):
        return Seasons.collection.find_one(query)

class SprintResults:
    collection: Collection = db_race_data['sprint_results']

    @staticmethod
    def find(query):
        return SprintResults.collection.find(query)

    @staticmethod
    def find_one(query):
        return SprintResults.collection.find_one(query)

class Status:
    collection: Collection = db_race_data['status']

    @staticmethod
    def find(query):
        return Status.collection.find(query)

    @staticmethod
    def find_one(query):
        return Status.collection.find_one(query)

# F1_Race_Events collections

class FatalAccidentsDrivers:
    collection: Collection = db_race_events['fatal_accidents_drivers']

    @staticmethod
    def find(query):
        return FatalAccidentsDrivers.collection.find(query)

    @staticmethod
    def find_one(query):
        return FatalAccidentsDrivers.collection.find_one(query)

class FatalAccidentsMarshalls:
    collection: Collection = db_race_events['fatal_accidents_marshalls']

    @staticmethod
    def find(query):
        return FatalAccidentsMarshalls.collection.find(query)

    @staticmethod
    def find_one(query):
        return FatalAccidentsMarshalls.collection.find_one(query)

class RedFlags:
    collection: Collection = db_race_events['red_flags']

    @staticmethod
    def find(query):
        return RedFlags.collection.find(query)

    @staticmethod
    def find_one(query):
        return RedFlags.collection.find_one(query)

class SafetyCars:
    collection: Collection = db_race_events['safety_cars']

    @staticmethod
    def find(query):
        return SafetyCars.collection.find(query)

    @staticmethod
    def find_one(query):
        return SafetyCars.collection.find_one(query)

class VirtualSafetyCarEstimates:
    collection: Collection = db_race_events['virtual_safety_car_estimates']

    @staticmethod
    def find(query):
        return VirtualSafetyCarEstimates.collection.find(query)

    @staticmethod
    def find_one(query):
        return VirtualSafetyCarEstimates.collection.find_one(query)
