db = None
calls = None


def init_calls(database):

    global db
    global calls

    db = database

    calls = db.calls
