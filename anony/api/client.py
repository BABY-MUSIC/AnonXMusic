import aiohttp
import asyncio
import json

from pyrogram import Client as PyroClient
from pytgcalls import PyTgCalls

from anony import config


class TelegramClient:

    def __init__(self):

        self.token = None
        self.api_url = None

        self.session = None

        self.debug = True

        # bot api session
        self.bot = None

        # userbot
        self.user = None

        # pytgcalls
        self.calls = None

    # ------------------------

    async def start(self, token, api_url=None, debug=True):

        self.token = token

        if api_url:
            self.api_url = api_url
        else:
            self.api_url = f"https://api.telegram.org/bot{token}/"

        self.debug = debug

        self.session = aiohttp.ClientSession()

        if self.debug:
            print("Bot API started")

        # =========================
        # USERBOT START
        # =========================

        self.user = PyroClient(
            "assistant",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            session_string=config.SESSION,
        )

        await self.user.start()

        print("Assistant started")

        # =========================
        # PYTGCALLS
        # =========================

        self.calls = PyTgCalls(self.user)

        await self.calls.start()

        print("PyTgCalls started")

    # ------------------------

    async def stop(self):

        if self.session:
            await self.session.close()

        if self.user:
            await self.user.stop()

        if self.calls:
            await self.calls.stop()

        if self.debug:
            print("Client stopped")

    # ------------------------

    async def request(self, method, data=None):

        url = self.api_url + method

        if self.debug:
            print("\nAPI CALL:", method)
            print("DATA:", data)

        try:

            # =========================
            # FILE REQUEST SUPPORT
            # =========================

            if data:

                file_key = None

                for k, v in data.items():
                    if hasattr(v, "read"):
                        file_key = k
                        break

                if file_key:

                    file = data.pop(file_key)

                    form = aiohttp.FormData()

                    for k, v in data.items():
                        form.add_field(k, str(v))

                    form.add_field(
                        file_key,
                        file,
                        filename="file",
                        content_type="application/octet-stream",
                    )

                    async with self.session.post(
                        url,
                        data=form,
                        timeout=60,
                    ) as resp:

                        text = await resp.text()

                        if self.debug:
                            print("RESP:", text)

                        try:
                            return json.loads(text)
                        except:
                            return text

            # =========================
            # NORMAL JSON REQUEST
            # =========================

            async with self.session.post(
                url,
                json=data,
                timeout=30,
            ) as resp:

                text = await resp.text()

                if self.debug:
                    print("RESP:", text)

                try:
                    return json.loads(text)
                except:
                    return text

        except Exception as e:

            if self.debug:
                print("API ERROR:", e)

            return None


# global client

client = TelegramClient()
