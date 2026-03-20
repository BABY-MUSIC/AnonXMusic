import asyncio

from anony import config

from anony.api.client import client
from anony.api.polling import polling
from anony.api.router import router

from anony.database import init_db


# =========================

async def handle_update(update):

    try:

        await router.handle(update)

    except Exception as e:

        if config.DEBUG:
            print("ROUTER ERROR:", e)


# =========================

async def run():

    print("Starting bot...")

    # ---------- MONGO ----------

    await init_db()

    print("Mongo connected")

    # ---------- BOT CLIENT ----------

    await client.start(
        token=config.BOT_TOKEN,
        api_url=config.ADMINISTER_URL,
        debug=config.DEBUG,
    )

    print("Bot started")

    # ---------- PYTGCALLS / USERBOT ----------

    try:

        await client.calls.start()

        print("PyTgCalls started")

    except Exception as e:

        print("Calls start error:", e)

    # ---------- PATCH POLLING ----------

    async def new_handle(update):

        await handle_update(update)

    polling.handle_update = new_handle

    # ---------- START POLLING ----------

    await polling.start(
        debug=config.DEBUG,
    )


# =========================

if __name__ == "__main__":

    try:

        asyncio.run(run())

    except KeyboardInterrupt:

        print("Stopped")
