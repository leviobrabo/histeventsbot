from historicalevents.database.db import *


def sudos(user_id):
    user = search_user(user_id)
    if user and user.get('sudo') == 'true':
        return True
    return False
