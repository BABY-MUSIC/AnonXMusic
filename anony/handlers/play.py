from anony import config
from anony.api.client import client
from anony.helpers import buttons


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

        # ---------- TODO PLAYER ----------

        # future:
        # search
        # download
        # stream
        # queue

        await client.request(
            "editMessageText",
            {
                "chat_id": chat_id,
                "message_id": msg["result"]["message_id"],
                "text": f"Added to queue:\n{query}",
            },
        )

    except Exception as e:

        if config.DEBUG:
            print("PLAY ERROR:", e)
