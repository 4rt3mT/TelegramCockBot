import telebot;
import requests;
from random import randint,choice
from deep_translator import GoogleTranslator

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

def plural_days(n):
    days = ['день', 'дня', 'дней']
    
    if n % 10 == 1 and n % 100 != 11:
        p = 0
    elif 2 <= n % 10 <= 4 and (n % 100 < 10 or n % 100 >= 20):
        p = 1
    else:
        p = 2

    return str(n) + ' ' + days[p]

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
                ({0}, {1}, "{2}","","","{3}",0,"{4}")
        """.format(message.from_user.id,Value,message.from_user.first_name, date.today(), date.today()))
        con.commit()
        DickName = choice(ArrayOfDickNames).lower()
        DickFullName = "Твой" +" "+ DickName    
        bot.send_message(message.chat.id, "Привет, {0.first_name}! {2} составляет: {1}см".format(message.from_user,str(Value),DickFullName), reply_markup=markup)
        bot.send_message(message.chat.id, "Член {0.first_name} выглядит так: \n  {1}".format(message.from_user,dickString))

@bot.message_handler(commands=['topdicks'])
def start_message(message):
    res = cur.execute("SELECT id,value,name FROM users ORDER BY value DESC".format(message.from_user.id))
    result = res.fetchall()
    
    res2 = cur.execute("SELECT id,days,lastUpdate FROM topDudes ORDER BY days DESC LIMIT 1")
    result2 = res2.fetchone()
   
    if result is not None:
        stringOfDicks = ""
        first = True
        last = len(result)
        now = 1
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
            if now == last:
                crown = "💀"
            
            if str(Dick[0]) == str(result2[0]):
                topName = Dick[2]
                top = " - " + plural_days(result2[1])

            
            stringOfDicks = stringOfDicks + crown  +str(Name) +crown + " - " + str(Dick[1]) + " см \n"
            now = now + 1
        
        bot.send_message(message.chat.id, stringOfDicks)
        bot.send_message(message.chat.id, "👑" +topName+ "👑" + " в топе уже " + plural_days(result2[1]) )
    

@bot.message_handler(commands=['dick'])
def pistrun(message):

    res = cur.execute("SELECT id,value,lastgrow FROM users WHERE id={0}".format(message.from_user.id))
    result = res.fetchone()
    print(message.chat.id)
    if result is not None:
        AllowGrow = True
        if result[2] is not None:
            LastGrow = datetime.strptime(result[2],"%Y-%m-%d")

            Today = date.today()

            Delta = datetime(Today.year, Today.month, Today.day) - LastGrow

            if Delta.days == 0:
                AllowGrow = False
        if AllowGrow == False:
            DickName = choice(ArrayOfDickNames).lower()
            DickFullName = WomanOrMen(DickName) +" "+ DickName
            bot.send_message(message.chat.id, "{0} отдыхает. Попробуй завтра".format(DickFullName))
        else:        
            
            
            
            actualLength = int(result[1])

            
            res3 = cur.execute("SELECT id,value,name FROM users ORDER BY value DESC LIMIT 1")
            result3 = res3.fetchone()
            advanceGrow = False
            print(round((result3[1] - actualLength) / 4))
            print((result3[1] - actualLength) / 4)
            if result3[1] - actualLength > 40:
                advanceGrow = True
            
            if advanceGrow == True:
                maxGrow = round((result3[1] - actualLength) / 4)
            else:
                maxGrow = 10
            
            print(maxGrow)
               
            RandGrow = randint(1,100)
            if RandGrow <= 10:
                Value = randint(-10,0)
            else:
                Value = randint(0,maxGrow)
                
                
            if Value >= 0:
                GrowOrNo = "увеличился"
            else:
                GrowOrNo = "уменьшился"
            actualLength = actualLength + Value
            dropDick = randint(1,100)
            death = False
            if dropDick == 1:
                actualLength = 0
                death = True
            
    
            res2 = cur.execute("SELECT id,days,lastUpdate FROM topDudes ORDER BY days DESC LIMIT 1")
            result2 = res2.fetchone()
            if result[0] != result3[0]:

                if actualLength > int(result3[1]):
                    
                    query1 = '''
                        UPDATE topDudes
                        SET days = 1, id = {0}, lastUpdate="{1}"
                        WHERE id = {2};
                        '''.format(result[0],date.today(),result2[0])
                      
                    print("here2")
                    print(result[0])
                    print(result2[0])
                    cur.execute(query1)
                    con.commit()
                    #bot.send_message(message.chat.id, message.from_user.first_name + " теперь на первом месте.")
                    print("here3")
            else:
                print("here4")
                if actualLength > int(result3[1]):
                    query1 = '''
                        UPDATE topDudes
                        SET days = {3}, id = {0}, lastUpdate="{1}"
                        WHERE id = {2};
                        '''.format(result[0],date.today(),result2[0], result2[1] + 1)
                    cur.execute(query1)
                    con.commit()
                if actualLength < int(result3[1]):
                    
                    res4 = cur.execute("SELECT id,value,name FROM users ORDER BY value DESC LIMIT 2")
                    result4 = res4.fetchall()
                    
                    query1 = '''
                        UPDATE topDudes
                        SET days = {3}, id = {0}, lastUpdate="{1}"
                        WHERE id = {2};
                        '''.format(result4[1][0],date.today(),result2[0], 1)
                    cur.execute(query1)
                    con.commit()
                    #bot.send_message(message.chat.id, result3[2] + " теперь на первом месте.")
    
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
            if death == False:
                bot.send_message(message.chat.id, "{2} {3} на {0}см ! Теперь его длина составляет: {1}см".format(str(Value),str(actualLength),DickFullName, GrowOrNo))
                bot.send_message(message.chat.id, "Член {0.first_name} выглядит так: \n  {1}".format(message.from_user,dickString))
                
                response = requests.get("http://numbersapi.com/" + str(actualLength))
                text_Eng = response.text
                text_Rus = GoogleTranslator(source='auto', target='ru').translate(text_Eng)
                bot.send_message(message.chat.id, text_Rus)
            else:
                bot.send_message(message.chat.id, "{2} {3} отвалился ! Теперь его длина составляет: {1}см".format(str(Value),str(actualLength),DickFullName, GrowOrNo))
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
                ({0}, {1}, "{2}","","","{3}",0,"{4}")
        """.format(message.from_user.id,Value,message.from_user.first_name, date.today(), date.today()))
        con.commit()
            
        bot.send_message(message.chat.id, "Привет, {0.first_name}! {2} составляет: {1}см".format(message.from_user,str(Value),DickFullName), reply_markup=markup)
        bot.send_message(message.chat.id, "Член {0.first_name} выглядит так: \n  {1}".format(message.from_user,dickString))

