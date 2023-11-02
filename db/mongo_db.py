import motor.motor_asyncio
from core.config import settings

MONGO_URI = settings.MONGO_URI
client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URI)
database = client[settings.MONGO_DATABASE_NAME]


def get_db():
    db = database
    return db
