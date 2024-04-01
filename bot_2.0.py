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
        #bot.send_message(message.chat.id, "👑" +topName+ "👑" + " в топе уже " + plural_days(result2[1]) )
    

import requests
from random import randint, choice
from datetime import datetime, date
from googletrans import Translator
from telebot import types

translator = Translator()

def get_user_data(user_id):
    """Получает данные пользователя из базы данных"""
    res = cur.execute("SELECT id, value, lastgrow FROM users WHERE id={0}".format(user_id))
    return res.fetchone()

def is_growable(last_grow):
    """Проверяет, можно ли увеличить член пользователя"""
    if last_grow is None:
        return True
    last_grow_date = datetime.strptime(last_grow, "%Y-%m-%d")
    today = date.today()
    delta = datetime(today.year, today.month, today.day) - last_grow_date
    return delta.days != 0

def get_max_grow(result, actual_length):
    """Вычисляет максимальный прирост длины члена"""
    res3 = cur.execute("SELECT id, value, name FROM users ORDER BY value DESC LIMIT 1")
    result3 = res3.fetchone()
    advance_grow = result3[1] - actual_length > 40
    if advance_grow:
        return round((result3[1] - actual_length) / 4)
    else:
        return 10

def update_hall_of_fame(user_id, strike):
    """Обновляет данные в таблице 'Зал Славы'"""
    # Проверяем, есть ли пользователь уже в Зале Славы
    res = cur.execute("SELECT id, strike FROM HallOfFame WHERE user_id=?", (user_id,))
    hall_of_fame_entry = res.fetchone()

    if hall_of_fame_entry:
        # Если пользователь уже в Зале Славы и его текущий стрик больше сохраненного, обновляем запись
        if strike > hall_of_fame_entry[1]:
            query_update = '''
                UPDATE HallOfFame
                SET strike = ?
                WHERE user_id = ?
            '''
            cur.execute(query_update, (strike, user_id))
            con.commit()
    else:
        # Если пользователь не в Зале Славы, добавляем его туда
        query_insert = '''
            INSERT INTO HallOfFame (user_id, strike)
            VALUES (?, ?, ?)
        '''
        cur.execute(query_insert, (user_id, strike))
        con.commit()


def update_top_dude():
    """Обновляет информацию о пользователе в топе"""
    today_date = date.today()

    # Получаем данные о пользователе с самым высоким значением
    res_top_user = cur.execute("SELECT id, value, name FROM users ORDER BY value DESC LIMIT 1")
    top_user = res_top_user.fetchone()

    # Получаем данные о текущем пользователе в топе, если таковой есть
    res_top_dude = cur.execute("SELECT id, days, lastUpdate FROM topDudes")
    top_dude = res_top_dude.fetchone()

    if top_dude:
        # Если текущий пользователь совпадает с новым и текущая дата отличается от последнего обновления
        if top_dude[0] == top_user[0] and top_dude[2] != today_date:
            # Обновляем данные в таблице topDudes для текущего пользователя
            query_update = '''
                UPDATE topDudes
                SET days = days + 1, lastUpdate = "{0}"
            '''.format(today_date)
            cur.execute(query_update)
            con.commit()
        elif top_dude[0] != top_user[0]:
            # Если пользователь отличается или текущая дата не отличается от последнего обновления,
            # просто обновляем дату последнего обновления
            update_hall_of_fame(top_dude[0],top_dude[1])
            query_update_date = '''
                UPDATE topDudes
                SET id = {0}, days = 1, lastUpdate = "{1}"
            '''.format(top_user[0], today_date)
            cur.execute(query_update_date)
            con.commit()
    else:
        # Если в таблице нет данных, добавляем новую запись
        query_insert = '''
            INSERT INTO topDudes (id, days, lastUpdate)
            VALUES ({0}, 1, "{1}")
        '''.format(top_user[0], today_date)
        cur.execute(query_insert)
        con.commit()

def update_user_data(result, actual_length, first_name):
    """Обновляет данные пользователя в базе данных"""
    query1 = '''
        UPDATE users
        SET value = {0}, name = "{2}", lastgrow="{3}"
        WHERE id = {1};
        '''.format(actual_length, result[0], first_name, date.today())
    cur.execute(query1)
    con.commit()

