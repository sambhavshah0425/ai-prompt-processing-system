from datetime import datetime
from database.mongo import Database

class HistoryModel:
    COLLECTION_NAME = "history"

    @classmethod
    def get_collection(cls):
        return Database.get_db()[cls.COLLECTION_NAME]

    @classmethod
    def create_history_record(cls, request_type, user_input, final_prompt, response, batch_id=None):
        """Saves a request and response record."""
        collection = cls.get_collection()
        record = {
            "requestType": request_type,
            "userInput": user_input,
            "finalPrompt": final_prompt,
            "response": response,
            "batchId": batch_id,
            "timestamp": datetime.utcnow()
        }
        result = collection.insert_one(record)
        record["_id"] = result.inserted_id
        return record

    @classmethod
    def get_all_history(cls):
        """Retrieves all history records sorted by timestamp descending."""
        collection = cls.get_collection()
        # Find all and sort by timestamp descending (-1)
        cursor = collection.find().sort("timestamp", -1)
        return list(cursor)
