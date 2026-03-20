from anony.core.queue import get, pop
from anony.core.calls import stream, leave

from anony.database import player



# =========================
# START PLAYER
# =========================

async def start_player(chat_id):

    data = await get(chat_id)

    if not data:
        return

    await player.update_one(
        {"chat_id": chat_id},
        {"$set": {"playing": True}},
        upsert=True,
    )

    await play_current(chat_id)


# =========================
# PLAY CURRENT
# =========================

async def play_current(chat_id):

    data = await get(chat_id)

    if not data:

        await stop_player(chat_id)
        return

    file = data.get("stream")
    title = data.get("title")

    print("PLAY:", title)

    try:

        await stream(chat_id, file)

    except Exception as e:

        print("STREAM ERROR:", e)

        await stop_player(chat_id)
        return

    await player.update_one(
        {"chat_id": chat_id},
        {"$set": {"current": data}},
        upsert=True,
    )


# =========================
# NEXT SONG
# =========================

async def next_song(chat_id):

    await pop(chat_id)

    data = await get(chat_id)

    if not data:

        await stop_player(chat_id)
        return

    await play_current(chat_id)


# =========================
# STOP
# =========================

async def stop_player(chat_id):

    try:
        await leave(chat_id)
    except:
        pass

    await player.delete_one(
        {"chat_id": chat_id}
    )


# =========================
# STATUS
# =========================

async def is_playing(chat_id):

    x = await player.find_one(
        {"chat_id": chat_id}
    )

    if not x:
        return False

    return x.get("playing", False)


# =========================
# GET CURRENT
# =========================

async def get_current(chat_id):

    x = await player.find_one(
        {"chat_id": chat_id}
    )

    if not x:
        return None

    return x.get("current")
