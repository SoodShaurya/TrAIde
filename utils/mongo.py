import logging

from pymongo import MongoClient


def initialize_mongodb():
    # Initialize MongoDB connection
    logging.info("Initializing MongoDB connection.")
    client = MongoClient("mongodb://localhost:27017")  # Replace with your connection string
    db = client["global"]  # Database name
    collection = db["posts"]  # Collection name
    return collection