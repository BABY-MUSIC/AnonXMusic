import asyncio

from anony.handlers import (
    start,
    help,
    settings,
    member,
    play,
    controls,
    queue,
    ping,
    stats,
    language,
)


class Router:

    def __init__(self):

        self.debug = True


    # =========================

    async def handle(self, update):

        if self.debug:
            print("\n=== UPDATE ===")
            print(update)

        if "message" in update:
            await self.handle_message(update["message"])
            return

        if "edited_message" in update:
            await self.handle_message(update["edited_message"])
            return

        if "callback_query" in update:
            await self.handle_callback(update["callback_query"])
            return


    # =========================

    async def handle_message(self, msg):

        if self.debug:
            print("\nMESSAGE:", msg)

        text = msg.get("text", "")

        if not text:
            text = ""

        # ---------- COMMANDS ----------

        if text.startswith("/start"):
            await start.start_cmd(msg)
            return

        if text.startswith("/help"):
            await help.help_cmd(msg)
            return

        if text.startswith("/settings"):
            await settings.settings_cmd(msg)
            return

        if text.startswith("/play"):
            await play.play_cmd(msg)
            return

        if text.startswith("/pause"):
            await controls.pause_cmd(msg)
            return

        if text.startswith("/resume"):
            await controls.resume_cmd(msg)
            return

        if text.startswith("/skip"):
            await controls.skip_cmd(msg)
            return

        if text.startswith("/stop"):
            await controls.stop_cmd(msg)
            return

        if text.startswith("/queue"):
            await queue.queue_cmd(msg)
            return

        if text.startswith("/ping"):
            await ping.ping_cmd(msg)
            return

        if text.startswith("/stats"):
            await stats.stats_cmd(msg)
            return

        if text.startswith("/lang"):
            await language.lang_cmd(msg)
            return

        # ---------- NEW MEMBER ----------

        if "new_chat_members" in msg:
            await member.new_member(msg)
            return


    # =========================

    async def handle_callback(self, cb):

        if self.debug:
            print("\nCALLBACK:", cb)

        data = cb.get("data", "")

        if not data:
            return

        # ---------- CONTROLS ----------

        if data.startswith("controls"):
            await controls.callback(cb)
            return

        # ---------- HELP ----------

        if data.startswith("help"):
            await help.callback(cb)
            return

        # ---------- LANGUAGE ----------

        if data.startswith("lang"):
            await language.callback(cb)
            return

        # ---------- SETTINGS ----------

        if data.startswith("settings"):
            await settings.callback(cb)
            return

        # ---------- QUEUE ----------

        if data.startswith("queue"):
            await queue.callback(cb)
            return

        # ---------- PLAY ----------

        if data.startswith("play"):
            await play.callback(cb)
            return

        if self.debug:
            print("Unknown callback:", data)


router = Router()
