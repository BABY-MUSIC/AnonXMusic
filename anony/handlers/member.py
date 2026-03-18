import asyncio

from anony import config, db
from anony.helpers import utils


# =========================
# NEW MEMBER
# =========================

async def new_member(message):

    if config.DEBUG:
        print("\n=== NEW MEMBER ===")

    try:

        if message["chat"]["type"] != "supergroup":
            return

        await asyncio.sleep(2)

        members = message.get("new_chat_members", [])

        for member in members:

            if config.DEBUG:
                print("Joined:", member)

            # bot added

            if member["id"] == config.BOT_ID:

                chat_id = message["chat"]["id"]

                if await db.is_chat(chat_id):
                    return

                await db.add_chat(chat_id)

                await utils.send_log(
                    message,
                    True,
                )

                if config.DEBUG:
                    print("Bot added to group:", chat_id)

    except Exception as e:

        if config.DEBUG:
            print("MEMBER ERROR:", e)
