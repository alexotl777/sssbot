from re import T
from sys import flags
from zipapp import ZipAppError
import telebot
#from telegram.ext import Updater
#from telegram.ext import CommandHandler, MessageHandler, Filters
import requests
from telebot import types
import openpyxl

#табл с расписанием
book = openpyxl.open("shsn_raspisanie_karkas.xlsx", read_only=True)
sheet = book.active

#otr=[] #отряды
#for i in range(2, 13, 6):
#    otr.append(str(sheet[i][0].value))
#print(otr)
bot = telebot.TeleBot("5795768012:AAF7vtBoABHnAxkoNp_ExfnDeJvwc_EobQ8")
owner = 401082878



@bot.message_handler(commands=['start'])
def start(message):
    global g
    g=0
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    back = types.KeyboardButton("Меню")

        
    markup.add(back)
    mes= f"<b>Привет, <u>{message.from_user.first_name}</u></b>! 🙃\nНапиши мне /help или нажми кнопку Меню"

    bot.send_message(message.chat.id, mes, parse_mode='html', reply_markup=markup)

@bot.message_handler(commands=['help'])
def help1(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    timetable = types.KeyboardButton("Расписание")
    report = types.KeyboardButton("Отзыв")
    qa = types.KeyboardButton("Q&A")
    global g
    g=0
    markup.add(timetable, report, qa)
    mes= f"<u>/ttable</u> - Твое расписание 🕑\n<u>/report</u> - Оставить отзыв ✏️\n<u>/questions</u> - Ответы на часто задаваемые вопросы 📚"
    bot.send_message(message.chat.id, mes, parse_mode='html', reply_markup=markup)


@bot.message_handler(commands=['send'])
def process_start(message):

    if int(message.chat.id) == owner:

        try:

            bot.send_message(message.chat.id, 'Для отправки сообщения сделай реплей')

            bot.forward_message(owner, message.chat.id, message.message_id)

            bot.register_next_step_handler(message, process_mind)

        except:

            bot.send_message(message.chat.id, "Что-то пошло не так! Ошибка возникла в блоке кода:\n<code>@bot.message_handler(commands=['send_message'])</code>", parse_mode='HTML')

    else:

        bot.send_message(message.chat.id, 'Вы не являетесь администратором для выполнения этой команды!')

def process_mind(message):

    if int(message.chat.id) == owner:

        try:

            text = 'Сообщение было отправлено пользователю ' + str(message.reply_to_message.forward_from.first_name)

            bot.forward_message(message.reply_to_message.forward_from.id, owner, message.message_id)

            bot.send_message(owner, text)

        except:

            bot.send_message(message.chat.id, 'Что-то пошло не так! Бот продолжил свою работу.' + ' Ошибка произошла в блоке кода:\n\n <code>def process_mind(message)</code>', parse_mode='HTML')

    else:
        bot.send_message(message.chat.id, 'Вы не являетесь администратором для выполнения этой команды!')  


@bot.message_handler()
def body(message):
    if message.text == "/ttable" or message.text == "Расписание":
        zap="Выбери день!"
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        pn = types.KeyboardButton("Понедельник")
        vt = types.KeyboardButton("Вторник")
        sr = types.KeyboardButton("Среда")
        cht = types.KeyboardButton("Четверг")
        pt = types.KeyboardButton("Пятница")
        sb = types.KeyboardButton("Суббота")
        markup.add(pn, vt, sr, cht, pt, sb)

        bot.send_message(message.chat.id, zap, parse_mode='html', reply_markup=markup)
        global g
        g=1
    elif message.text == "Помогите 🥺" or message.text == "Меню":
        
        g=0
        help1(message)
    elif message.text == "Понедельник":
        h=[]
        hf="Понедельник:"
        for i in range(2, 18):
             if str(sheet[i][1].value) != "None":
                if str(sheet[i][1].value)[:6] == "Лекция":
                    w1= "🔵"
                elif  str(sheet[i][1].value)[:7] == "Семинар":
                    w1= "🟡"
                else:
                    w1 = "🟢"
                hf+="\n"+"<u>"+str(sheet[i][0].value)+"</u>"+f" {w1} \n"+str(sheet[i][1].value)
                h.append([str(sheet[i][0].value),str(sheet[i][1].value)])
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        back = types.KeyboardButton("Меню")

        g=0
        markup.add(back)
        bot.send_message(message.chat.id, f"<b>{hf}</b>", parse_mode='html', reply_markup=markup)
    elif message.text == "Вторник":

        hf="Вторник:"
        for i in range(2, 18):
             if str(sheet[i][2].value) != "None":
                if str(sheet[i][2].value)[:6] == "Лекция":
                    w1= "🔵"
                elif  str(sheet[i][2].value)[:7] == "Семинар":
                    w1= "🟡"
                else:
                    w1 = "🟢"
                hf+="\n"+"<u>"+str(sheet[i][0].value)+"</u>"+f" {w1} \n"+str(sheet[i][2].value)

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        back = types.KeyboardButton("Меню")

        g=0
        markup.add(back)
        bot.send_message(message.chat.id, f"<b>{hf}</b>", parse_mode='html', reply_markup=markup)
    elif message.text == "Среда":

        hf="Среда:"
        for i in range(2, 18):
             if str(sheet[i][3].value) != "None":
                if str(sheet[i][3].value)[:6] == "Лекция":
                    w1= "🔵"
                elif  str(sheet[i][3].value)[:7] == "Семинар":
                    w1= "🟡"
                else:
                    w1 = "🟢"
                time = str(sheet[i][0].value)
                if str(sheet[i+1][3].value) == "None" and i!=17:
                    time = time[:10]+str(sheet[i+1][0].value)[10:]
                hf+="\n"+"<u>"+time+"</u>"+f" {w1} \n"+str(sheet[i][3].value)

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        back = types.KeyboardButton("Меню")

        g=0
        markup.add(back)
        bot.send_message(message.chat.id, f"<b>{hf}</b>", parse_mode='html', reply_markup=markup)

    elif message.text == "Четверг":

        hf="Четверг:"
        for i in range(2, 18):
             if str(sheet[i][4].value) != "None":
                if str(sheet[i][4].value)[:6] == "Лекция":
                    w1= "🔵"
                elif  str(sheet[i][4].value)[:7] == "Семинар":
                    w1= "🟡"
                else:
                    w1 = "🟢"
                time = str(sheet[i][0].value)
                if str(sheet[i+1][4].value) == "None" and i!=17:
                    time = time[:10]+str(sheet[i+1][0].value)[10:]
                hf+="\n"+"<u>"+time+"</u>"+f" {w1} \n"+str(sheet[i][4].value)
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        back = types.KeyboardButton("Меню")

        g=0
        markup.add(back)
        bot.send_message(message.chat.id, f"<b>{hf}</b>", parse_mode='html', reply_markup=markup)

    elif message.text == "Пятница":

        hf="Пятница:"
        for i in range(2, 18):
             if str(sheet[i][5].value) != "None":
                if str(sheet[i][5].value)[:6] == "Лекция":
                    w1= "🔵"
                elif  str(sheet[i][5].value)[:7] == "Семинар":
                    w1= "🟡"
                else:
                    w1 = "🟢"
                time = str(sheet[i][0].value)
                if str(sheet[i+1][5].value) == "None" and i!=17:
                    time = time[:10]+str(sheet[i+1][0].value)[10:]
                hf+="\n"+"<u>"+time+"</u>"+f" {w1} \n"+str(sheet[i][5].value)
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        back = types.KeyboardButton("Меню")

        g=0
        markup.add(back)
        bot.send_message(message.chat.id, f"<b>{hf}</b>", parse_mode='html', reply_markup=markup)

    elif message.text == "Суббота":
        h=[]
        hf="Суббота:"
        for i in range(2, 18):
             if str(sheet[i][6].value) != "None":
                if str(sheet[i][6].value)[:6] == "Лекция":
                    w1= "🔵"
                elif  str(sheet[i][6].value)[:7] == "Семинар":
                    w1= "🟡"
                else:
                    w1 = "🟢"
                time = str(sheet[i][0].value)
                if str(sheet[i+1][6].value) == "None" and i!=17:
                    time = time[:10]+str(sheet[i+1][0].value)[10:]
                hf+="\n"+"<u>"+time+"</u>"+f" {w1} \n"+str(sheet[i][6].value)
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        back = types.KeyboardButton("Меню")

        g=0
        markup.add(back)
        bot.send_message(message.chat.id, f"<b>{hf}</b>", parse_mode='html', reply_markup=markup)
    
    #elif message.text == "Обратная связь" or message.text == "/report":
    #    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
     #   back = types.KeyboardButton("Меню")
      #  
       # g=0
        #markup.add(back)
        #bot.send_message(message.chat.id, f"<b>Этого еще нет...</b>", parse_mode='html', reply_markup=markup)
    elif message.text == "Q&A" or message.text == "/questions":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        back = types.KeyboardButton("Меню")
        
        g=0
        markup.add(back)
        bot.send_message(message.chat.id, f"<b>Этого еще нет...</b>", parse_mode='html', reply_markup=markup)
    
    
    #elif message.text in otr and g==1:
     #   global t

      #  bot.send_message(message.chat.id, "Твой отряд есть!", parse_mode='html')


    #elif message.text == "Отзыв" or message.text == "/report":
     #   bot.send_message(message.chat.id, f"<b>Напиши вопрос в виде: В: 'Твой вопрос'</b>\nТак нужно для нашего удобства)", parse_mode='html')
    #    #bot.send_message(message.chat.id, '<b>Напиши вопрос в виде: "В: <Твой вопрос>"</b>\nТак нужно для нашего удобства)')
    #elif message.text[:2] == "В:":
     #   if int(message.chat.id) == owner:

#            try:

#                bot.send_message(message.chat.id, 'Сообщение от администратора было получено')

#            except:
#                bot.send_message(owner, 'Что-то пошло не так! Бот продолжил свою работу.' + ' Ошибка произошла в блоке кода:\n\n <code>@bot.message_handler(content_types=["text"])</code>', parse_mode='HTML')



 #       else:

  #          pass

   #     try:

    #        bot.forward_message(owner, message.chat.id, message.message_id)
            
     #       bot.send_message(message.chat.id, str(message.from_user.first_name) + ',' +' я получил сообщение и очень скоро на него отвечу :)')

      #  except:

       #     bot.send_message(owner, 'Что-то пошло не так! Бот продолжил свою работу.')
       # markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        #back = types.KeyboardButton("Меню")
        
        #g=0
        #markup.add(back)
       # bot.send_message(message.chat.id, f"<b>Этого еще нет...</b>", parse_mode='html', reply_markup=markup)


    elif message.text == "Отзыв" or message.text == "/report":
        try:
            bot.send_message(message.chat.id, "Пиши свой отзыв!")
            bot.register_next_step_handler(message, txt)
        except:
            bot.send_message(message.chat.id, "Ошибка!")



    else:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        help = types.KeyboardButton("Помогите 🥺")

        markup.add(help)
        bot.send_message(message.chat.id, "<b>Я тебя не понимаю</b> 🥲\nЖми <u>/help</u>", parse_mode='html', reply_markup=markup) 
        sad = open('sad.webp', 'rb')
        bot.send_sticker(message.chat.id, sad)
        bot.send_sticker(message.chat.id, "FILEID")
'''def rep(message):
    if message.text == "Отзыв" or message.text == "/report":
        try:
            bot.send_message(message.chat.id, "Пиши свой отзыв!")
            bot.register_next_step_handler(message, process_mind)
        except:
            bot.send_message(message.chat.id, "Ошибка!")'''
def txt(message):
    #bot.send_message(message.chat.id, "Отправлено!")
    bot.forward_message(owner, message.chat.id, message.message_id)

    #bot.send_message(owner, f"Отзыв: \n\n{message.text}", parse_mode='html')
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    back = types.KeyboardButton("Меню")
    
    g=0
    markup.add(back)
    bot.send_message(message.chat.id, f"<b>Отправлено! Спасибо за отзыв</b> 🥰", parse_mode='html', reply_markup=markup)
    love = open('love.webp', 'rb')
    bot.send_sticker(message.chat.id, love)
    bot.send_sticker(message.chat.id, "FILEID")

bot.polling(none_stop=True)