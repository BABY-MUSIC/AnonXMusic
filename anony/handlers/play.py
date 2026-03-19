from anony import config
from anony.api.client import client

from anony.core.youtube import (
    search,
    download_song,
)


# =========================
# PLAY COMMAND
# =========================

async def play_cmd(message):

    if config.DEBUG:
        print("\n=== PLAY CMD ===")

    try:

        chat_id = message["chat"]["id"]

        text = message.get("text", "")

        args = text.split(maxsplit=1)

        query = None

        # ---------- ARG ----------

        if len(args) > 1:
            query = args[1]

        # ---------- REPLY ----------

        if not query and "reply_to_message" in message:

            r = message["reply_to_message"]

            if "text" in r:
                query = r["text"]

            if "caption" in r:
                query = r["caption"]

        # ---------- EMPTY ----------

        if not query:

            await client.request(
                "sendMessage",
                {
                    "chat_id": chat_id,
                    "text": "Give song name",
                },
            )
            return

        if config.DEBUG:
            print("Query:", query)

        # ---------- LOADING ----------

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

        title = data.get("title")
        url = data.get("url")

        if config.DEBUG:
            print("FOUND:", title)

        # =========================
        # DOWNLOAD
        # =========================

        stream = await download_song(url)

        if config.DEBUG:
            print("STREAM:", stream)

        # =========================
        # RESULT
        # =========================

        await client.request(
            "editMessageText",
            {
                "chat_id": chat_id,
                "message_id": msg_id,
                "text": f"Added to queue\n\n{title}",
            },
        )

    except Exception as e:

        print("PLAY ERROR:", e)

        await client.request(
            "sendMessage",
            {
                "chat_id": chat_id,
                "text": f"Error:\n{e}",
            },
        )
