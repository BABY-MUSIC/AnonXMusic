import time

from anony import config, db
from anony.api.client import client


START_TIME = time.time()


# =========================
# STATS
# =========================

async def stats_cmd(message):

    if config.DEBUG:
        print("\n=== STATS ===")

    try:

        chat_id = message["chat"]["id"]

        users = await db.count_users()
        chats = await db.count_chats()

        uptime = int(time.time() - START_TIME)

        h = uptime // 3600
        m = (uptime % 3600) // 60
        s = uptime % 60

        up = f"{h}h {m}m {s}s"

        text = (
            "Stats\n\n"
            f"Users: {users}\n"
            f"Chats: {chats}\n"
            f"Uptime: {up}"
        )

        await client.request(
            "sendMessage",
            {
                "chat_id": chat_id,
                "text": text,
            },
        )

    except Exception as e:

        if config.DEBUG:
            print("STATS ERROR:", e)
