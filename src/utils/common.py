
import os
import sys
import json
from pymongo import MongoClient


# CommonUtils class to handle MongoDB connection
class CommonUtils:
    def __init__(self):
        # Read MongoDB connection details from environment variables
        mongo_host = os.getenv("MONGODB_URI")
        mongo_port = int(os.getenv("MONGODB_PORT"))
        mongo_db = os.getenv("MONGODB")
        
        # Initialize the MongoDB client and database connection
        self.client = MongoClient(mongo_host, mongo_port)
        self.db = self.client[mongo_db]

    def insert_main_table(self):
        # Use the initialized database connection
        mongo_collection = os.getenv("MONGO_COLLECTION")
        collection = self.db[mongo_collection]
        return collection

    def insert_into_urgency_table(self):
        # Use the initialized database connection
        mongo_collection = os.getenv("URGENCY_TABLE")
        collection = self.db[mongo_collection]
        return collection
    
    def insert_into_video_table(self):
        # Use the initialized database connection
        mongo_collection = os.getenv("MONGO_VIDEO_LINK_TABLE")
        collection = self.db[mongo_collection]
        return collection
    
    def close(self):
        # Close the MongoDB client connection
        self.client.close()
            
            
