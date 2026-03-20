from anony.database import queue as queue_db


async def add(chat_id, data):

    await queue_db.queue.update_one(
        {"chat_id": chat_id},
        {"$push": {"songs": data}},
        upsert=True,
    )


async def get(chat_id):

    x = await queue_db.queue.find_one(
        {"chat_id": chat_id}
    )

    if not x:
        return None

    songs = x.get("songs", [])

    if not songs:
        return None

    return songs[0]


async def pop(chat_id):

    await queue_db.queue.update_one(
        {"chat_id": chat_id},
        {"$pop": {"songs": -1}},
    )


async def clear(chat_id):

    await queue_db.queue.delete_one(
        {"chat_id": chat_id}
    )
