from pymongo import MongoClient
from datetime import datetime

MONGODB_URI = "mongodb+srv://magargame:Magarthai1@cluster0.msxpgo0.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(MONGODB_URI)

db = client.whitelist

whitelist_collection = db.list_whitelists

data = {
    "name": "thatsamaphon boonchuntuk",
    "license": "ABC123",
    "createdAt": datetime.utcnow(), 
    "updatedAt": datetime.utcnow() 
}

result = whitelist_collection.insert_one(data)

doc_id = result.inserted_id

print(doc_id)

client.close()
