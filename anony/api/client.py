import aiohttp
import asyncio
import json


class TelegramClient:

    def __init__(self):

        self.token = None
        self.api_url = None

        self.session = None

        self.debug = True


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
            print("Client started")
            print("API:", self.api_url)


    # ------------------------

    async def stop(self):

        if self.session:
            await self.session.close()

        if self.debug:
            print("Client stopped")


    # ------------------------

    async def request(self, method, data=None):

        url = self.api_url + method

        if self.debug:
            print("\nAPI CALL:", method)
            print("DATA:", data)

        try:

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
