from anony import config, lang


# =========================
# BASE
# =========================

def build(rows):

    return {
        "inline_keyboard": rows
    }


def btn(text, callback=None, url=None):

    b = {"text": text}

    if callback:
        b["callback_data"] = callback

    if url:
        b["url"] = url

    return b


# =========================
# START
# =========================

def start_key(_lang, private=False):

    rows = [

        [
            btn(
                _lang["add_me"],
                url=f"https://t.me/{config.BOT_USERNAME}?startgroup=true",
            )
        ],

        [
            btn(
                _lang["help"],
                callback="help",
            )
        ],

        [
            btn(
                _lang["support"],
                url=config.SUPPORT_CHAT,
            ),
            btn(
                _lang["channel"],
                url=config.SUPPORT_CHANNEL,
            ),
        ],
    ]

    if private:

        rows.append(
            [
                btn(
                    _lang["source"],
                    url="https://github.com/",
                )
            ]
        )

    else:

        rows.append(
            [
                btn(
                    _lang["language"],
                    callback="lang",
                )
            ]
        )

    return build(rows)


# =========================
# HELP
# =========================

def help_markup(_lang, back=False):

    if back:

        rows = [
            [
                btn(_lang["back"], "help back"),
                btn(_lang["close"], "help close"),
            ]
        ]

        return build(rows)

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
                _lang[f"help_{i}"],
                f"help {cb}",
            )
        )

    rows = [
        buttons[i:i+3]
        for i in range(0, len(buttons), 3)
    ]

    return build(rows)


# =========================
# SETTINGS
# =========================

def settings_markup(
    _lang,
    admin_only,
    cmd_delete,
    language,
    chat_id,
):

    rows = [

        [
            btn(
                _lang["play_mode"] + " ➜",
                "settings",
            ),
            btn(
                str(admin_only),
                "settings play",
            ),
        ],

        [
            btn(
                _lang["cmd_delete"] + " ➜",
                "settings",
            ),
            btn(
                str(cmd_delete),
                "settings delete",
            ),
        ],

        [
            btn(
                _lang["language"] + " ➜",
                "settings",
            ),
            btn(
                language,
                "lang",
            ),
        ],
    ]

    return build(rows)


# =========================
# LANG
# =========================

def lang_markup(current):

    langs = lang.get_languages()

    buttons = []

    for code, name in langs.items():

        text = f"{name} ({code})"

        if code == current:
            text += " ✔️"

        buttons.append(
            btn(
                text,
                f"lang_change {code}",
            )
        )

    rows = [
        buttons[i:i+2]
        for i in range(0, len(buttons), 2)
    ]

    return build(rows)


# =========================
# QUEUE
# =========================

def queue_markup(chat_id, text, playing):

    action = "pause" if playing else "resume"

    rows = [
        [
            btn(
                text,
                f"controls {action} {chat_id}",
            )
        ]
    ]

    return build(rows)
