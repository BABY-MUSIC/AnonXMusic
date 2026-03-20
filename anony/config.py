from os import getenv
from dotenv import load_dotenv

load_dotenv()


class Config:
    def __init__(self):

        self.API_ID = int(getenv("API_ID", 16457832))
        self.API_HASH = getenv("API_HASH", "3030874d0befdb5d05597deacc3e83ab")

        self.BOT_TOKEN = getenv(
            "BOT_TOKEN",
            "8288250166:AAGM5bwNOI33FAkfC87CwAYxhMR8waU-9vg",
        )

        self.MONGO_URL = getenv(
            "MONGO_URL",
            "mongodb+srv://coder:coder@coder.htbxi.mongodb.net/?retryWrites=true&w=majority",
        )

        self.LOGGER_ID = int(getenv("LOGGER_ID", "-1002667870369"))
        self.OWNER_ID = int(getenv("OWNER_ID", "6657539971"))

        self.DURATION_LIMIT = int(getenv("DURATION_LIMIT", 60)) * 60
        self.QUEUE_LIMIT = int(getenv("QUEUE_LIMIT", 20))
        self.PLAYLIST_LIMIT = int(getenv("PLAYLIST_LIMIT", 20))

        self.SESSION1 = getenv(
            "SESSION1",
            "BQD7IGgACVw-28t6ixkUCWR5qa8-TVvmTNYuj7cWHnd9iuxKxlRCCkVvUdzwOLFtEeN7nEL-HYd79OBH22BUh4JfnIGUHrQz0XJy0iHZ-RUBH6VkcX5y8J13Z66AdQmk8pT3keKDfGHPDQUoWkbo6Q3rA0KdsAfwEm9qIXiqO24mn4vT5tM5bXUpu9HWkevmfFWUsVLNIwaJik8JG4RHZ9Bqh4G7Y9LEFG6Q4oci-mdh0195zEDNx5ygYS6UogThHkgvI31rIqWFDqzEJlrZcXwM2tbyOFcLZXI6nlhQV_V_M8MHX4pWAAIcrL3AztO2LZr5XjeXSxzerUIdl5cw2v6jv4w18gAAAAH5tqCaAA",
        )

        self.SESSION2 = getenv("SESSION2", None)
        self.SESSION3 = getenv("SESSION3", None)

        self.SUPPORT_CHANNEL = getenv(
            "SUPPORT_CHANNEL", "https://t.me/fallenx"
        )
        self.SUPPORT_CHAT = getenv(
            "SUPPORT_CHAT", "https://t.me/DevilsHeavenMF"
        )

        self.AUTO_LEAVE: bool = getenv(
            "AUTO_LEAVE", "False"
        ).lower() == "true"

        self.AUTO_END: bool = getenv(
            "AUTO_END", "False"
        ).lower() == "true"

        self.THUMB_GEN: bool = getenv(
            "THUMB_GEN", "True"
        ).lower() == "true"

        self.VIDEO_PLAY: bool = getenv(
            "VIDEO_PLAY", "True"
        ).lower() == "true"

        self.LANG_CODE = getenv("LANG_CODE", "en")

        self.COOKIES_URL = [
            url
            for url in getenv("COOKIES_URL", "").split(" ")
            if url and "batbin.me" in url
        ]

        self.DEFAULT_THUMB = getenv(
            "DEFAULT_THUMB",
            "https://te.legra.ph/file/3e40a408286d4eda24191.jpg",
        )

        self.PING_IMG = getenv(
            "PING_IMG",
            "https://files.catbox.moe/haagg2.png",
        )

        self.START_IMG = getenv(
            "START_IMG",
            "https://files.catbox.moe/zvziwk.jpg",
        )

        # =========================
        # TELEGRAM API MODE
        # =========================

        self.ADMINISTER_URL = getenv(
            "ADMINISTER_URL",
            f"https://api.telegram.org/bot{self.BOT_TOKEN}/",
        )

        self.BOT_ID = int(getenv("BOT_ID", 0))

        self.BOT_NAME = getenv("BOT_NAME", "AnonXMusic")

        self.BOT_USERNAME = getenv("BOT_USERNAME", "")

        self.API_MODE: bool = getenv(
            "API_MODE", "True"
        ).lower() == "true"

        # =========================
        # DEBUG MODE
        # =========================

        self.DEBUG: bool = getenv(
            "DEBUG", "True"
        ).lower() == "true"

        # =========================
        # BLACKLIST
        # =========================

        self.BL_USERS = [
            int(x)
            for x in getenv("BL_USERS", "").split()
            if x
        ]

    # =========================

    def check(self):

        missing = [
            var
            for var in [
                "API_ID",
                "API_HASH",
                "BOT_TOKEN",
                "MONGO_URL",
                "LOGGER_ID",
                "OWNER_ID",
                "SESSION1",
            ]
            if not getattr(self, var)
        ]

        if missing:
            raise SystemExit(
                f"Missing required environment variables: {', '.join(missing)}"
            )


config = Config()
