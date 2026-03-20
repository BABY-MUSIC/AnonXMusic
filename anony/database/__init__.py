from motor.motor_asyncio import AsyncIOMotorClient

from anony import config

from .stream import init_stream
from .player import init_player
from .calls import init_calls
from .queue import init_queue


db = None


async def init_db():

    global db

    client = AsyncIOMotorClient(config.MONGO_URL)

    db = client.anony

    init_stream(db)
    init_player(db)
    init_calls(db)
    init_queue(db)
