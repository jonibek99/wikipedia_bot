from telegram.ext import (
    Updater,
    CallbackContext,
    CommandHandler,
    MessageHandler,
    Filters,
    CallbackQueryHandler,
)
from telegram import (
    Update,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)
import wikipedia
from dotenv import load_dotenv
import os
from tinydb import TinyDB,Query
import json
load_dotenv()
token = os.getenv("token")

updater = Updater(token=token)
dispatcher = updater.dispatcher
def chat_id_handler(update:Update,contex:CallbackContext):
    bot=contex.bot
    chat_id=update.message.chat.id
    user_name=update.message.from_user.username
    f_name=update.message.from_user.first_name
    l_name=update.message.from_user.last_name
    db=TinyDB('user_info.json')
    user=Query()
    if not db.search(user.chat_id==chat_id):
        db.insert({'chat_id':chat_id,
                   'user_name':user_name,
                   'first_name':f_name,
                   'last_name':l_name
                   })
    
    message = f"Salom @{user_name or f_name or l_name}"
    bot.send_message(chat_id=chat_id,text=message)#'bot ishlashi uchu. startni nbosing',#reply_markup=button)
    wikipedia.set_lang('uz')
def text_handler(update: Update, context: CallbackContext):
    text=update.message.text
    user=update.message.from_user
    chat_id=update.message.chat.id
    a=f'Your message {text} is received'

    try:
        res = wikipedia.summary(text, sentences=3)
        title=wikipedia.page(text).title
    except wikipedia.exceptions.PageError:
        res = "Kechirasiz, bu mavzu bo‘yicha maqola topilmadi."
    except wikipedia.exceptions.DisambiguationError as e:
        res = f"Iltimos aniqroq yozing. Mumkin bo‘lgan mavzular:\n{', '.join(e.options[:5])}"
    except Exception as e:
        res = f"Xatolik yuz berdi: {e}"

    context.bot.send_message(chat_id=chat_id, text=res)
    db=TinyDB('data.json')
    db.insert({
        'chat_id':chat_id,
        'user_name':user.username,
        'first_name':user.first_name,
        'last_name':user.last_name,
        'query':text,
        'title':title,})
dispatcher.add_handler(CommandHandler('start',chat_id_handler))
dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, text_handler))

updater.start_polling()
updater.idle()

 




