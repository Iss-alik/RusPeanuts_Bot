from aiogram import Bot, Dispatcher
from aiogram.types import *
from aiogram.filters import Command

import structural.adapter
import constans
import structural.what_num
from datetime import datetime
import random

# Вставляем токен из файла с константами
BOT_TOKEN = constans.TOKEN

bot = Bot(BOT_TOKEN)
dp = Dispatcher()

delta =1 
global cur_num 
cur_num = structural.what_num.num_from_url(url=constans.BASE) # сразу присваиваем дату последнего стрипа с acomics, потому что /start выдает последний стрип
lst_num = cur_num

# генерации клавиатур с инлайн-кнопками
menu= [
[
    InlineKeyboardButton(text='⏪', callback_data= 'first'),
    InlineKeyboardButton(text='◀️', callback_data= 'previous'),
    InlineKeyboardButton(text='🔄', callback_data= 'random'),
    InlineKeyboardButton(text='▶️', callback_data= 'next'),
    InlineKeyboardButton(text='⏩', callback_data= 'last')
]
]
menu = InlineKeyboardMarkup(inline_keyboard=menu)


# Реагирует на /start и выдает последний стрип на acomics
@dp.message(Command("start"))
async def start_handler(msg:Message):

    structural.adapter.url_to_square(url=constans.BASE)

    request = FSInputFile("request.png") # Открываем файл 
    issueName = structural.what_num.issueName(url=constans.BASE + '/' +str(cur_num)) # Достаем дату выпуска с acomics
    await msg.answer_photo(request, reply_markup=menu, caption = issueName)


# Этот хэндлер будет срабатывать на нажатие инлайн-кнопки
@dp.callback_query()
async def process_button_press(query: CallbackQuery, bot: Bot):
    global cur_num

    if query.data == 'first':
        cur_num = 1

    elif  query.data == 'previous' and cur_num !=1:
        cur_num -= delta

    elif query.data == 'random':
        cur_num  = random.randint(1,lst_num+1)

    elif query.data == 'next' and cur_num != lst_num:
        cur_num += delta
        
    elif query.data == 'last':
        cur_num = lst_num
    
    structural.adapter.url_to_square(url=constans.BASE + '/' +str(cur_num)) # Достаем стрип с номером = cur_num
    request = FSInputFile("request.png")
    issueName = structural.what_num.issueName(url=constans.BASE + '/' +str(cur_num)) # Достаем дату выпуска

    await query.message.answer_photo(request, reply_markup=menu, caption= issueName) # Отправляем стрип
    await query.message.delete() # Удаляем предыдущие сообщение 

@dp.message(Command("help"))
async def help(msg:Message):
    await msg.answer("/start - запуск бота, /date - Стрип по определеной дате, /bookmark - сделать закладку")

# Этот хэндлер будет срабатывать на все остальные сообщения
@dp.message()
async def send_echo(message: Message):
    await message.answer(text='Не понимаю')


if __name__ == '__main__':
    dp.run_polling(bot)
