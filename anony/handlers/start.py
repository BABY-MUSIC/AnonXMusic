from anony import config, db, lang
from anony.api.client import client
from anony.helpers import buttons, utils


# =====================

async def start_cmd(message):

    if config.DEBUG:
        print("\n=== START CMD ===")
        print(message)

    try:

        user_id = message["from"]["id"]
        chat_id = message["chat"]["id"]

        private = message["chat"]["type"] == "private"

        if user_id in config.BL_USERS:
            if config.DEBUG:
                print("Blocked user")
            return

        # ---------- LANG ----------

        L = lang

        # ---------- TEXT ----------

        if private:

            text = L["start_pm"].format(
                message["from"]["first_name"],
                config.BOT_NAME,
            )

        else:

            text = L["start_gp"].format(
                config.BOT_NAME,
            )

        # ---------- BUTTON ----------

        markup = buttons.start_key(
            L,
            private,
        )

        # ---------- SEND ----------

        await client.request(
            "sendPhoto",
            {
                "chat_id": chat_id,
                "photo": config.START_IMG,
                "caption": text,
                "parse_mode": "HTML",   # ✅ FIX
                "reply_markup": markup,
            },
        )

        # ---------- DB ----------

        try:

            if private:

                if not await db.is_user(user_id):

                    await db.add_user(user_id)

                    await utils.send_log(message)

            else:

                if not await db.is_chat(chat_id):

                    await db.add_chat(chat_id)

                    await utils.send_log(message, True)

        except Exception as e:

            if config.DEBUG:
                print("DB ERROR:", e)

    except Exception as e:

        if config.DEBUG:
            print("START ERROR:", e)
