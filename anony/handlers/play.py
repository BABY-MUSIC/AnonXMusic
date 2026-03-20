from anony import config

from anony.api.client import client

from anony.core.youtube import (
    search,
    download_song,
)

from anony.core.queue import (
    add,
    get,
)

from anony.core.player import start_player

from anony.core.thumbs import gen_thumb

from anony.helpers.buttons import play_buttons

from anony.lang import get_string


# =========================
# PLAY COMMAND
# =========================


async def play_cmd(message):

    try:

        chat_id = message["chat"]["id"]

        user = message["from"]["first_name"]

        text = message.get("text", "")

        args = text.split(maxsplit=1)

        query = None

        # ---------- arg ----------

        if len(args) > 1:
            query = args[1]

        # ---------- reply ----------

        if not query and "reply_to_message" in message:

            r = message["reply_to_message"]

            query = r.get("text") or r.get("caption")

        # ---------- empty ----------

        if not query:

            await client.request(
                "sendMessage",
                {
                    "chat_id": chat_id,
                    "text": "Give song name",
                },
            )
            return

        # ---------- loading ----------

        msg = await client.request(
            "sendMessage",
            {
                "chat_id": chat_id,
                "text": "Searching...",
            },
        )

        msg_id = msg["result"]["message_id"]

        # =========================
        # SEARCH
        # =========================

        data = await search(query)

        title = data["title"]

        url = data["url"]

        vidid = url.split("v=")[-1]

        # =========================
        # DOWNLOAD
        # =========================

        stream = await download_song(url)

        # =========================
        # QUEUE ADD
        # =========================

        pos = await add(
            chat_id,
            {
                "title": title,
                "url": url,
                "stream": stream,
                "vidid": vidid,
                "user": user,
            },
        )

        # ---------- queue message ----------

        if pos and pos > 1:

            await client.request(
                "editMessageText",
                {
                    "chat_id": chat_id,
                    "message_id": msg_id,
                    "text": f"Added to queue #{pos}\n\n{title}",
                },
            )

            return

        # =========================
        # FIRST SONG
        # =========================

        thumb, info = await gen_thumb(vidid)

        # ✅ SAFE DURATION

        duration = "0"

        if info and isinstance(info, dict):
            duration = info.get("duration") or "0"

        lang = get_string("play_media")

        caption = lang.format(
            url,
            title,
            duration,
            user,
        )

        caption += "\n<b>Made by:</b> @YourChannel"

        # delete loading

        await client.request(
            "deleteMessage",
            {
                "chat_id": chat_id,
                "message_id": msg_id,
            },
        )

        # send player message

        sent = await client.request(
            "sendPhoto",
            {
                "chat_id": chat_id,
                "photo": thumb,
                "caption": caption,
                "parse_mode": "HTML",
                "reply_markup": play_buttons(),
            },
        )

        player_msg = sent["result"]["message_id"]

        config.PLAYER_MSG[chat_id] = player_msg

        # =========================
        # START PLAYER
        # =========================

        await start_player(chat_id)

    except Exception as e:

        print("PLAY ERROR:", e)

        await client.request(
            "sendMessage",
            {
                "chat_id": chat_id,
                "text": str(e),
            },
        )
