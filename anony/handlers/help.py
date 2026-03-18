from anony import config
from anony.api.client import client
from anony.helpers import buttons


# =========================
# HELP COMMAND
# =========================

async def help_cmd(message):

    if config.DEBUG:
        print("\n=== HELP CMD ===")

    try:

        if message["chat"]["type"] != "private":
            return

        chat_id = message["chat"]["id"]

        text = message["lang"]["help_menu"]

        markup = buttons.help_markup(
            message["lang"]
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
            print("HELP ERROR:", e)


# =========================
# HELP CALLBACK
# =========================

async def callback(cb):

    if config.DEBUG:
        print("\n=== HELP CALLBACK ===")

    try:

        data = cb.get("data", "")

        chat_id = cb["message"]["chat"]["id"]
        msg_id = cb["message"]["message_id"]

        text = cb["message"]["text"]

        if data == "help close":

            await client.request(
                "deleteMessage",
                {
                    "chat_id": chat_id,
                    "message_id": msg_id,
                },
            )

            return

        if data == "help back":

            markup = buttons.help_markup(
                cb["lang"]
            )

            await client.request(
                "editMessageReplyMarkup",
                {
                    "chat_id": chat_id,
                    "message_id": msg_id,
                    "reply_markup": markup,
                },
            )

            return

        # other help pages

        markup = buttons.help_markup(
            cb["lang"],
            back=True,
        )

        await client.request(
            "editMessageReplyMarkup",
            {
                "chat_id": chat_id,
                "message_id": msg_id,
                "reply_markup": markup,
            },
        )

    except Exception as e:

        if config.DEBUG:
            print("HELP CALLBACK ERROR:", e)
