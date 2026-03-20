db = None
queue = None


def init_queue(database):

    global db
    global queue

    print("INIT_QUEUE CALLED")

    db = database

    print("DB =", db)

    queue = db.queue

    print("QUEUE =", queue)
