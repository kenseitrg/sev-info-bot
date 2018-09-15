from site_parser import get_messages_main
from hashlib import md5
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db.models import User, MsgHash
import os

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

def process_worker(msg_type, db_session):
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
    local_path = "postgresql://postgres:pgpass@localhost:5432/test"
    db_url = os.environ.get("DATABASE_URL") or local_path
    engine = create_engine(db_url)
    Session = sessionmaker(bind=engine)
    db_session = Session()
    process_worker("water", db_session)
    process_worker("electro_plan", db_session)
    process_worker("electro_emg", db_session)
    db_session.close()

