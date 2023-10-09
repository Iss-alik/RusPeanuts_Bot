import telebot
from telebot import types
import constans
import structural.adapter
import structural.what_num
from datetime import datetime
import random

bot = telebot.TeleBot(constans.TOKEN)
delta = 1
global cur_num
cur_num = structural.what_num.num_from_url(url=constans.BASE)
lst_num = cur_num

@bot.message_handler(commands=['help'])
def help_message(message):
    bot.send_message(message.chat.id, text= "На данный момент бот способен показать: 1) последний стрип на акомиксе через '/start' 2) предыдущий стрип '<' 3)слуйчайный стрип '()'  4) следующий стрип '>'")

@bot.message_handler(commands=['start'])
def get_text_message(message):

    km = types.InlineKeyboardMarkup(row_width=3)
    previous = types.InlineKeyboardButton(text="<", callback_data="previous")
    rnd = types.InlineKeyboardButton(text="()", callback_data="rnd")
    next= types.InlineKeyboardButton(text=">", callback_data="next")
    km.add(previous, rnd, next)

    structural.adapter.url_to_square(url=constans.BASE)


    img = 'request.png'
    file = open(img, 'rb')
    bot.send_photo(message.chat.id, file, "Самое горячее, самое актруальное", reply_markup= km) 

@bot.callback_query_handler(func = lambda callback: callback.data)
def update(callback):
    global cur_num
    km = types.InlineKeyboardMarkup(row_width=3)
    previous = types.InlineKeyboardButton(text="<", callback_data="previous")
    rnd = types.InlineKeyboardButton(text="()", callback_data="rnd")
    next= types.InlineKeyboardButton(text=">", callback_data="next")
    km.add(previous, rnd, next)

    if  callback.data == 'previous':
        cur_num -= delta

    elif callback.data == 'next':
        cur_num += delta
    
    elif callback.data == 'rnd':
        cur_num  = random.randint(1,lst_num+1)
    
    structural.adapter.url_to_square(url=constans.BASE + '/' +str(cur_num))

    img = 'request.png'
    file = open(img, 'rb')

    bot.send_photo(callback.message.chat.id, file, reply_markup=km)

@bot.message_handler(commands='date')
def strip_of_date(message):
    query = message.text.split(' ')
    q_date = datetime.strptime(query[1], '%Y-%m-%d')
    q_num = structural.what_num.num_of_date(cur_date= q_date)

    km = types.InlineKeyboardMarkup(row_width=3)
    previous = types.InlineKeyboardButton(text="<", callback_data="previous")
    rnd = types.InlineKeyboardButton(text="()", callback_data="rnd")
    next= types.InlineKeyboardButton(text=">", callback_data="next")
    km.add(previous, rnd, next)

    structural.adapter.url_to_square(url=constans.BASE + '/' +str(q_num))

    img = 'request.png'
    file = open(img, 'rb')

    bot.send_photo(message.chat.id, file, reply_markup=km)

bot.polling()
