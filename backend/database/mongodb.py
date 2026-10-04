from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")

db = client["QuantumBrainTumorDB"]

users = db["users"]

predictions = db["predictions"]

patients = db["patients"]
pending_signups = db["pending_signups"]
otps = db["otps"]

# Auto-delete expired records
pending_signups.create_index("expires_at", expireAfterSeconds=0)
otps.create_index("expires_at", expireAfterSeconds=0)

reports = db["reports"]
reports.create_index([("doctor.email", 1), ("unlocked_by", 1)])

# The referral code must be unique across all reports
reports.create_index("referral_code", unique=True)
reports.create_index("doctor_email")
reports.create_index("lab_id")