from site_parser import get_messages_main
from hashlib import md5
from bot import Session
from db.models import User, MsgHash

def hash_messages(msg_dict):
    messages = "".join(str(msg_dict))
    return md5(messages.encode()).hexdigest()

def update_db(session, msg_type, msg_hash):
    message = get_from_db(session, msg_type)
    if message is None:
        message = MsgHash(msg_type, msg_hash)
        session.add(message)
    else:
        message.msg_hash = msg_hash
    session.commit()

def get_from_db(session, msg_type):
    return session.query(MsgHash).filter(MsgHash.msg_type == msg_type).first()

def process_worker(msg_type):
    db_session = Session()
    messages = get_messages_main(msg_type)
    messages_hash = hash_messages(messages)
    old_message = get_from_db(db_session, msg_type)
    if old_message is None:
        update_db(db_session, msg_type, messages_hash)
        return messages
    elif old_message.msg_hash != messages_hash:
        update_db(db_session, msg_type, messages_hash)
        return messages
    else:
        return 0

if __name__ == "__main__":
    process_worker("water")
    process_worker("electro_plan")
    process_worker("electro_emg")

