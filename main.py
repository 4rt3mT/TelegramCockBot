import telebot;
from random import randint,choice

from telebot import types
import sqlite3 
import csv
from time import sleep
import pymorphy2


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

@bot.message_handler(commands=['start'])
def start_message(message):
    with open("users.csv", mode="r") as inp:
        reader = csv.reader(inp)
        dict_from_csv = {rows[0]: rows[1] for rows in reader}
    res = cur.execute("SELECT id FROM users WHERE id={0}".format(message.from_user.id))
    if res.fetchone() is not None:
        DickName = Inflect(choice(ArrayOfDickNames).lower())
        bot.send_message(message.chat.id, "Привет, {0.first_name}! Нажми на кнопку что вырастить {1}.".format(message.from_user,DickName))
    else:
        markup = types.ReplyKeyboardMarkup()
        button1 = types.KeyboardButton("/увеличитьпиструн")
        markup.add(button1)
        Value = randint(1,15)
        

        cur.execute("""
            INSERT INTO users VALUES
                ({0}, {1},{2})
        """.format(message.from_user.id,Value,message.from_user.first_name))
        con.commit()
        DickName = choice(ArrayOfDickNames).lower()
        DickFullName = WomanOrMen(DickName) +" "+ DickName    
        bot.send_message(message.chat.id, "Привет, {0.first_name}! {2} составляет: {1}см".format(message.from_user,str(Value),DickFullName), reply_markup=markup)


@bot.message_handler(commands=['увеличитьпиструн'])
def pistrun(message):
    with open("users.csv", mode="r") as inp2:
        reader2 = csv.reader(inp2)
        dict_from_csv2 = {rows2[0]: rows2[1] for rows2 in reader2}
    res = cur.execute("SELECT id,value FROM users WHERE id={0}".format(message.from_user.id))
    result = res.fetchone()
    if result is not None:
        print(result[0])
        actualLength = int(result[1])
        Value = randint(-5,10)
        actualLength = actualLength + Value
        query1 = '''
            UPDATE users
            SET value = {0}
            WHERE id = {1};
            '''.format(actualLength,result[0])
        cur.execute(query1)
        con.commit()
        DickName = choice(ArrayOfDickNames).lower()
        DickFullName = WomanOrMen(DickName) +" "+ DickName
        bot.send_message(message.chat.id, "{2} увеличился на {0}см ! Теперь его длина составляет: {1}см".format(str(Value),str(actualLength),DickFullName))

            
    else:
        DickName = choice(ArrayOfDickNames).lower()
        DickFullName = WomanOrMen(DickName) +" "+ DickName
        bot.send_message(message.chat.id, "Я {0} еще не знаю, щас запишу...".format(DickFullName.lower()))
        markup = types.ReplyKeyboardMarkup()
        button1 = types.KeyboardButton("/увеличитьпиструн")
        markup.add(button1)
        Value = randint(1,15)
        

        cur.execute("""
            INSERT INTO users VALUES
                ({0}, {1}, {2})
        """.format(message.from_user.id,Value,message.from_user.first_name))
        con.commit()
            
        bot.send_message(message.chat.id, "Привет, {0.first_name}! {2} составляет: {1}см".format(message.from_user,str(Value),DickFullName), reply_markup=markup)



						
while True:
    try:
        bot.polling(none_stop=True)
    except Exception as _ex:
        print(_ex)
        sleep(3)


