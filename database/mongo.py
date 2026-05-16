from pymongo import MongoClient
from config import Config

class Database:
    client = None
    db = None

    @classmethod
    def initialize(cls):
        try:
            cls.client = MongoClient(Config.MONGO_URI, serverSelectionTimeoutMS=5000)
            # Verify connection
            cls.client.server_info()
            cls.db = cls.client[Config.DB_NAME]
            print(f"Successfully connected to MongoDB database: {Config.DB_NAME}")
        except Exception as e:
            print(f"Error connecting to MongoDB: {e}")
            raise e

    @classmethod
    def get_db(cls):
        if cls.db is None:
            cls.initialize()
        return cls.db
