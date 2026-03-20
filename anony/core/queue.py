from anony.database import queue



# =========================
# ADD
# =========================

async def add(chat_id, data):

    await queue.update_one(
        {"chat_id": chat_id},
        {"$push": {"songs": data}},
        upsert=True,
    )


# =========================
# GET CURRENT
# =========================

async def get(chat_id):

    x = await queue.find_one(
        {"chat_id": chat_id}
    )

    if not x:
        return None

    songs = x.get("songs", [])

    if not songs:
        return None

    return songs[0]


# =========================
# POP FIRST
# =========================

async def pop(chat_id):

    await queue.update_one(
        {"chat_id": chat_id},
        {"$pop": {"songs": -1}},
    )


# =========================
# GET FULL QUEUE (optional)
# =========================

async def get_all(chat_id):

    x = await queue.find_one(
        {"chat_id": chat_id}
    )

    if not x:
        return []

    return x.get("songs", [])


# =========================
# CLEAR
# =========================

async def clear(chat_id):

    await queue.delete_one(
        {"chat_id": chat_id}
    )
