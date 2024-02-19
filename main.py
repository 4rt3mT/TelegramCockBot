import telebot;
from random import randint,choice

from telebot import types
import sqlite3 
import csv
from time import sleep
import pymorphy2
from datetime import date, datetime, timedelta


bot = telebot.TeleBot('6054495160:AAF3k0Ye_u2P9iy3XtEwakl9Rhis-1buIFE')

con = sqlite3.connect("main.db",check_same_thread=False)
cur = con.cursor()
morph = pymorphy2.MorphAnalyzer()


def Inflect(word):
    return morph.parse(word)[0].inflect({'gent'}).word

def WomanOrMen(word):
    p = morph.parse(word)[0]

    lastChar = word[-1]
    if p.tag.gender == "femn":
        Sex = 'Твоя'
    elif p.tag.gender == "masc":
        Sex = 'Твой'
    else:
        Sex = 'Твоё'

    return Sex





ArrayOfDickNames = [
    "Анаконда", 
    "Банан", 
    "Стояк", 
    "Сосиска", 
    "Выпуклость", 
    "Диккенс", 
    "Динь-дон", 
    "Палочка", 
    "Экскалибур",  
    "Фасоль", 
    "Корнишон", 
    "Голдфингер", 
    "Шланг", 
    "Молоток", 
    "Джимми", 
    "Джонсон", 
    "Джонсон", 
    "Джойстик", 
    "Младший", 
    "Мусор", 
    "Ручка", 
    "Хобгоблин", 
    "Лерой", 
    "Парень", 
    "Стояк", 
    "Молоток", 
    "Геркулес", 
    "Джойстик", 
    "Палка", 
    "Участник", 
    "Дик", 
    "Везувий", 
    "Пит", 
    "Монстр", 
    "Змея", 
    "Упаковка", 
    "Пепперони", 
    "Огурец", 
    "Поршень", 
    "Залупа", 
    "Ракета", 
    "Эскимо",  
    "Питон", 
    "Стержень", 
    "Салями", 
    "Колбаса", 
    "Шланг", 
    "Вал", 
    "Змея", 
    "Стиффи", 
    "Нога", 
    "Тор", 
    "Ствол", 
    "Тунец"
]



def getDickLenght(Value):
    if Value <= 0:
        dick = "<3"
        return dick
    elif Value <=10:
        dick = "<=3"
        return dick
    charCount = int(Value / 10)
    dick = "<" + "=" * charCount + "3"
    return dick

@bot.message_handler(commands=['start'])
def start_message(message):
    
    res = cur.execute("SELECT id FROM users WHERE id={0}".format(message.from_user.id))
    if res.fetchone() is not None:
        DickName = Inflect(choice(ArrayOfDickNames).lower())
        bot.send_message(message.chat.id, "Привет, {0.first_name}! Нажми на кнопку что вырастить {1}.".format(message.from_user,DickName))
    else:
        markup = types.ReplyKeyboardMarkup()
        #button1 = types.KeyboardButton("/dick")
        #markup.add(button1)
        Value = randint(1,15)
        dickString = getDickLenght(Value)
        

        cur.execute("""
            INSERT INTO users VALUES
                ({0}, {1},"{2}","","",NULL)
        """.format(message.from_user.id,Value,message.from_user.first_name))
        con.commit()
        DickName = choice(ArrayOfDickNames).lower()
        DickFullName = "Твой" +" "+ DickName    
        bot.send_message(message.chat.id, "Привет, {0.first_name}! {2} составляет: {1}см".format(message.from_user,str(Value),DickFullName), reply_markup=markup)
        bot.send_message(message.chat.id, "Член {0.first_name} выглядит так: \n  {1}".format(message.from_user,dickString))

@bot.message_handler(commands=['topdicks'])
def start_message(message):
    res = cur.execute("SELECT id,value,name FROM users ORDER BY value DESC".format(message.from_user.id))
    result = res.fetchall()
    if result is not None:
        stringOfDicks = ""
        first = True
        for Dick in result:
            
            if Dick[2] is None:
                Name = Dick[0]
            else:
                Name = Dick[2]
            if first:
                crown = "👑"
                first = False
            else:
                crown = ""
            stringOfDicks = stringOfDicks + crown  +str(Name) +crown + " - " + str(Dick[1]) + " см \n"
        
        bot.send_message(message.chat.id, stringOfDicks)
    

@bot.message_handler(commands=['dick'])
def pistrun(message):

    res = cur.execute("SELECT id,value,lastgrow FROM users WHERE id={0}".format(message.from_user.id))
    result = res.fetchone()
    
    if result is not None:
        AllowGrow = True
        if result[2] is not None:
            LastGrow = datetime.strptime(result[2],"%Y-%m-%d")
            Today = date.today()
            Delta = datetime(Today.year, Today.month, Today.day) - LastGrow
            if Delta != 0:
                AllowGrow = False
        if AllowGrow == False:
            DickName = choice(ArrayOfDickNames).lower()
            DickFullName = WomanOrMen(DickName) +" "+ DickName
            bot.send_message(message.chat.id, "{0} отдыхает. Попробуй завтра".format(DickFullName))
        else:        
            print(result[0])
            actualLength = int(result[1])
            Value = randint(-5,10)
            actualLength = actualLength + Value
            dickString = getDickLenght(actualLength)
            query1 = '''
                UPDATE users
                SET value = {0}, name = "{2}", lastgrow="{3}"
                WHERE id = {1};
                '''.format(actualLength,result[0],message.from_user.first_name,date.today())
            cur.execute(query1)
            con.commit()
            DickName = choice(ArrayOfDickNames).lower()
            DickFullName = WomanOrMen(DickName) +" "+ DickName
            bot.send_message(message.chat.id, "{2} увеличился на {0}см ! Теперь его длина составляет: {1}см".format(str(Value),str(actualLength),DickFullName))
            bot.send_message(message.chat.id, "Член {0.first_name} выглядит так: \n  {1}".format(message.from_user,dickString))

            
    else:
        DickName = choice(ArrayOfDickNames).lower()
        DickFullName = WomanOrMen(DickName) +" "+ DickName
        bot.send_message(message.chat.id, "Я {0} еще не знаю, щас запишу...".format(DickFullName.lower()))
        markup = types.ReplyKeyboardMarkup()
        #button1 = types.KeyboardButton("/увеличитьпиструн")
        #markup.add(button1)
        Value = randint(1,15)
        dickString = getDickLenght(Value)
        
        cur.execute("""
            INSERT INTO users VALUES
                ({0}, {1}, "{2}","","",NULL)
        """.format(message.from_user.id,Value,message.from_user.first_name))
        con.commit()
            
        bot.send_message(message.chat.id, "Привет, {0.first_name}! {2} составляет: {1}см".format(message.from_user,str(Value),DickFullName), reply_markup=markup)
        bot.send_message(message.chat.id, "Член {0.first_name} выглядит так: \n  {1}".format(message.from_user,dickString))



						
while True:
    try:
        bot.polling(none_stop=True)
    except Exception as _ex:
        print(_ex)
        sleep(3)


