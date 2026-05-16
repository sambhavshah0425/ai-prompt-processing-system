import json
from bson import ObjectId
from datetime import datetime

class MongoJSONEncoder(json.JSONEncoder):
    """
    Custom JSON Encoder that handles MongoDB ObjectIds and datetimes.
    """
    def default(self, obj):
        if isinstance(obj, ObjectId):
            return str(obj)
        if isinstance(obj, datetime):
            return obj.isoformat()
        return super().default(obj)

def parse_json(data):
    """
    Helper to convert MongoDB documents to serializable dictionaries.
    """
    return json.loads(json.dumps(data, cls=MongoJSONEncoder))
