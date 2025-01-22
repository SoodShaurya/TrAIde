import logging

from pymongo import MongoClient

def initialize_mongodb(port):
    # Initialize MongoDB connection
    logging.info("Initializing MongoDB connection.")
    client = MongoClient(f"mongodb://localhost:{port}")  # Replace with your connection string
    db = client["global"]  # Database name
    collection = db["posts"]  # Collection name
    return collection