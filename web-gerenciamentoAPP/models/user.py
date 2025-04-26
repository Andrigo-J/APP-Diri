from flask_login import UserMixin
from bson import ObjectId

class User(UserMixin):
    def __init__(self, user_data):
        self.id = str(user_data['_id'])
        self.username = user_data['username']

    @staticmethod
    def from_db(user_id, usuarios_collection):
        user_data = usuarios_collection.find_one({"_id": ObjectId(user_id)})
        if user_data:
            return User(user_data)
        return None