@bot.message_handler(commands=['fact'])
def getFact(message):
    Number = "228"
    
    response = requests.get("http://numbersapi.com/228")

    
    text_Eng = response.text
    text_Rus = GoogleTranslator(source='auto', target='ru').translate(text_Eng)
    bot.send_message(message.chat.id, text_Rus)
    
 
@bot.message_handler(commands=['all'])
def getFact(message):
    
    bot.send_message(message.chat.id, "@nohopeman @basangbasasiya @Nanuvie @FUCK_YOU_PIDORAS @Noface812 @Dante_Rage @wwwPlan4ik @YungJ1 - Вас вызывают на разговор")
       
@bot.message_handler(commands=['change'])
def add_length(message):
    # Проверяем, имеет ли пользователь айди 696969
    if message.from_user.id != 1063677223:
        bot.send_message(message.chat.id, "У вас нет разрешения на выполнение этой команды.")
        return

    # Разбиваем сообщение на айди и значение для увеличения
    try:
        _, user_id, increase_value = message.text.split()
        user_id = str(user_id)
        increase_value = int(increase_value)
    except ValueError:
        bot.send_message(message.chat.id, "Неправильный формат сообщения. Используйте /AddLenght <name> <value>")
        return

    # Проверяем, есть ли пользователь с указанным айди в базе данных
    res = cur.execute("SELECT id, value, name FROM users WHERE name=?", (user_id,))
    result = res.fetchone()
    if result is None:
        bot.send_message(message.chat.id, "Пользователя с таким именем не найдено.")
        return

    # Увеличиваем значение и обновляем базу данных
    new_value = result[1] + increase_value
    query = '''
            UPDATE users
            SET value = ?
            WHERE name = ?;
            '''
    cur.execute(query, (new_value, user_id))
    con.commit()

    bot.send_message(message.chat.id, f"Длина члена пользователя {result[2]} изменена на {increase_value} см. Новая длина: {new_value} см.")

def get_combo_text(dice_value: int):
    """
    Возвращает то, что было на конкретном дайсе-казино
    :param dice_value: значение дайса (число)
    :return: массив строк, содержащий все выпавшие элементы в виде текста

    Альтернативный вариант (ещё раз спасибо t.me/svinerus):
        return [casino[(dice_value - 1) // i % 4]for i in (1, 4, 16)]
    """
    #           0       1         2        3
    values = ["BAR", "виноград", "лимон", "семь"]

    dice_value -= 1
    result = []
    for _ in range(3):
        result.append(values[dice_value % 4])
        dice_value //= 4
    return result

