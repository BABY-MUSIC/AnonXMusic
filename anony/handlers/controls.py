from anony import config
from anony.api.client import client


# =========================
# PAUSE
# =========================

async def pause_cmd(message):

    if config.DEBUG:
        print("\n=== PAUSE ===")

    chat_id = message["chat"]["id"]

    await client.request(
        "sendMessage",
        {
            "chat_id": chat_id,
            "text": "Paused",
        },
    )


# =========================
# RESUME
# =========================

async def resume_cmd(message):

    if config.DEBUG:
        print("\n=== RESUME ===")

    chat_id = message["chat"]["id"]

    await client.request(
        "sendMessage",
        {
            "chat_id": chat_id,
            "text": "Resumed",
        },
    )


# =========================
# SKIP
# =========================

async def skip_cmd(message):

    if config.DEBUG:
        print("\n=== SKIP ===")

    chat_id = message["chat"]["id"]

    await client.request(
        "sendMessage",
        {
            "chat_id": chat_id,
            "text": "Skipped",
        },
    )


# =========================
# STOP
# =========================

async def stop_cmd(message):

    if config.DEBUG:
        print("\n=== STOP ===")

    chat_id = message["chat"]["id"]

    await client.request(
        "sendMessage",
        {
            "chat_id": chat_id,
            "text": "Stopped",
        },
    )


# =========================
# CALLBACK
# =========================

async def callback(cb):

    if config.DEBUG:
        print("\n=== CONTROL CALLBACK ===")

    data = cb.get("data", "")

    chat_id = cb["message"]["chat"]["id"]

    parts = data.split()

    if len(parts) < 2:
        return

    action = parts[1]

    if action == "pause":

        await client.request(
            "sendMessage",
            {
                "chat_id": chat_id,
                "text": "Paused",
            },
        )

    elif action == "resume":

        await client.request(
            "sendMessage",
            {
                "chat_id": chat_id,
                "text": "Resumed",
            },
        )

    elif action == "skip":

        await client.request(
            "sendMessage",
            {
                "chat_id": chat_id,
                "text": "Skipped",
            },
        )

    elif action == "stop":

        await client.request(
            "sendMessage",
            {
                "chat_id": chat_id,
                "text": "Stopped",
            },
        )