def send_grow_message(bot, message, actual_length, Value, DickFullName, GrowOrNo, dickString):
    """Отправляет сообщение о приросте длины члена"""
    bot.send_message(message.chat.id, "{2} {3} на {0}см ! Теперь его длина составляет: {1}см".format(str(Value), str(actual_length), DickFullName, GrowOrNo))
    bot.send_message(message.chat.id, "Член {0.first_name} выглядит так: \n  {1}".format(message.from_user, dickString))
    response = requests.get("http://numbersapi.com/" + str(actual_length))
    text_Eng = response.text
    text_Rus = translator.translate(text_Eng, dest='ru').text
    bot.send_message(message.chat.id, text_Rus)

def send_death_message(bot, message, actual_length, DickFullName, GrowOrNo, dickString):
    """Отправляет сообщение о смерти члена"""
    bot.send_message(message.chat.id, "{2} {3} отвалился ! Теперь его длина составляет: {1}см".format(str(Value), str(actual_length), DickFullName, GrowOrNo))
    bot.send_message(message.chat.id, "Член {0.first_name} выглядит так: \n  {1}".format(message.from_user, dickString))

@bot.message_handler(commands=['dick'])
def pistrun(message):
    user_data = get_user_data(message.from_user.id)
    if user_data:
        result = user_data
        AllowGrow = is_growable(result[2])
        if not AllowGrow:
            DickName = choice(ArrayOfDickNames).lower()
            DickFullName = WomanOrMen(DickName) +" "+ DickName
            bot.send_message(message.chat.id, "{0} отдыхает. Попробуй завтра".format(DickFullName))
        else:
            DickName = choice(ArrayOfDickNames).lower()
            DickFullName = WomanOrMen(DickName) +" "+ DickName
            actualLength = int(result[1])
            res3 = cur.execute("SELECT id,value,name FROM users ORDER BY value DESC LIMIT 1")
            result3 = res3.fetchone()
            
            maxGrow = get_max_grow(result, actualLength)
            Value = randint(-10, maxGrow) if randint(1, 100) <= 10 else randint(0, maxGrow)
            GrowOrNo = "увеличился" if Value >= 0 else "уменьшился"
            actualLength += Value
            death = randint(1, 100) == 1
            #update_top_dudes(result,result3, actualLength)
            update_user_data(result, actualLength, message.from_user.first_name)
            dickString = getDickLenght(actualLength)
            if not death:
                send_grow_message(bot, message, actualLength, Value, DickFullName, GrowOrNo, dickString)
            else:
                send_death_message(bot, message, actualLength, DickFullName, GrowOrNo, dickString)
    else:
        DickName = choice(ArrayOfDickNames).lower()
        DickFullName = WomanOrMen(DickName) +" "+ DickName
        bot.send_message(message.chat.id, "Я {0} еще не знаю, щас запишу...".format(DickFullName.lower()))
        Value = randint(1, 15)
        dickString = getDickLenght(Value)
        cur.execute("""
            INSERT INTO users VALUES
                ({0}, {1}, "{2}","","","{3}",0,"{4}")
        """.format(message.from_user.id, Value, message.from_user.first_name, date.today(), date.today()))
        con.commit()
        bot.send_message(message.chat.id, "Привет, {0.first_name}! {2} составляет: {1}см".format(message.from_user, str(Value), DickFullName), reply_markup=markup)
        bot.send_message(message.chat.id, "Член {0.first_name} выглядит так: \n {1}".format(message.from_user, dickString))



