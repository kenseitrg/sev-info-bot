from site_parser import get_messages_main
from telebot import TeleBot, types
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db.models import User, MsgHash
import os

TOKEN = os.environ.get("TG_TOKEN")
local_path = "postgresql://postgres:pgpass@localhost:5432/test"
db_url = os.environ.get("DATABASE_URL") or local_path
bot = TeleBot(TOKEN)
engine = create_engine(db_url)
Session = sessionmaker(bind=engine)


def register_user(user_id):
    db_session = Session()
    existing_user = db_session.query(User).filter(User.tg_id == user_id).first()
    if existing_user is None:
        db_session.add(User(user_id))
    db_session.commit()

def generate_initial_markup():
    markup = types.InlineKeyboardMarkup()
    water_button = types.InlineKeyboardButton("Вода", callback_data="water")
    electro_button = types.InlineKeyboardButton("Электричество", callback_data="electro")
    markup.row(water_button, electro_button)
    return markup

def generate_electro_markup():
    markup = types.InlineKeyboardMarkup()
    plan_button = types.InlineKeyboardButton("Плановые работы", callback_data="electro_plan")
    emg_button = types.InlineKeyboardButton("Аварии", callback_data="electro_emg")
    markup.row(plan_button, emg_button)
    return markup

@bot.message_handler(commands=['start'])
def handle_start_help(message):
    bot.send_message(message.from_user.id, "Инормация о работе служб в Севастополе")
    bot.send_message(message.from_user.id, "Вода или Электроэнергия?", reply_markup=generate_initial_markup())
    register_user(message.from_user.id)

def render_reply(reply):
    output = reply["date"] + "-" + reply["title"] + "\n" + reply["text"] + "\n"
    link = '<a href="' + reply["link"] + '">Подробнее...</a>'
    return "".join([output, link])

@bot.callback_query_handler(func=lambda call: call.data != "electro")
def handle_general_message(call):
    replies = get_messages_main(call.data)
    for reply in replies:
        bot.send_message(call.from_user.id, render_reply(reply), parse_mode="HTML", disable_web_page_preview=True)
    bot.send_message(call.from_user.id, "Больше информации?", reply_markup=generate_initial_markup())

@bot.callback_query_handler(func=lambda call: call.data == "electro")
def handle_electro_message(call):
    bot.send_message(call.from_user.id, "Тип работ?", reply_markup=generate_electro_markup())

bot.polling(none_stop=True)
