db = None
player = None


def init_player(database):

    global db
    global player

    db = database

    player = db.player
