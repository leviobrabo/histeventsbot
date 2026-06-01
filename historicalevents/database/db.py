from datetime import datetime, timedelta

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


def _utcnow():
    return datetime.utcnow()


def _day_string(date_value=None):
    current = date_value or _utcnow()
    return current.strftime('%Y-%m-%d')


def _base_user_document(user_id, first_name, last_name, username, start_source='direct'):
    now = _utcnow()
    current_day = _day_string(now)
    return {
        'user_id': user_id,
        'first_name': first_name or '',
        'last_name': last_name or '',
        'username': username or '',
        'sudo': 'false',
        'msg_private': 'true',
        'message_id': '',
        'hits': 0,
        'questions': 0,
        'progress': 0,
        'created_at': now,
        'first_seen_at': now,
        'last_active_at': now,
        'last_active_day': current_day,
        'active_days': [current_day],
        'start_source': start_source or 'direct',
        'first_action_at': None,
        'actions_total': 0,
        'actions': {},
    }


def add_user_db(message):
    first_name = message.from_user.first_name
    last_name = str(message.from_user.last_name).replace('None', '')
    username = str(message.from_user.username).replace('None', '')
    start_source = extract_start_source(getattr(message, 'text', ''))
    return db.users.insert_one(
        _base_user_document(
            message.from_user.id,
            first_name,
            last_name,
            username,
            start_source=start_source,
        )
    )


def add_new_user(user_id, first_name, last_name, username, start_source='direct'):
    last_name = last_name if last_name is not None else ''
    username = username if username is not None else ''
    return db.users.insert_one(
        _base_user_document(
            user_id,
            first_name,
            last_name,
            username,
            start_source=start_source,
        )
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


def extract_start_source(message_text):
    if not message_text:
        return 'direct'

    parts = message_text.strip().split(maxsplit=1)
    if len(parts) < 2:
        return 'direct'

    payload = parts[1].strip()
    if not payload:
        return 'direct'

    return payload[:80]


def record_user_activity(
    user_id,
    action_name,
    *,
    first_name=None,
    last_name=None,
    username=None,
    start_source=None,
    count_as_first_action=True,
):
    now = _utcnow()
    current_day = _day_string(now)
    user = search_user(user_id)

    if not user:
        add_new_user(
            user_id,
            first_name or '',
            last_name or '',
            username or '',
            start_source=start_source or 'direct',
        )
        user = search_user(user_id)

    set_payload = {
        'last_active_at': now,
        'last_active_day': current_day,
    }

    if first_name is not None:
        set_payload['first_name'] = first_name
    if last_name is not None:
        set_payload['last_name'] = last_name or ''
    if username is not None:
        set_payload['username'] = username or ''
    if start_source and not user.get('start_source'):
        set_payload['start_source'] = start_source
    if not user.get('created_at'):
        set_payload['created_at'] = now
    if not user.get('first_seen_at'):
        set_payload['first_seen_at'] = now
    if count_as_first_action and not user.get('first_action_at'):
        set_payload['first_action_at'] = now

    return db.users.update_one(
        {'user_id': user_id},
        {
            '$set': set_payload,
            '$addToSet': {'active_days': current_day},
            '$inc': {
                'actions_total': 1,
                f'actions.{action_name}': 1,
            },
        },
    )


def get_active_user_count(days, today=None):
    today = today or _utcnow()
    active_days = [
        _day_string(today - timedelta(days=offset)) for offset in range(days)
    ]
    return db.users.count_documents({'active_days': {'$in': active_days}})


def get_retention_snapshot(days, today=None):
    today = today or _utcnow()
    cohort_start = (today - timedelta(days=days)).replace(
        hour=0, minute=0, second=0, microsecond=0
    )
    cohort_end = cohort_start + timedelta(days=1)
    return_day = _day_string(cohort_start + timedelta(days=days))

    cohort_query = {
        'first_seen_at': {'$gte': cohort_start, '$lt': cohort_end},
    }
    cohort_size = db.users.count_documents(cohort_query)
    if cohort_size == 0:
        return {'cohort_size': 0, 'retained_users': 0, 'retention_rate': None}

    retained_users = db.users.count_documents(
        {
            **cohort_query,
            'active_days': return_day,
        }
    )
    retention_rate = (retained_users / cohort_size) * 100
    return {
        'cohort_size': cohort_size,
        'retained_users': retained_users,
        'retention_rate': retention_rate,
    }


def get_top_start_sources(limit=5):
    pipeline = [
        {'$match': {'start_source': {'$exists': True, '$nin': ['', None]}}},
        {'$group': {'_id': '$start_source', 'users': {'$sum': 1}}},
        {'$sort': {'users': -1, '_id': 1}},
        {'$limit': limit},
    ]
    return list(db.users.aggregate(pipeline))


def get_avg_time_to_first_action():
    pipeline = [
        {
            '$match': {
                'first_seen_at': {'$type': 'date'},
                'first_action_at': {'$type': 'date'},
            }
        },
        {
            '$project': {
                'seconds': {
                    '$divide': [
                        {'$subtract': ['$first_action_at', '$first_seen_at']},
                        1000,
                    ]
                }
            }
        },
        {'$group': {'_id': None, 'avg_seconds': {'$avg': '$seconds'}, 'users': {'$sum': 1}}},
    ]
    result = list(db.users.aggregate(pipeline))
    if not result:
        return None
    return result[0]


def get_top_users_by_activity(limit=5):
    return list(
        db.users.find(
            {'actions_total': {'$gt': 0}},
            {
                'user_id': 1,
                'first_name': 1,
                'username': 1,
                'actions_total': 1,
            },
        )
        .sort([('actions_total', -1), ('last_active_at', -1)])
        .limit(limit)
    )


def get_funnel_counts():
    return {
        'started': db.users.count_documents({}),
        'help': db.users.count_documents({'actions.help': {'$gt': 0}}),
        'notifications_on': db.users.count_documents(
            {'actions.sendon': {'$gt': 0}}
        ),
        'poll_answer': db.users.count_documents(
            {'actions.poll_answer': {'$gt': 0}}
        ),
    }


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
