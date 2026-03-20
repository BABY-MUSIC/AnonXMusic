db = None
queue = None


def init_queue(database):

    global db
    global queue

    db = database

    queue = db.queue
