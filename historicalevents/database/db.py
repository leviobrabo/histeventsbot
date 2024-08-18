from pymongo import ASCENDING, MongoClient

from historicalevents.config import MONGO_CON
from historicalevents.loggers import logger

try:

    logger.info('ℹ️ INITIATING CONNECTION WITH MONGODB')

    client = MongoClient(MONGO_CON)
    db = client.historicalevents
    logger.success('✅ Connection to MongoDB established successfully!')

except Exception as e:
    logger.error(f'❗️ Error connecting to MongoDB: {e}')


# User related operations


def add_user_db(message):
    first_name = message.from_user.first_name
    last_name = str(message.from_user.last_name).replace('None', '')
    username = str(message.from_user.username).replace('None', '')
    return db.users.insert_one(
        {
            'user_id': message.from_user.id,
            'first_name': first_name,
            'last_name': last_name,
            'username': username,
            'sudo': 'false',
            'msg_private': 'true',
            'message_id': '',
            'hits': 0,
            'questions': 0,
            'progress': 0,
        }
    )


def add_new_user(user_id, first_name, last_name, username):
    last_name = last_name if last_name is not None else ''
    username = username if username is not None else ''
    return db.users.insert_one(
        {
            'user_id': user_id,
            'first_name': first_name,
            'last_name': last_name,
            'username': username,
            'sudo': 'false',
            'msg_private': 'true',
            'message_id': '',
            'hits': 0,
            'questions': 0,
            'progress': 0,
        }
    )


def search_user(user_id):
    return db.users.find_one({'user_id': user_id})


def get_all_users(query=None):
    if query:
        return db.users.find(query)
    else:
        return db.users.find({})


def set_user_message_id(user_id, message_id):
    return db.users.update_one(
        {'user_id': user_id}, {'$set': {'message_id': message_id}}
    )


def unset_user_message_id(user_id):
    return db.users.update_one(
        {'user_id': user_id}, {'$set': {'message_id': ''}}
    )


def remove_user_db(user_id):
    db.users.delete_one({'user_id': user_id})


def users_with_sudo():
    return db.users.find({'sudo': 'true'})


def set_user_sudo(user_id):
    return db.users.update_one(
        {'user_id': user_id}, {'$set': {'sudo': 'true'}}
    )


def un_set_user_sudo(user_id):
    return db.users.update_one(
        {'user_id': user_id}, {'$set': {'sudo': 'false'}}
    )


def set_hit_user(user_id):
    user = db.users.find_one({'user_id': user_id})
    if user:
        if 'hits' in user:
            db.users.update_one({'user_id': user_id}, {'$inc': {'hits': 1}})
        else:
            db.users.insert_one(
                {'user_id': user_id, 'hits': 1, 'questions': 1}
            )


def set_questions_user(user_id):
    user = db.users.find_one({'user_id': user_id})
    if user:
        if 'hits' in user:
            db.users.update_one({'user_id': user_id}, {'$inc': {'hits': 1}})
        else:
            db.users.insert_one(
                {'user_id': user_id, 'hits': 1, 'questions': 1}
            )


def update_msg_private(user_id, new_status):
    return db.users.update_one(
        {'user_id': user_id},
        {'$set': {'msg_private': new_status}},
    )


# Operations related to chats


def add_chat_db(chat_id, chat_name):
    return db.chats.insert_one(
        {
            'chat_id': chat_id,
            'chat_name': chat_name,
            'blocked': 'false',
            'forwarding': 'true',
            'thread_id': '',
            'question': 'false',
        }
    )


def search_group(chat_id):
    return db.chats.find_one({'chat_id': chat_id})


def get_all_chats(query=None):
    if query:
        return db.chats.find(query)
    else:
        return db.chats.find({})


def remove_chat_db(chat_id):
    db.chats.delete_one({'chat_id': chat_id})


def update_forwarding_status(chat_id, new_status):
    return db.chats.update_one(
        {'chat_id': chat_id},
        {'$set': {'forwarding': new_status}},
    )


def update_thread_id(chat_id, new_thread_id):
    db.chats.update_one(
        {'chat_id': chat_id},
        {'$set': {'thread_id': new_thread_id}},
    )


# Operations related to polls


def add_poll_db(chat_id, poll_id, correct_option_id, date):
    return db.poll.insert_one(
        {
            'chat_id': chat_id,
            'poll_id': poll_id,
            'correct_option_id': correct_option_id,
            'date': date,
        }
    )


def remove_all_poll_db():
    db.poll.delete_many({})


def search_poll(poll_id):
    return db.poll.find_one({'poll_id': poll_id})


# Operations related to sending presidents


def add_presidents_db(id, date):
    return db.presidents.insert_one(
        {
            'id': id,
            'date': date,
        }
    )


def rem_presidents_db(date):
    return db.presidents.delete_one(
        {
            'date': date,
        }
    )


def search_id_presidente(id):
    return db.presidents.find_one({'id': id})


def search_date_presidente(date):
    return db.presidents.find_one({'date': date})


# Operations related to user counter


def count_user_channel(count, date):
    return db.counter.insert_one({'count': count, 'date': date})

def update_last_entry(count, date):
    db.counter.update_one({}, {'$set': {'count': count, 'date': date}})

def get_last_entry():
    return db.counter.find_one({}, sort=[('date', -1)])
