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
bot = telebot.TeleBot("Token")

@bot.message_handler(commands=['start'])
def start(message):
    global g
    g=0
    mes= f"<b>Привет, <u>{message.from_user.first_name}</u></b>! 🙃\nНапиши мне /help"
    bot.send_message(message.chat.id, mes, parse_mode='html')

@bot.message_handler(commands=['help'])
def help1(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    timetable = types.KeyboardButton("Расписание")
    report = types.KeyboardButton("Обратная связь")
    qa = types.KeyboardButton("Q&A")
    global g
    g=0
    markup.add(timetable, report, qa)
    mes= f"<u>/ttable</u> - Твое расписание \n<u>/report</u> - Обратная связь \n<u>/questions</u> - Ответы на часто задаваемые вопросы"
    bot.send_message(message.chat.id, mes, parse_mode='html', reply_markup=markup)





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
                hf+="\n"+"<u>"+str(sheet[i][0].value)+"</u>"+" ▶️ "+str(sheet[i][1].value)
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
                hf+="\n"+"<u>"+str(sheet[i][0].value)+"</u>"+" ▶️ "+str(sheet[i][2].value)
                
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        back = types.KeyboardButton("Меню")
        
        g=0
        markup.add(back)
        bot.send_message(message.chat.id, f"<b>{hf}</b>", parse_mode='html', reply_markup=markup)
    elif message.text == "Среда":
        
        hf="Среда:"
        for i in range(2, 18):
             if str(sheet[i][3].value) != "None":
                time = str(sheet[i][0].value)
                if str(sheet[i+1][3].value) == "None" and i!=17:
                    time = time[:10]+str(sheet[i+1][0].value)[10:]
                hf+="\n"+"<u>"+time+"</u>"+" ▶️ "+str(sheet[i][3].value)
                
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        back = types.KeyboardButton("Меню")
        
        g=0
        markup.add(back)
        bot.send_message(message.chat.id, f"<b>{hf}</b>", parse_mode='html', reply_markup=markup)

    elif message.text == "Четверг":
        
        hf="Четверг:"
        for i in range(2, 18):
             if str(sheet[i][4].value) != "None":
                time = str(sheet[i][0].value)
                if str(sheet[i+1][4].value) == "None" and i!=17:
                    time = time[:10]+str(sheet[i+1][0].value)[10:]
                hf+="\n"+"<u>"+time+"</u>"+" ▶️ "+str(sheet[i][4].value)
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        back = types.KeyboardButton("Меню")
        
        g=0
        markup.add(back)
        bot.send_message(message.chat.id, f"<b>{hf}</b>", parse_mode='html', reply_markup=markup)

    elif message.text == "Пятница":
        
        hf="Пятница:"
        for i in range(2, 18):
             if str(sheet[i][5].value) != "None":
                time = str(sheet[i][0].value)
                if str(sheet[i+1][5].value) == "None" and i!=17:
                    time = time[:10]+str(sheet[i+1][0].value)[10:]
                hf+="\n"+"<u>"+time+"</u>"+" ▶️ "+str(sheet[i][5].value)
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
                time = str(sheet[i][0].value)
                if str(sheet[i+1][6].value) == "None" and i!=17:
                    time = time[:10]+str(sheet[i+1][0].value)[10:]
                hf+="\n"+"<u>"+time+"</u>"+" ▶️ "+str(sheet[i][6].value)
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        back = types.KeyboardButton("Меню")
        
        g=0
        markup.add(back)
        bot.send_message(message.chat.id, f"<b>{hf}</b>", parse_mode='html', reply_markup=markup)
    
    elif message.text == "Обратная связь" or message.text == "/report":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        back = types.KeyboardButton("Меню")
        
        g=0
        markup.add(back)
        bot.send_message(message.chat.id, f"<b>Этого еще нет...</b>", parse_mode='html', reply_markup=markup)
    elif message.text == "Q&A" or message.text == "/questions":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        back = types.KeyboardButton("Меню")
        
        g=0
        markup.add(back)
        bot.send_message(message.chat.id, f"<b>Этого еще нет...</b>", parse_mode='html', reply_markup=markup)
    
    
    #elif message.text in otr and g==1:
     #   global t

      #  bot.send_message(message.chat.id, "Твой отряд есть!", parse_mode='html')

        






    else:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        help = types.KeyboardButton("Помогите 🥺")

        markup.add(help)
        bot.send_message(message.chat.id, "<b>Я тебя не понимаю</b> 🥲\nЖми <u>/help</u>", parse_mode='html', reply_markup=markup) 
    
    



bot.polling(none_stop=True)
