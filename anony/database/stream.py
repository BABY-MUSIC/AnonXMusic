from motor.motor_asyncio import AsyncIOMotorDatabase

db: AsyncIOMotorDatabase = None

stream = None


def init_stream(database):

    global db
    global stream

    db = database

    stream = db.stream
