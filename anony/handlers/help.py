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

        private = message["chat"]["type"] == "private"

        # ---------- LANG ----------

        L = lang

        # ---------- TEXT ----------

        text = L["help_menu"]

        # ---------- BUTTON ----------

        markup = buttons.help_markup(L)

        # ---------- SEND ----------

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

        # ---------- LANG ----------

        L = lang

        # -----------------
        # CLOSE
        # -----------------

        if data == "help close":

            await client.request(
                "deleteMessage",
                {
                    "chat_id": chat_id,
                    "message_id": msg_id,
                },
            )
            return

        # -----------------
        # BACK
        # -----------------

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

        # -----------------
        # OTHER PAGE
        # -----------------

        if data.startswith("help"):

            text = L["help_menu"]

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
