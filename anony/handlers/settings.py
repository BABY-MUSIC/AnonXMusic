from anony import config, db
from anony.api.client import client
from anony.helpers import buttons


# =========================
# SETTINGS COMMAND
# =========================

async def settings_cmd(message):

    if config.DEBUG:
        print("\n=== SETTINGS CMD ===")

    try:

        chat_id = message["chat"]["id"]

        admin_only = await db.get_play_mode(chat_id)
        cmd_delete = await db.get_cmd_delete(chat_id)
        _language = await db.get_lang(chat_id)

        text = message["lang"]["start_settings"].format(
            message["chat"]["title"]
        )

        markup = buttons.settings_markup(
            message["lang"],
            admin_only,
            cmd_delete,
            _language,
            chat_id,
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
            print("SETTINGS ERROR:", e)


# =========================
# CALLBACK
# =========================

async def callback(cb):

    if config.DEBUG:
        print("\n=== SETTINGS CALLBACK ===")

    try:

        data = cb.get("data", "")

        chat_id = cb["message"]["chat"]["id"]
        msg_id = cb["message"]["message_id"]

        parts = data.split()

        if len(parts) < 2:
            return

        action = parts[1]

        # ---------- PLAY MODE ----------

        if action == "play":

            current = await db.get_play_mode(chat_id)

            new = not current

            await db.set_play_mode(chat_id, new)

        # ---------- DELETE ----------

        if action == "delete":

            current = await db.get_cmd_delete(chat_id)

            new = not current

            await db.set_cmd_delete(chat_id, new)

        # ---------- LANGUAGE ----------

        if action == "lang":
            return

        # ---------- REFRESH ----------

        admin_only = await db.get_play_mode(chat_id)
        cmd_delete = await db.get_cmd_delete(chat_id)
        _language = await db.get_lang(chat_id)

        markup = buttons.settings_markup(
            cb["lang"],
            admin_only,
            cmd_delete,
            _language,
            chat_id,
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
            print("SETTINGS CALLBACK ERROR:", e)
