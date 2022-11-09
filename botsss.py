#from re import T
#from sqlite3 import Row
#from sys import flags
#from zipapp import ZipAppError
import telebot
#from telegram.ext import Updater
#from telegram.ext import CommandHandler, MessageHandler, Filters

from telebot import types
import openpyxl
import gspread
import datetime

#табл с расписанием
book = openpyxl.open("raspok.xlsx", read_only=True)
sheet = book.active


#Табл с отзывами
gc = gspread.service_account(filename='social-school-367309-cc83c4d1b3a3.json')
#Откр таблицу
sh = gc.open("Отзывы ШСН")
worksheet = sh.get_worksheet(0)



#otr=[] #отряды
#for i in range(2, 13, 6):
#    otr.append(str(sheet[i][0].value))
#print(otr)
bot = telebot.TeleBot("TOKEN")
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
    file = open('hi.webp', 'rb')
    bot.send_sticker(message.chat.id, file)

@bot.message_handler(commands=['help'])
def help1(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    timetable = types.KeyboardButton("Расписание")
    report = types.KeyboardButton("Отзыв")
    qa = types.KeyboardButton("Q&A")
    #inter= types.KeyboardButton("Полезное")
    global g
    g=0
    markup.add(timetable, report, qa)
    mes= f"<u>/ttable</u> - Твое расписание 🕑\n<u>/report</u> - Оставить отзыв ✏️\n<u>/questions</u> - Ответы на часто задаваемые вопросы 📚"
    bot.send_message(message.chat.id, mes, parse_mode='html', reply_markup=markup)
    if message.chat.id == 687388034:
        try:
            bot.send_photo("photo.png")
        except:
            g=0
        for i in range(3):
           bot.send_message(message.chat.id, "Вика злая😡")

@bot.message_handler(commands=['send'])
def process_start(message):

    if int(message.chat.id) == owner or int(message.chat.id) == 687388034:

        try:

            bot.send_message(message.chat.id, 'Для отправки сообщения сделай реплей')

            bot.forward_message(owner, message.chat.id, message.message_id)
            bot.forward_message(687388034, message.chat.id, message.message_id)

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
        for i in range(3, 14):
            if str(sheet[i][0].value) != "None":
                if str(sheet[i][0].value)[:6] == "Лекция":
                    w1= "🔵"
                elif  str(sheet[i][0].value)[:7] == "Семинар":
                    w1= "🟡"
                else:
                    w1 = "🟢"
                if str(sheet[i][3].value) == "None":
                    ved = "-"
                elif i == 5:
                    ved == "Директор ШСН Сорвин К.В., организаторы ШСН, студенты ФСН"
                else:
                    ved = str(sheet[i][3].value)
                hf+="\n"+"<u>"+str(sheet[i][1].value)+" - "+ str(sheet[i][2].value) + "</u>"+f" {w1} \n"+str(sheet[i][0].value + "\n  Ведущие: " + f"{ved}\n")
                h.append([str(sheet[i][0].value),str(sheet[i][1].value)])
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        back = types.KeyboardButton("Меню")

        g=0
        markup.add(back)
        bot.send_message(message.chat.id, f"<b>{hf}</b>", parse_mode='html', reply_markup=markup)
    elif message.text == "Вторник":

        hf="Вторник:"
        for i in range(17, 35):
            if str(sheet[i][0].value) != "None":
                if str(sheet[i][0].value)[:6] == "Лекция":
                    w1= "🔵"
                elif  str(sheet[i][0].value)[:7] == "Семинар":
                    w1= "🟡"
                else:
                    w1 = "🟢"
                if str(sheet[i][3].value) == "None":
                    ved = "-"
                elif i == 5:
                    ved == "Директор ШСН Сорвин К.В., организаторы ШСН, студенты ФСН"
                else:
                    ved = str(sheet[i][3].value)
                hf+="\n"+"<u>"+str(sheet[i][1].value)+" - "+ str(sheet[i][2].value) + "</u>"+f" {w1} \n"+str(sheet[i][0].value + "\n  Ведущие: " + f"{ved}\n")


        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        back = types.KeyboardButton("Меню")

        g=0
        markup.add(back)
        bot.send_message(message.chat.id, f"<b>{hf}</b>", parse_mode='html', reply_markup=markup)
    elif message.text == "Среда":

        hf="Среда:"
        for i in range(39, 58):
            if str(sheet[i][0].value) != "None":
                if str(sheet[i][0].value)[:6] == "Лекция":
                    w1= "🔵"
                elif  str(sheet[i][0].value)[:7] == "Семинар":
                    w1= "🟡"
                else:
                    w1 = "🟢"
                if str(sheet[i][3].value) == "None":
                    ved = "-"
                elif i == 5:
                    ved == "Директор ШСН Сорвин К.В., организаторы ШСН, студенты ФСН"
                else:
                    ved = str(sheet[i][3].value)
                hf+="\n"+"<u>"+str(sheet[i][1].value)+" - "+ str(sheet[i][2].value) + "</u>"+f" {w1} \n"+str(sheet[i][0].value + "\n  Ведущие: " + f"{ved}\n")

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        back = types.KeyboardButton("Меню")

        g=0
        markup.add(back)
        bot.send_message(message.chat.id, f"<b>{hf}</b>", parse_mode='html', reply_markup=markup)

    elif message.text == "Четверг":

        hf="Четверг:"
        for i in range(60, 79):
            if str(sheet[i][0].value) != "None":
                if str(sheet[i][0].value)[:6] == "Лекция":
                    w1= "🔵"
                elif  str(sheet[i][0].value)[:7] == "Семинар":
                    w1= "🟡"
                else:
                    w1 = "🟢"
                if str(sheet[i][3].value) == "None":
                    ved = "-"
                elif i == 5:
                    ved == "Директор ШСН Сорвин К.В., организаторы ШСН, студенты ФСН"
                else:
                    ved = str(sheet[i][3].value)
                hf+="\n"+"<u>"+str(sheet[i][1].value)+" - "+ str(sheet[i][2].value) + "</u>"+f" {w1} \n"+str(sheet[i][0].value + "\n  Ведущие: " + f"{ved}\n")
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        back = types.KeyboardButton("Меню")

        g=0
        markup.add(back)
        bot.send_message(message.chat.id, f"<b>{hf}</b>", parse_mode='html', reply_markup=markup)

    elif message.text == "Пятница":

        hf="Пятница:"
        for i in range(82, 102):
            if str(sheet[i][0].value) != "None":
                if str(sheet[i][0].value)[:6] == "Лекция":
                    w1= "🔵"
                elif  str(sheet[i][0].value)[:7] == "Семинар" or str(sheet[i][0].value)[:4] == "Подг":
                    w1= "🟡"
                else:
                    w1 = "🟢"
                if str(sheet[i][3].value) == "None":
                    ved = "-"
                elif i == 5:
                    ved == "Директор ШСН Сорвин К.В., организаторы ШСН, студенты ФСН"
                else:
                    ved = str(sheet[i][3].value)
                hf+="\n"+"<u>"+str(sheet[i][1].value)+" - "+ str(sheet[i][2].value) + "</u>"+f" {w1} \n"+str(sheet[i][0].value + "\n  Ведущие: " + f"{ved}\n")
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        back = types.KeyboardButton("Меню")

        g=0
        markup.add(back)
        bot.send_message(message.chat.id, f"<b>{hf}</b>", parse_mode='html', reply_markup=markup)

    elif message.text == "Суббота":
        h=[]
        hf="Суббота:"
        for i in range(104, 112):
            if str(sheet[i][0].value) != "None":
                if str(sheet[i][0].value)[:6] == "Лекция":
                    w1= "🔵"
                elif  str(sheet[i][0].value)[:7] == "Семинар":
                    w1= "🟡"
                else:
                    w1 = "🟢"
                if str(sheet[i][3].value) == "None":
                    ved = "-"
                elif i == 108:
                    ved == "Директор ШСН Сорвин К.В., организаторы ШСН, студенты ФСН"
                else:
                    ved = str(sheet[i][3].value)
                hf+="\n"+"<u>"+str(sheet[i][1].value)+" - "+ str(sheet[i][2].value) + "</u>"+f" {w1} \n"+str(sheet[i][0].value + "\n  Ведущие: " + f"{ved}\n")
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
   # elif message.text == "Q&A" or message.text == "/questions":
    #    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
     #   back = types.KeyboardButton("Меню")
#
 #       g=0
  #      markup.add(back)
   #     bot.send_message(message.chat.id, f"<b>Этого еще нет...</b>", parse_mode='html', reply_markup=markup)


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

    elif message.text == "Q&A" or message.text == "/questions":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        first = types.KeyboardButton("Как не пропустить ничего важного на лекции и запомнить все, что рассказал преподаватель?")
        second = types.KeyboardButton("Во сколько планируется отъезд из Москвы в Вороново, куда и ко скольки нужно приехать?")
        third = types.KeyboardButton("Во сколько и где заканчивается программа Школы в последний день 12 ноября?")
        fourth = types.KeyboardButton("Будет ли осуществляться встреча и сопровождение иногородних участников?")
        fifth = types.KeyboardButton("Если у меня есть аллергия на какие-то продукты, где я могу это указать?")
        sixth = types.KeyboardButton("Где найти реквизиты для оплаты?")
        seventh = types.KeyboardButton("Что обязательно нужно взять на Школу?")
        eighth = types.KeyboardButton("Предоставляется ли трансфер до места сбора в Москве в день начала Школы?")

        markup.add(first, second, third, fourth, fifth, sixth, seventh, eighth)
        bot.send_message(message.chat.id, "Список:", reply_markup=markup)

    elif message.text == "Как не пропустить ничего важного на лекции и запомнить все, что рассказал преподаватель?":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        help = types.KeyboardButton("Меню")

        markup.add(help)
        bot.send_message(message.chat.id, "Как не пропустить ничего важного на лекции и запомнить все, что рассказал преподаватель?\n\nПравильно: нужно вести конспекты! Это отличная возможность систематизировать все знания и зафиксировать важную информацию, чтобы ее можно было к тому же использовать и в будущем.\n\nПоэтому сегодня мы спешим поделиться с вами лайфхаками о том, как создать самый крутой конспект!\n\n✏ Конспектируйте только самое важное.\n\nДослушайте мысль лектора до конца, подумайте и выделите в ней только самое важное. Запишите ключевые слова: имена, даты, связки, примеры. Старайтесь пересказывать, а не дословно записывать.\n\n✏ Используйте цвет.\n\nПри конспектировании можно и нужно выделять цветами понятия, определения, примеры. Это позволит мозгу быстрее определять тип информации. Вам будет проще ориентироваться в конспектах, когда нужно что-то найти. Но не увлекайтесь, а то получите раскраску. Достаточно двух-трёх основных цветов.\n\n✏ Сокращайте.\n\nПишите аббревиатуры, используйте символы, можете даже придумать свой собственный язык, но не забудьте написать чёткую легенду, в которой указано, что вы имели в виду. Тогда вы не будете потом «ломать» голову над тем, что же все это значит.\n\n✏ Решая, где вести конспекты, отталкивайтесь от задач и своего удобства.\n\nЕсли вам нужно создать базу знаний по теме — больше подойдёт электронный формат. Печатать гораздо быстрее, чем писать от руки, и конспекты получатся более подробными и простыми для поиска необходимых материалов. Если главное — запомнить и осмыслить много информации, пишите конспекты от руки. Доказано, что при конспектировании от руки студенты лучше запоминают материал лекции, и меньше отвлекаются. Поэтому через какое-то время они могут вспомнить гораздо больше, чем те, кто печатал на компьютере.\n\n✏ Структурируйте информацию.\n\nСтавьте даты, записывайте имена лекторов и нумеруйте страницы. Выделяйте главные части конспекта: темы, заголовки, определения, ключевые слова, делайте списки. Визуализируйте, используйте графику, символы — стрелки, восклицательные и вопросительные знаки, пометки такие как, например: ! — «важно», N.B. — «обратить внимание!».\n\n✏ Перечитывайте конспект.\n\nЭто важно, хоть и трудно найти на это время. Лучше делайте это несколько раз: сразу после лекции, чтобы заполнить пробелы; в течение суток после лекции, чтобы закрепить изученное; перед следующей лекцией, чтобы освежить в памяти.\n\nЕсли заинтересовала тема ведения конспектов и вы хотите стать настоящими гуру и запоминать все необходимое, то советуем почитать про популярные методы работы с текстовыми заметками: метод Корнелла, схематическое ведение конспекта, способ интеллект-карт, метод предложений, метод течения, ведение с помощью отступов, метод боксов.\n\nМетодов ведения конспекта намного больше, и какой выбрать — решать вам! Главное, чтобы вам было удобно, и работа была эффективной.\n\nПриятного конспектирования,\nВаша команда ШСН 22❤", parse_mode='html',reply_markup=markup)
    elif message.text == "Во сколько планируется отъезд из Москвы в Вороново, куда и ко скольки нужно приехать?":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        help = types.KeyboardButton("Меню")

        markup.add(help)
        bot.send_message(message.chat.id, "Мы выезжаем в понедельник (7 ноября) из Москвы в 12:30 от здания университета, поэтому к этому времени нужно обязательно быть на Мясницкой 11, примерное начало сбора — с 9 утра.\n\nОбратите внимание, что в 12:30 сбор уже заканчивается! Пожалуйста, следите за временем и не опаздывайте!",reply_markup=markup)
    elif message.text == "Во сколько и где заканчивается программа Школы в последний день 12 ноября?":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        help = types.KeyboardButton("Меню")

        markup.add(help)
        bot.send_message(message.chat.id, "Официальная программа заканчивается в 17:00 (суббота) уже в Москве на Мясницкой 11🤍",reply_markup=markup)
    elif message.text == "Будет ли осуществляться встреча и сопровождение иногородних участников?":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        help = types.KeyboardButton("Меню")

        markup.add(help)
        bot.send_message(message.chat.id, "Мы организуем волонтёров, которые смогут встретить вас в день начала Школы (7 ноября), если вы из другого города, и доехать с вами до места сбора.\n\nОбратите внимание! Волонтёры не смогут встретить вас из аэропорта, но помогут вам доехать до места встречи от какой-либо станции метро (желательно в пределах МКАД), от места прибытия аэроэкспресса или с железнодорожного вокзала. Время начало работы волонтеров ориентировочно с 7-8 утра по московскому времени.", reply_markup=markup)
    elif message.text == "Если у меня есть аллергия на какие-то продукты, где я могу это указать?":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        help = types.KeyboardButton("Меню")

        markup.add(help)
        bot.send_message(message.chat.id, "Когда вы будете отправлять письма со всеми необходимыми для участия документами, вы можете указать все индивидуальные особенности, которые могут повлиять на ваше участие в Школе, в том числе наличие аллергии, и это обязательно учтут.", reply_markup=markup)
    elif message.text == "Где найти реквизиты для оплаты?":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        help = types.KeyboardButton("Меню")

        markup.add(help)
        bot.send_message(message.chat.id, "Вся необходимая информация по оплате была выслана вместе с необходимыми для участия в Школе документами. Реквизиты по оргвзносу расположены на последней странице оферты, по ним и нужно производить оплату. Для оплаты питания в пакете есть отдельные реквизиты. Всю остальную информацию, пожалуйста, уточняйте в банке.\n\n<b>Важно!</b> Вам также необходимо не только отправить подтверждение оплаты вместе со всеми документами, но и иметь с собой на руках в день отъезда на Школу.", parse_mode='html', reply_markup=markup)
    elif message.text == "Что обязательно нужно взять на Школу?":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        help = types.KeyboardButton("Меню")

        markup.add(help)
        bot.send_message(message.chat.id, "Не пропустите, перед самой Школой мы обязательно опубликуем в группе подробный чек-лист того, что нужно не забыть!\n\n https://vk.com/school_fsn", reply_markup=markup)
    elif message.text == "Предоставляется ли трансфер до места сбора в Москве в день начала Школы?":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        help = types.KeyboardButton("Меню")

        markup.add(help)
        bot.send_message(message.chat.id, "Нет, трансфер будет осуществлен только от здания университета на Мясницкой 20 до Вороново (и обратно в крайний день школы), до места встречи в день приезда участникам будет необходимо добраться самостоятельно.", reply_markup=markup)
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
    #bot.forward_message(687388034, message.chat.id, message.message_id)

    #bot.send_message(owner, f"Отзыв: \n\n{message.text}", parse_mode='html')
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    back = types.KeyboardButton("Меню")
    #Запись в табл
    for i in range(1, 10**5):
        if worksheet.cell(i, 1).value == None:
            row = i
            break
    worksheet.update_cell(row, 4, message.from_user.id)
    worksheet.update_cell(row, 1, message.from_user.username)
    dt = str(datetime.datetime.utcnow())
    t = str((int(dt[11:13])+3)%24)
    cl=""
    for i in range(19):
        if i == 11:
            cl+=t[0]
        elif i == 12:
            cl+=t[1]
        else:
            cl+=dt[i]
    cl+="  мск"
    worksheet.update_cell(row, 2, cl)
    worksheet.update_cell(row, 3, message.text)

    g=0
    markup.add(back)
    bot.send_message(message.chat.id, f"<b>Отправлено! Спасибо за отзыв</b> 🥰", parse_mode='html', reply_markup=markup)
    love = open('love.webp', 'rb')
    bot.send_sticker(message.chat.id, love)
    bot.send_sticker(message.chat.id, "FILEID")
bot.delete_webhook()
bot.polling(none_stop=True)
