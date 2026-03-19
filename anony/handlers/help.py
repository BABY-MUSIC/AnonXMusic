from anony import config, lang
from anony.api.client import client
from anony.helpers import buttons


# =========================
# HELP COMMAND
# =========================

async def help_cmd(message):

    if config.DEBUG:
        print("\n=== HELP CMD ===")
        print(message)

    try:

        chat_id = message["chat"]["id"]

        L = lang

        text = L["help_menu"]

        markup = buttons.help_markup(L)

        await client.request(
            "sendPhoto",
            {
                "chat_id": chat_id,
                "photo": config.START_IMG,
                "caption": text,
                "parse_mode": "HTML",
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
        print(cb)

    try:

        data = cb.get("data", "")

        chat_id = cb["message"]["chat"]["id"]
        msg_id = cb["message"]["message_id"]

        L = lang

        # ======================
        # HOME → START PAGE
        # ======================

        if data == "help home":

            name = cb["from"]["first_name"]

            text = L["start_pm"].format(
                name,
                config.BOT_NAME,
            )

            markup = buttons.start_key(
                L,
                True,
            )

            await client.request(
                "editMessageMedia",
                {
                    "chat_id": chat_id,
                    "message_id": msg_id,
                    "media": {
                        "type": "photo",
                        "media": config.START_IMG,
                        "caption": text,
                        "parse_mode": "HTML",
                    },
                    "reply_markup": markup,
                },
            )
            return

        # ======================
        # CLOSE
        # ======================

        if data == "help close":

            await client.request(
                "deleteMessage",
                {
                    "chat_id": chat_id,
                    "message_id": msg_id,
                },
            )
            return

        # ======================
        # BACK
        # ======================

        if data == "help back":

            text = L["help_menu"]

            markup = buttons.help_markup(L)

            await client.request(
                "editMessageCaption",
                {
                    "chat_id": chat_id,
                    "message_id": msg_id,
                    "caption": text,
                    "parse_mode": "HTML",
                    "reply_markup": markup,
                },
            )
            return

        # ======================
        # HELP CLICK
        # ======================

        if data == "help":

            text = L["help_menu"]

            markup = buttons.help_markup(L)

            await client.request(
                "editMessageCaption",
                {
                    "chat_id": chat_id,
                    "message_id": msg_id,
                    "caption": text,
                    "parse_mode": "HTML",
                    "reply_markup": markup,
                },
            )
            return

        # ======================
        # CATEGORY CLICK
        # ======================

        if data.startswith("help "):

            name = data.split()[1]   # admins / auth / sudo / play

            key = f"help_{name}"     # help_admins

            text = L.get(
                key,
                "No help found"
            )

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
                    "parse_mode": "HTML",
                    "reply_markup": markup,
                },
            )
            return

    except Exception as e:

        if config.DEBUG:
            print("HELP CALLBACK ERROR:", e)
