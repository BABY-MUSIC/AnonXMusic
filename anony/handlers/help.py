import json

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
                "reply_markup": json.dumps(markup),
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

        L = cb["lang"]

        # CLOSE

        if data == "help close":

            await client.request(
                "deleteMessage",
                {
                    "chat_id": chat_id,
                    "message_id": msg_id,
                },
            )
            return

        # BACK

        if data == "help back":

            text = L["help_menu"]

            markup = buttons.help_markup(L)

            await client.request(
                "editMessageCaption",
                {
                    "chat_id": chat_id,
                    "message_id": msg_id,
                    "caption": text,
                    "reply_markup": json.dumps(markup),
                },
            )
            return

        # OTHER HELP PAGE

        text = L["help_page"]

        markup = buttons.help_markup(
            L,
            back=True,
        )

        await client.request(
            "editMessageCaption",
            {
                "chat_id": chat_id,
                "message_id": msg_id,
                "caption": text,
                "reply_markup": json.dumps(markup),
            },
        )

    except Exception as e:

        if config.DEBUG:
            print("HELP CALLBACK ERROR:", e)
