from anony import config
from anony.api.client import client

from anony.core.player import play


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

        # ---------- PLAYER ----------

        data, first = await play(chat_id, query)

        title = data.get("title", "Unknown")

        if first:
            text = f"Playing:\n{title}"
        else:
            text = f"Added to queue:\n{title}"

        # ---------- EDIT ----------

        await client.request(
            "editMessageText",
            {
                "chat_id": chat_id,
                "message_id": msg["result"]["message_id"],
                "text": text,
            },
        )

    except Exception as e:

        if config.DEBUG:
            print("PLAY ERROR:", e)