@bot.message_handler(commands=['duel'])
def duel_command(message):

    print(message.chat.id)
    if message.chat.id != -1002101471139:
        bot.reply_to(message, "Иди-ка ты нахуй, наебать не получится")
        return

    if len(message.text.split()) != 2 and len(message.text.split()) != 3:
        bot.reply_to(message, "Используйте команду /duel [имя_пользователя]")
        return
    
    # Получаем имя пользователя, которому предложен дуэль
    challenged_name = message.text.split()[1]
    
    
    if len(message.text.split()) == 3:
        debt =  message.text.split()[2]
    else:
        debt = "5"
        
    if int(debt) > 50:
        bot.reply_to(message, "Ставка не может быть выше 50")
        return
    if int(debt) < 0:
        bot.reply_to(message, "Сука ну ты  дурак? Нахуя вот мне думать и обрабатывать событие когда какой то чушпан напишет число меньше нуля")
        return
        
        
    # Получаем id пользователя, которому предложен дуэль
    cur.execute("SELECT id FROM users WHERE name=?", (challenged_name,))
    row = cur.fetchone()
    if row is None:
        bot.reply_to(message, f"Пользователь {challenged_name} не найден")
        return
    challenged_id = row[0]


    
    # Получаем id пользователя, который предложил дуэль
    challenger_id = message.from_user.id
    cur.execute("SELECT value FROM users WHERE id=?", (challenged_id,))
    actualDick = cur.fetchone()[0]
    if int(actualDick) < int(debt):
        bot.reply_to(message, "У тебя итак долг, куда еще больше")
        return
    # Получаем id пользователя, которому предложен дуэль
    cur.execute("SELECT id FROM users WHERE name=?", (challenged_name,))
    row = cur.fetchone()
    if row is None:
        bot.reply_to(message, f"Пользователь {challenged_name} не найден")
        return
    challenged_id = row[0]
    
    if challenged_id == challenger_id:
        bot.reply_to(message, f"🤡")
        return

    # Добавляем игру в таблицу duels со статусом "Ожидание"
    

    # Отправляем сообщение о вызове на дуэль и кнопки Принять, Отказаться
    markup = telebot.types.InlineKeyboardMarkup()
    accept_button = telebot.types.InlineKeyboardButton("Принять ✔", callback_data='accept')
    decline_button = telebot.types.InlineKeyboardButton("Отказаться ❌", callback_data='decline')
    markup.row(accept_button, decline_button)
    msg = bot.send_message(message.chat.id, f"[{challenged_name}](tg://user?id={challenged_id}) вас вызывают на дуэль 🎲 Ставка: {debt}", reply_markup=markup, parse_mode='MarkdownV2')
    cur.execute("INSERT INTO duels (id,challenger_id, challenged_id, status) VALUES (?,?, ?, ?)", (msg.message_id,challenger_id, challenged_id, "Ожидание"))
    con.commit()
    
    
# Обработчик нажатий на кнопки Принять, Отказаться
@bot.callback_query_handler(func=lambda call: True)
def handle_callback_query(call):
    # Получаем id пользователя, который нажал на кнопку
    user_id = call.from_user.id
    
    # Получаем id пользователя, который предложил дуэль
    print(call.message.message_id)
    cur.execute("SELECT challenger_id,challenged_id FROM duels WHERE id=?", (call.message.message_id,))
    duel_data = cur.fetchone()
    

    
    if duel_data:
        challenger_id, challenged_id = duel_data
        debt = call.message.text
        debt = int(debt.split("Ставка: ",1)[1])
        cur.execute("SELECT name FROM users WHERE id=?", (challenged_id,))
        challenged_name = cur.fetchone()[0]
        
        cur.execute("SELECT name FROM users WHERE id=?", (challenger_id,))
        challenger_name = cur.fetchone()[0]
        
        if call.data == 'accept':
            # Если пользователь нажал на кнопку Принять, и это именно тот, кому предложили игру
            if user_id == challenged_id:
                # Обновляем статус игры на "Идет игра"
                cur.execute("UPDATE duels SET status=? WHERE id=?", ("Идет игра", call.message.message_id))
                con.commit()
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                      text=f"Игра началась!\n{challenger_name} против {challenged_name}")
                data = bot.send_dice(call.message.chat.id, emoji='🎲', reply_to_message_id  = call.message.message_id)
                data2 = bot.send_dice(call.message.chat.id, emoji='🎲', reply_to_message_id  = call.message.message_id)
                sleep(2.8)
                result_challenger = data.dice.value
                result_challenged = data2.dice.value
                if result_challenger > result_challenged:
                    cur.execute("UPDATE users SET value = value + ? WHERE id=?", (debt,challenger_id,))
                    cur.execute("UPDATE users SET value = value - ? WHERE id=?", (debt,challenged_id,))
                    bot.reply_to(call.message, f"Победитель: {challenger_name}")
                    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                      text=f"Игра закончилась ✔\n{challenger_name} против {challenged_name}\n----------\nИтог: {challenger_name} - победитель.")
                    
                elif result_challenged == result_challenger:
                    bot.reply_to(call.message, f"Ничья!")
                    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                      text=f"Игра закончилась ✔\n{challenger_name} против {challenged_name}\n----------\nИтог: Ничья")
                else:
                    

                    cur.execute("UPDATE users SET value = value - ? WHERE id=?", (debt,challenger_id,))
                    cur.execute("UPDATE users SET value = value + ? WHERE id=?", (debt,challenged_id,))
                    bot.reply_to(call.message, f"Победитель: {challenged_name}\n")
                    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                      text=f"Игра закончилась ✔\n{challenger_name} против {challenged_name}\n----------\nИтог: {challenged_name} - победитель.")
                cur.execute("UPDATE duels SET status=? WHERE id=?", ("Завершена", call.message.message_id))
                con.commit()
            else:
                bot.send_message(call.message.chat.id, f"🤡 {call.from_user.first_name}, вы не можете принять эту игру, так как вас не вызывали на дуэль.")
        elif call.data == 'decline':
            if user_id == challenged_id:
                # Редактируем сообщение, убирая inline кнопки и добавляя текст "Дуэль отменена"
                cur.execute("UPDATE duels SET status=? WHERE id=?", ("Игра отменена", call.message.message_id))
                con.commit()
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                      text="Дуэль отменена ❌")
            else:
                bot.send_message(call.message.chat.id, f"🤡 {call.from_user.first_name}, вы не можете отменить эту игру, так как вас не вызывали")




