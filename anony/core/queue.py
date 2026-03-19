QUEUE = {}


def add(chat_id, data):

    if chat_id not in QUEUE:
        QUEUE[chat_id] = []

    QUEUE[chat_id].append(data)


def get(chat_id):

    return QUEUE.get(chat_id, [])


def pop(chat_id):

    if chat_id in QUEUE and QUEUE[chat_id]:

        return QUEUE[chat_id].pop(0)
