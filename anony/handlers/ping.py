import time

from anony import config
from anony.api.client import client


# =========================
# PING
# =========================

async def ping_cmd(message):

    if config.DEBUG:
        print("\n=== PING ===")

    try:

        chat_id = message["chat"]["id"]

        start = time.time()

        msg = await client.request(
            "sendMessage",
            {
                "chat_id": chat_id,
                "text": "Pinging...",
            },
        )

        end = time.time()

        ms = round((end - start) * 1000)

        await client.request(
            "editMessageText",
            {
                "chat_id": chat_id,
                "message_id": msg["result"]["message_id"],
                "text": f"Pong {ms} ms",
            },
        )

    except Exception as e:

        if config.DEBUG:
            print("PING ERROR:", e)
