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
