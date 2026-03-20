from anony.database import db


calls = db.calls


# =========================
# JOIN
# =========================

async def join(chat_id):

    await calls.update_one(
        {"chat_id": chat_id},
        {
            "$set": {
                "active": True
            }
        },
        upsert=True,
    )

    print("JOIN VC", chat_id)


# =========================
# STREAM
# =========================

async def stream(chat_id, stream):

    await join(chat_id)

    await calls.update_one(
        {"chat_id": chat_id},
        {
            "$set": {
                "stream": stream
            }
        },
        upsert=True,
    )

    print("STREAM", chat_id, stream)


# =========================
# LEAVE
# =========================

async def leave(chat_id):

    await calls.delete_one(
        {"chat_id": chat_id}
    )

    print("LEAVE", chat_id)


# =========================
# PAUSE
# =========================

async def pause(chat_id):

    await calls.update_one(
        {"chat_id": chat_id},
        {
            "$set": {
                "paused": True
            }
        },
    )

    print("PAUSE", chat_id)


# =========================
# RESUME
# =========================

async def resume(chat_id):

    await calls.update_one(
        {"chat_id": chat_id},
        {
            "$set": {
                "paused": False
            }
        },
    )

    print("RESUME", chat_id)


# =========================
# STATUS
# =========================

async def is_active(chat_id):

    x = await calls.find_one(
        {"chat_id": chat_id}
    )

    return bool(x)
