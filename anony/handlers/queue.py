from anony import config
from anony.api.client import client
from anony.helpers import buttons


# =========================
# QUEUE
# =========================

async def queue_cmd(message):

    if config.DEBUG:
        print("\n=== QUEUE ===")

    try:

        chat_id = message["chat"]["id"]

        # future queue list
        queue_list = []

        if not queue_list:

            await client.request(
                "sendMessage",
                {
                    "chat_id": chat_id,
                    "text": "Queue empty",
                },
            )

            return

        text = "Queue:\n\n"

        for i, item in enumerate(queue_list, 1):

            text += f"{i}. {item}\n"

        markup = buttons.queue_markup(
            chat_id,
            "Pause",
            True,
        )

        await client.request(
            "sendMessage",
            {
                "chat_id": chat_id,
                "text": text,
                "reply_markup": markup,
            },
        )

    except Exception as e:

        if config.DEBUG:
            print("QUEUE ERROR:", e)
