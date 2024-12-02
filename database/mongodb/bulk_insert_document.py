import csv
from pymongo import MongoClient

# MongoDB connection details
mongo_host = 'mongo host'
mongo_port = 27017
mongo_db = 'db_name'
mongo_collection = 'data'

# CSV file path
csv_file_path = r'your CSV file path'

# Connect to MongoDB
client = MongoClient(mongo_host, mongo_port)
db = client[mongo_db]
collection = db[mongo_collection]

# Read CSV file and insert data into MongoDB
with open(csv_file_path, mode='r', encoding='utf-8-sig') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        collection.insert_one(row)

print("Data inserted successfully.")