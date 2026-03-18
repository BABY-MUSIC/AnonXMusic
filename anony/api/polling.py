import asyncio

from anony.api.client import client


class Polling:

    def __init__(self):

        self.offset = 0

        self.running = False

        self.debug = True


    # -------------------------

    async def start(self, debug=True):

        self.debug = debug

        self.running = True

        if self.debug:
            print("Polling started")

        while self.running:

            try:

                data = await client.request(
                    "getUpdates",
                    {
                        "timeout": 30,
                        "offset": self.offset,
                    },
                )

                if not data:
                    continue

                if not data.get("ok"):
                    continue

                updates = data.get("result", [])

                for upd in updates:

                    self.offset = upd["update_id"] + 1

                    await self.handle_update(upd)

            except Exception as e:

                if self.debug:
                    print("Polling error:", e)

                await asyncio.sleep(1)


    # -------------------------

    async def stop(self):

        self.running = False

        if self.debug:
            print("Polling stopped")


    # -------------------------

    async def handle_update(self, update):

        if self.debug:
            print("Update:", update)


polling = Polling()