@bot.message_handler(commands=['fact'])
def getFact(message):
    Number = "228"
    
    response = requests.get("http://numbersapi.com/228")

    
    text_Eng = response.text
    text_Rus = GoogleTranslator(source='auto', target='ru').translate(text_Eng)
    bot.send_message(message.chat.id, text_Rus)
    
 
@bot.message_handler(commands=['all'])
def getFact(message):
     
    bot.send_message(message.chat.id, "[Артем](tg://user?id=1063677223), [Саша](tg://user?id=1473377894),[Филя](tg://user?id=108150618),[Никита](tg://user?id=917793861),[Паша](tg://user?id=495605727),[Серафим](tg://user?id=1193757607),[Фока](tg://user?id=822344339),[Артем](tg://user?id=1063677223),[Денчик](tg://user?id=680793601) \- Вас вызывают на разговор", parse_mode='MarkdownV2')
       
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
        bot.send_message(message.chat.id, "Неправильный формат сообщения. Используйте /change <name> <value>")
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
  

@bot.message_handler(func=lambda message: True)
def echo_message(message):
    # Проверяем текст сообщения
    print(message.text)
    messageText = message.text.lower().replace("?", "")
    messageText = messageText.replace(".", "")
    messageText = messageText.replace("!", "")
    
    if messageText == "ура":
        bot.reply_to(message, "Ура!")
        
    elif messageText == "да":
        bot.reply_to(message, "Пизда")
    elif messageText == "нет":
        bot.reply_to(message, "Пидора ответ")
        
    elif messageText == "где":
        bot.reply_to(message, "В пизде")
        
    elif messageText == "че":
        bot.reply_to(message, "Хуй через плечо")
        
    elif messageText == "чё":
        bot.reply_to(message, "Хуй через плечо")
    
    elif messageText == "странно":
        bot.reply_to(message, "Очень")
    
    elif messageText == "денчик":
        bot.reply_to(message, "Хуенчик")
    elif messageText == "дэнис":
        bot.reply_to(message, "Пэнис")
    elif messageText == "денис":
        bot.reply_to(message, "Пенис")
    elif messageText == "сашка":
        bot.reply_to(message, "Хуяшка")
    elif messageText == "пашка":
        bot.reply_to(message, "Хуяшка")
    elif messageText == "филя":
        bot.reply_to(message, "Хуиля")
    elif messageText == "никита":
        bot.reply_to(message, "Хуи́та")
    elif messageText == "никитка":
        bot.reply_to(message, "Хуи́тка")
    elif messageText == "артем":
        bot.reply_to(message, "Гандон")
    elif messageText == "артём":
        bot.reply_to(message, "Гандон")
    elif messageText == "пидор":
        bot.reply_to(message, "Асуждаю")
    elif messageText == "фока":
        bot.reply_to(message, "Хуёка")
    elif messageText == "фокинс":
        bot.reply_to(message, "Хуёкинс")
    elif messageText == "данечка":
        bot.reply_to(message, "Хуянечка")
    elif messageText == "павел":
        bot.reply_to(message, "Хуявел")
    elif messageText == "павел":
        bot.reply_to(message, "Хуявел")
    elif messageText == "серафимка":
        bot.reply_to(message, "Хуинка")
    elif messageText == "денчик":
        bot.reply_to(message, "Хуенчик")
    elif messageText == "дэнчик":
        bot.reply_to(message, "Хуенчик")
    elif messageText == "саша":
        bot.reply_to(message, "Хуяша")
    elif messageText == "ортем":
        bot.reply_to(message, "Гандон?")
        
 
@bot.message_handler(func=lambda message: True, content_types=['left_chat_member'])
def handle_left_chat_member(message):
    left_user = message.left_chat_member
    bot.reply_to(message, f"{left_user.first_name} съебал с позором.")
 


						
while True:
    try:
        #bot.send_message("-1002101471139", "#остановитесь")
        bot.polling(none_stop=True)
    except Exception as _ex:
        print(_ex)
        sleep(3)


