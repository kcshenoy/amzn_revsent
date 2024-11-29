from werkzeug.security import generate_password_hash, check_password_hash
from flask import current_app
from flask_pymongo import PyMongo

# The 'mongo' object is automatically available after initializing PyMongo in app.py
mongo = PyMongo()

class User:
    @classmethod
    def create_user(cls, email, password):
        """
        Create a new user with the provided email and password.
        The password will be hashed before storing.
        """
        hashed_password = generate_password_hash(password)
        # Insert the user data into the MongoDB users collection
        mongo.db.users.insert_one({
            "email": email,
            "password": hashed_password
        })

    @classmethod
    def get_user_by_email(cls, email):
        """
        Get a user by email.
        """
        print(mongo.db)
        return mongo.db.users.find_one({"email": email})

    @classmethod
    def check_password(cls, email, password):
        """
        Check if the provided password matches the stored password.
        """
        user = cls.get_user_by_email(email)
        if user and check_password_hash(user['password'], password):
            return True
        return False

