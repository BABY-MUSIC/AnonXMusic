from anony import config


# =====================

def start_key(lang, private: bool):

    if private:

        keyboard = [
            [
                {
                    "text": lang["add_me"],
                    "url": f"https://t.me/{config.BOT_NAME}?startgroup=true",
                }
            ],
            [
                {
                    "text": lang["support"],
                    "url": config.SUPPORT_CHAT,
                },
                {
                    "text": lang["help"],
                    "callback_data": "help",
                },
            ],
        ]

    else:

        keyboard = [
            [
                {
                    "text": lang["support"],
                    "url": config.SUPPORT_CHAT,
                }
            ]
        ]

    return {
        "inline_keyboard": keyboard
    }


# =========================
# HELP
# =========================

def help_markup(_lang, back=False):

    def btn(text, callback=None, url=None):

        b = {"text": text}

        if callback:
            b["callback_data"] = callback

        if url:
            b["url"] = url

        return b

    def build(rows):

        return {
            "inline_keyboard": rows
        }

    # BACK PAGE

    if back:

        rows = [
            [
                btn("Back", "help back"),
                btn("Close", "help close"),
            ],
            [
                btn("Home", "help home"),
            ],
        ]

        return build(rows)

    # CATEGORY PAGE

    cbs = [
        "admins",
        "auth",
        "blist",
        "lang",
        "ping",
        "play",
        "queue",
        "stats",
        "sudo",
    ]

    buttons = []

    for i, cb in enumerate(cbs):

        buttons.append(
            btn(
                _lang.get(f"help_{i}", cb),
                f"help {cb}",
            )
        )

    rows = [
        buttons[i:i+3]
        for i in range(0, len(buttons), 3)
    ]

    # last row home

    rows.append(
        [
            btn("Home", "help home"),
            btn("Close", "help close"),
        ]
    )

    return build(rows)


# =========================
# PLAYER MARKUP
# =========================

def play_buttons(
    duration,
    chat_id,
):

    def btn(text, cb):

        return {
            "text": text,
            "callback_data": cb,
        }

    def build(rows):

        return {
            "inline_keyboard": rows
        }

    # ---------- TIMER BAR ----------

    bar_len = 10

    current = 0

    total = int(duration) if duration else 1

    if total == 0:
        total = 1

    pos = int((current / total) * bar_len)

    bar = "━" * pos + "●" + "─" * (bar_len - pos)

    timer = f"{current}s {bar} {total}s"


    # ---------- BUTTONS ----------

    rows = [

        # timer row
        [
            {
                "text": timer,
                "callback_data": f"player none {chat_id}",
            }
        ],

        # controls
        [
            btn("⏮", f"player prev {chat_id}"),
            btn("⏯", f"player pause {chat_id}"),
            btn("⏭", f"player next {chat_id}"),
            btn("🔈", f"player mute {chat_id}"),
        ],

        # close
        [
            btn("✖", f"player close {chat_id}"),
        ],
    ]

    return build(rows)
