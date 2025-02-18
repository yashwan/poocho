from motor.motor_asyncio import AsyncIOMotorClient

MONGODB_URL = "mongodb://localhost:27017"
DATABASE = "poocho"
client = AsyncIOMotorClient(MONGODB_URL, serverSelectionTimeoutMS=1000)
db = client[DATABASE]