from pytgcalls import PyTgCalls
from pytgcalls.types import AudioPiped
from pytgcalls.exceptions import NoActiveGroupCall

from anony.api.client import userbot
from anony.database import db


calls_db = db.calls

calls = None


# =========================
# START CALLS
# =========================

async def start_calls():

    global calls

    calls = PyTgCalls(userbot)

    await calls.start()

    print("PyTgCalls started")


# =========================
# JOIN
# =========================

async def join(chat_id):

    try:

        await calls.join_group_call(
            chat_id,
            AudioPiped("silence.mp3"),
        )

    except NoActiveGroupCall:

        print("No active VC")

    await calls_db.update_one(
        {"chat_id": chat_id},
        {"$set": {"active": True}},
        upsert=True,
    )


# =========================
# STREAM
# =========================

async def stream(chat_id, file):

    try:

        await calls.change_stream(
            chat_id,
            AudioPiped(file),
        )

    except Exception:

        await join(chat_id)

        await calls.change_stream(
            chat_id,
            AudioPiped(file),
        )

    await calls_db.update_one(
        {"chat_id": chat_id},
        {"$set": {"stream": file}},
        upsert=True,
    )


# =========================
# LEAVE
# =========================

async def leave(chat_id):

    try:
        await calls.leave_group_call(chat_id)
    except:
        pass

    await calls_db.delete_one(
        {"chat_id": chat_id}
    )


# =========================
# PAUSE
# =========================

async def pause(chat_id):

    try:
        await calls.pause_stream(chat_id)
    except:
        pass


# =========================
# RESUME
# =========================

async def resume(chat_id):

    try:
        await calls.resume_stream(chat_id)
    except:
        pass


# =========================
# MUTE
# =========================

async def mute(chat_id):

    try:
        await calls.mute_stream(chat_id)
    except:
        pass


# =========================
# UNMUTE
# =========================

async def unmute(chat_id):

    try:
        await calls.unmute_stream(chat_id)
    except:
        pass
