from .queue import add, get
from .youtube import search


async def play(chat_id, query):

    data = search(query)

    add(chat_id, data)

    queue = get(chat_id)

    first = len(queue) == 1

    return data, first
