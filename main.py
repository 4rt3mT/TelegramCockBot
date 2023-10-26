import telebot;
from random import randint
from telebot import types
import sqlite3 
import csv
from time import sleep

bot = telebot.TeleBot('6054495160:AAF3k0Ye_u2P9iy3XtEwakl9Rhis-1buIFE')

con = sqlite3.connect("main.db",check_same_thread=False)
cur = con.cursor()


@bot.message_handler(commands=['start'])
def start_message(message):
    with open("users.csv", mode="r") as inp:
        reader = csv.reader(inp)
        dict_from_csv = {rows[0]: rows[1] for rows in reader}
    res = cur.execute("SELECT id FROM users WHERE id={0}".format(message.from_user.id))
    if res.fetchone() is not None:
        bot.send_message(message.chat.id, "Привет, {0.first_name}! Нажми на кнопку что вырастить писюн.".format(message.from_user))
    else:
        markup = types.ReplyKeyboardMarkup()
        button1 = types.KeyboardButton("/увеличитьпиструн")
        markup.add(button1)
        Value = randint(1,15)
        

        cur.execute("""
            INSERT INTO users VALUES
                ({0}, {1})
        """.format(message.from_user.id,Value))
        con.commit()
            
        bot.send_message(message.chat.id, "Привет, {0.first_name}! Твой писюн составляет: {1}см".format(message.from_user,str(Value)), reply_markup=markup)


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
        bot.send_message(message.chat.id, "Твой агрегат увеличился на {0}см ! Теперь его длина составляет: {1}см".format(str(Value),str(actualLength)))

            
    else:
        bot.send_message(message.chat.id, "Я твой писюн еще на знаю, сначала напиши /start")


						
while True:
    try:
        bot.polling(none_stop=True)
    except Exception as _ex:
        print(_ex)
        sleep(3)


