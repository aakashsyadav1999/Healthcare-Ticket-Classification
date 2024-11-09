import csv
from pymongo import MongoClient

# MongoDB connection details
mongo_host = 'mongodb+srv://skyrayzor1:SCg11DiLjLwBZCAS@health.pwap2.mongodb.net/'
mongo_port = 27017
mongo_db = 'health_care'
mongo_collection = 'data'

# CSV file path
csv_file_path = r'D:\vscode\Healthcare-Ticket-Classification\data\final_csv\final.csv'

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