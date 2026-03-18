from anony import config, db, lang
from anony.api.client import client
from anony.helpers import buttons


# =========================
# /lang command
# =========================

async def lang_cmd(message):

    if config.DEBUG:
        print("\n=== LANG CMD ===")

    try:

        chat_id = message["chat"]["id"]

        current = await db.get_lang(chat_id)

        markup = buttons.lang_markup(current)

        await client.request(
            "sendMessage",
            {
                "chat_id": chat_id,
                "text": "Select language",
                "reply_markup": markup,
            },
        )

    except Exception as e:

        if config.DEBUG:
            print("LANG CMD ERROR:", e)


# =========================
# CALLBACK
# =========================

async def callback(cb):

    if config.DEBUG:
        print("\n=== LANG CALLBACK ===")

    try:

        data = cb.get("data", "")

        chat_id = cb["message"]["chat"]["id"]
        msg_id = cb["message"]["message_id"]

        parts = data.split()

        if len(parts) < 2:
            return

        action = parts[0]

        if action != "lang_change":
            return

        code = parts[1]

        await db.set_lang(chat_id, code)

        markup = buttons.lang_markup(code)

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
            print("LANG CALLBACK ERROR:", e)
