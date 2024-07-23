from motor.motor_asyncio import AsyncIOMotorClient
from schemas.settings import Settings

settings = Settings()
client = AsyncIOMotorClient(settings.MONGO_URL)
database = client.taskdb
