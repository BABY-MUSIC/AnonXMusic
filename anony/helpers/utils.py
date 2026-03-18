def get_user(update):
    if 'message' in update:
        return update['message']['from']['id']
    if 'callback_query' in update:
        return update['callback_query']['from']['id']
    return None
