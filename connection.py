from pymongo import MongoClient
MONGODB_URI = "mongodb+srv://magargame:Magarthai1@cluster0.msxpgo0.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(MONGODB_URI)

db = client.whitelist

whitelist_collection = db.list_whitelist

data = {
    "name" : "thatsamaphon boonchuntuk",
    "license" : "ABC123"
}


result = whitelist_collection.insert_one(data)

doc_id = result.inserted_id

print(doc_id)

client.close()