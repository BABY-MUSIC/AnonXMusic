from anony import config

from anony.core.queue import (
    get,
    pop,
)

from anony.api.client import client


PLAYING = {}


# =========================
# START PLAYER
# =========================


async def start_player(chat_id):

    if chat_id in PLAYING:
        return

    data = await get(chat_id)

    if not data:
        return

    PLAYING[chat_id] = True

    await play_current(chat_id)


# =========================
# PLAY CURRENT
# =========================


async def play_current(chat_id):

    data = await get(chat_id)

    if not data:

        PLAYING.pop(chat_id, None)

        return

    stream = data["stream"]

    title = data["title"]

    print("PLAYING:", title)

    # =========================
    # HERE WILL BE VC STREAM
    # =========================

    # future:
    # await calls.stream(chat_id, stream)

    # =========================
    # START TIMER LOOP
    # =========================

    # future timer

    # await timer_loop(chat_id)


# =========================
# NEXT SONG
# =========================


async def next_song(chat_id):

    await pop(chat_id)

    data = await get(chat_id)

    if not data:

        PLAYING.pop(chat_id, None)

        return

    await play_current(chat_id)


# =========================
# STOP PLAYER
# =========================


async def stop_player(chat_id):

    PLAYING.pop(chat_id, None)

    # future leave vc

    # await calls.leave(chat_id)


# =========================
# IS PLAYING
# =========================


def is_playing(chat_id):

    return chat_id in PLAYING
