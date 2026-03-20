from pytgcalls.types.stream.media_stream import MediaStream
from pytgcalls.exceptions import NoActiveGroupCall

from anony.api.client import client
from anony.database import db


calls = db.calls


# =========================
# JOIN
# =========================

async def join(chat_id):

    try:

        await client.calls.join_group_call(
            chat_id,
            MediaStream("silence.mp3"),
        )

    except NoActiveGroupCall:

        print("No active VC")

    await calls.update_one(
        {"chat_id": chat_id},
        {"$set": {"active": True}},
        upsert=True,
    )


# =========================
# STREAM
# =========================

async def stream(chat_id, file):

    try:

        await client.calls.change_stream(
            chat_id,
            MediaStream(file),
        )

    except Exception:

        await join(chat_id)

        await client.calls.change_stream(
            chat_id,
            MediaStream(file),
        )

    await calls.update_one(
        {"chat_id": chat_id},
        {"$set": {"stream": file}},
        upsert=True,
    )


# =========================
# LEAVE
# =========================

async def leave(chat_id):

    try:
        await client.calls.leave_group_call(chat_id)
    except:
        pass

    await calls.delete_one(
        {"chat_id": chat_id}
    )


# =========================
# PAUSE
# =========================

async def pause(chat_id):

    try:
        await client.calls.pause_stream(chat_id)
    except:
        pass


# =========================
# RESUME
# =========================

async def resume(chat_id):

    try:
        await client.calls.resume_stream(chat_id)
    except:
        pass


# =========================
# MUTE
# =========================

async def mute(chat_id):

    try:
        await client.calls.mute_stream(chat_id)
    except:
        pass


# =========================
# UNMUTE
# =========================

async def unmute(chat_id):

    try:
        await client.calls.unmute_stream(chat_id)
    except:
        pass