@bot.message_handler(commands=['slot'])
def slot(message):
    
    bot.send_message(message.chat.id, message.from_user.first_name + " крутит рулетку..." )
    
    res = cur.execute("SELECT id, value, name, casino, casinodate FROM users WHERE name=?", (message.from_user.first_name,))
    result = res.fetchone()
    if result is None:
        bot.send_message(message.chat.id, "Пользователя с таким именем не найдено.")
        return
    
    tickets = result[3]
    
    Time = date.today()
    
    AllowGrow = True
    if result[4] is not None:
        LastGrow = datetime.strptime(result[4],"%Y-%m-%d")

        Today = date.today()

        Delta = datetime(Today.year, Today.month, Today.day) - LastGrow

        if Delta.days == 0:
            AllowGrow = False
    else:
        
        query = '''
            UPDATE users
            SET casinodate = ?
            WHERE name = ?;
            '''
        cur.execute(query, (Time, message.from_user.first_name))
        con.commit()
        tickets = 0
        
    if AllowGrow == True:
        tickets = 0
        Time = date.today()
        query = '''
            UPDATE users
            SET casinodate = ?
            WHERE name = ?;
            '''
        cur.execute(query, (Time, message.from_user.first_name))
        con.commit()

    
    
    if tickets >= 5:
        bot.send_message(message.chat.id, "Сегодня больше крутить нельзя. Попробуйте завтра.")
        return
    # Увеличиваем значение и обновляем базу данных
    new_value = result[1] - 1
    tickets = tickets + 1
    query = '''
            UPDATE users
            SET value = ?, casino = ?
            WHERE name = ?;
            '''
    cur.execute(query, (new_value,tickets, message.from_user.first_name))
    con.commit()
    
    grow = True
    data = bot.send_dice(message.chat.id, emoji='🎰')
    sleep(1.5)
    resultCombo = get_combo_text(data.dice.value)
    if resultCombo[0] == "семь" and resultCombo[0] == resultCombo[1] and resultCombo[0] == resultCombo[2]: # Три семерки
        text = "ДЖЕКПОТ! Ваш писюн увеличился на 7см"
        new_value = int(result[1]) + 8
    elif resultCombo[0] == "семь" and resultCombo[0] == resultCombo[1]:                          # Две семерки
        text = "Поздравляю, вы выиграли. Ваш писюн увеличился на 5 см."
        new_value = int(result[1]) + 6
    elif resultCombo[0] == "BAR" and  resultCombo[0] == resultCombo[1] and resultCombo[0] == resultCombo[2]: # Три бара
        text = "Поздравляю, вы выиграли... Но не то что хотелось,  ваш писюн уменьшился на 5 см."
        new_value = int(result[1]) - 4
    elif resultCombo[0] == "BAR" and  resultCombo[0] == resultCombo[1]:                                         # Два бара
        text = "Поздравляю, вы выиграли. Ваш писюн увеличился на 3 см."
        new_value = int(result[1]) + 4
    elif resultCombo[0] == "виноград" and  resultCombo[0] == resultCombo[1] and resultCombo[0] == resultCombo[2]: # Три винограда
        text = "Поздравляю, вы выиграли. Ваш писюн увеличился на 4 см."
        new_value = int(result[1]) + 5
    elif resultCombo[0] == "виноград" and  resultCombo[0] == resultCombo[1]:                                         # Два винограда
        text = "Поздравляю, вы выиграли. Ваш писюн увеличился на 2 см."
        new_value = int(result[1]) + 3
    elif resultCombo[0] == "лимон" and  resultCombo[0] == resultCombo[1] and resultCombo[0] == resultCombo[2]:  # Три лимона
        text = "Поздравляю, вы выиграли. Ваш писюн увеличился на 6 см."
        new_value = int(result[1]) + 7
    elif resultCombo[0] == "лимон" and  resultCombo[0] == resultCombo[1]:                                         # Два лимона
        text = "Поздравляю, вы выиграли. Ваш писюн увеличился на 3 см."
        new_value = int(result[1]) + 4
    elif resultCombo[1] == "BAR" and  resultCombo[1] == resultCombo[2]:                                         # Два бара сзади
        text = "Поздравляю, вы выиграли. Ваш писюн увеличился на 3 см."
        new_value = int(result[1]) + 4
    elif resultCombo[1] == "виноград" and  resultCombo[1] == resultCombo[2]:                                         # Два винограда сзади
        text = "Поздравляю, вы выиграли. Ваш писюн увеличился на 3 см."
        new_value = int(result[1]) + 4
    elif resultCombo[1] == "лимон" and  resultCombo[1] == resultCombo[2]:                                         # Два лимона сзади
        text = "Поздравляю, вы выиграли. Ваш писюн увеличился на 3 см."
        new_value = int(result[1]) + 4
    elif resultCombo[1] == "семь" and resultCombo[1] == resultCombo[2]:                          # Две семерки C ЖОПЫ ЧТОБЫ ТЕТЕ САШЕ БЫЛО ПРИЯТНО
        text = "Поздравляю, вы выиграли. Ваш писюн увеличился на 5 см."
        new_value = int(result[1]) + 6
    elif resultCombo[0] == resultCombo[2]:
        text = "Вы ничего не проиграли."
        new_value = result[1] + 1
    else:
        text = "Вы проиграли. Писюн уменьшился на 1см"
        grow = False

    if grow == True:
        query = '''
        UPDATE users
        SET value = ?
        WHERE name = ?;
        '''
        cur.execute(query, (new_value, message.from_user.first_name))
        con.commit()
            
    
    
    bot.send_message(message.chat.id, text )
   
						
while True:
    try:
        #bot.send_message("-1002101471139", "#остановитесь")
        bot.polling(none_stop=True)
    except Exception as _ex:
        print(_ex)
        sleep(3)


