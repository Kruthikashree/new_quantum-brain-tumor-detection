from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")

db = client["QuantumBrainTumorDB"]

users = db["users"]

predictions = db["predictions"]