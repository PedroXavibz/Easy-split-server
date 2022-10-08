from pymongo.database import Database
from pymongo.mongo_client import MongoClient
from core.config import Config
from typing import Optional


class DataBase():
    DATABASE: Optional[Database] = None
    CLIENT: Optional[MongoClient] = None

    @staticmethod
    def connect():
        try:
            DataBase.CLIENT = MongoClient(host=Config.DB_URL, connect=True)
            DataBase.DATABASE = DataBase.CLIENT.get_database(
                name=Config.DB_NAME)
            print('Connected to the MongoDB database!')
        except Exception as e:
            print(e)

    @staticmethod
    def close():
        try:
            DataBase.CLIENT.close() if DataBase.CLIENT else Exception('There\' no client')
            print('Close database connection!')
        except Exception as e:
            print(e)

    @staticmethod
    def insert_one(collection: str, data):
        try:
            DataBase.DATABASE[collection].insert_one(
                data) if DataBase.DATABASE else Exception('Database connection failed')
        except Exception as e:
            print(e)

    @staticmethod
    def insert(collection: str, data):
        try:
            DataBase.DATABASE[collection].insert(data) if DataBase.DATABASE else Exception(
                'Database connection failed')
        except Exception as e:
            print(e)

    @staticmethod
    def find(collection: str, query):
        try:
            return DataBase.DATABASE[collection].find(query) if DataBase.DATABASE else Exception('Database connection failed')
        except Exception as e:
            print(e)

    @staticmethod
    def find_one(collection: str, query):
        try:
            return DataBase.DATABASE[collection].find_one(query)if DataBase.DATABASE else Exception('Database connection failed')
        except Exception as e:
            print(e)
