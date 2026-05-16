from datetime import datetime
from database.mongo import Database

class PromptModel:
    COLLECTION_NAME = "prompts"

    @classmethod
    def get_collection(cls):
        return Database.get_db()[cls.COLLECTION_NAME]

    @classmethod
    def create_prompt(cls, prompt_id, template):
        """Creates or updates a prompt template."""
        collection = cls.get_collection()
        prompt_data = {
            "_id": prompt_id,
            "template": template,
            "createdAt": datetime.utcnow()
        }
        # Upsert: update if exists, insert if not
        collection.update_one({"_id": prompt_id}, {"$set": prompt_data}, upsert=True)
        return prompt_data

    @classmethod
    def get_prompt(cls, prompt_id):
        """Retrieves a prompt template by ID."""
        collection = cls.get_collection()
        return collection.find_one({"_id": prompt_id})
