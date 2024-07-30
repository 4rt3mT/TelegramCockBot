import telebot
from telebot import types
import random
from PIL import Image
import os
from time import sleep
import threading
from time import sleep



bot = telebot.TeleBot('6473963712:AAEj_wDB1gY2lM3E8vjQslJfuEjJR-0I7pA')
# Структура данных для хранения информации об игроках и их ставках
class Player:
    def __init__(self, user_id, username):
        self.user_id = user_id
        self.username = username
        self.cards = []
        self.messageId = 0
        self.bet = 0
        self.score = 0
        self.stand = False

# Структура данных для хранения информации о лобби и игре
class Game:
    def __init__(self):
        self.players = []
        self.deck = self.create_deck()
        self.dealer_cards = []
        self.dealer_message_id = 0
        self.is_active = False

    def create_deck(self):
        suits = ['hearts', 'diamonds', 'clubs', 'spades']
        ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        deck = [(rank, suit) for suit in suits for rank in ranks]
        random.shuffle(deck)
        return deck

    def deal_card(self):
        return self.deck.pop() if self.deck else None

    def calculate_score(self, cards):
        score = 0
        num_aces = 0
        for rank, _ in cards:
            if rank in 'JQK':
                score += 10
            elif rank == 'A':
                num_aces += 1
                score += 11
            else:
                score += int(rank)
        while score > 21 and num_aces:
            score -= 10
            num_aces -= 1
        return score
        
game = Game()
@bot.message_handler(commands=['start'])
def start_game(message):
    bot.send_message(message.chat.id, "Начинаем игру в 21 очко! Введите вашу ставку.")
    if not game.is_active:
        game.is_active = True
        threading.Timer(5.0, start_blackjack,args=[message]).start()

@bot.message_handler(func=lambda message: message.text.isdigit())
def place_bet(message):
    user_id = message.chat.id
    username = message.from_user.username
    bet = int(message.text)
    player = next((p for p in game.players if p.user_id == user_id), None)
    if player:
        player.bet = bet
    else:
        new_player = Player(user_id, username)
        new_player.bet = bet
        game.players.append(new_player)
    bot.send_message(message.chat.id, f"{username} сделал ставку: {bet}")

def start_blackjack(message):
    bot.send_message(message.chat.id, "Игра началась!")
    deal_initial_cards()
    display_game_state(message)

def deal_initial_cards():
    for player in game.players:
        player.cards = [game.deal_card(), game.deal_card()]
        player.score = game.calculate_score(player.cards)
    game.dealer_cards = [game.deal_card(), game.deal_card()]

def display_game_state(message):
    dealer_image = create_card_image(game.dealer_cards[0], game.dealer_cards[1])
    dealer_message = bot.send_photo(message.chat.id, photo=open(dealer_image, 'rb'), caption="Карты дилера")
    game.dealer_message_id = dealer_message.id
    for player in game.players:
        player_image = create_card_image(*player.cards)
        player.score = game.calculate_score(player.cards)
        markup = create_player_actions(player)
        if player.score == 21:
            message2 = bot.send_photo(message.chat.id, photo=open(player_image, 'rb'), caption=f"{player.username} карты. 21 очко!✅")
            determine_winner(message.chat.id)
        elif game.calculate_score(game.dealer_cards) == 21:
            message2 = bot.send_photo(message.chat.id, photo=open(player_image, 'rb'), caption=f"{player.username} карты. У диллера 21 очко!❌")
            determine_winner(message.chat.id)
        else:
            message2 = bot.send_photo(message.chat.id, photo=open(player_image, 'rb'), caption=f"{player.username} карты", reply_markup=markup)
        player.messageId = message2.id
        
    
def create_card_image(*cards):
    images = [Image.open(f'cards/{rank}_of_{suit}.png') for rank, suit in cards if rank and suit]
    widths, heights = zip(*(i.size for i in images))
    total_width = sum(widths)
    max_height = max(heights)
    combined = Image.new('RGB', (total_width, max_height))
    x_offset = 0
    for im in images:
        combined.paste(im, (x_offset, 0))
        x_offset += im.size[0]
    combined_path = 'cards/combined.png'
    combined.save(combined_path)
    return combined_path

def create_player_actions(player):
    markup = types.InlineKeyboardMarkup()
    hit_button = types.InlineKeyboardButton("Взять карту", callback_data=f"hit_{player.user_id}")
    stand_button = types.InlineKeyboardButton("Остановиться", callback_data=f"stand_{player.user_id}")
    markup.add(hit_button, stand_button)
    return markup

@bot.callback_query_handler(func=lambda call: call.data.startswith('hit_') or call.data.startswith('stand_'))
def handle_action(call):
    user_id = int(call.data.split('_')[1])
    player = next((p for p in game.players if p.user_id == user_id), None)
    if not player:
        return
    if call.data.startswith('hit_'):
        player.cards.append(game.deal_card())
        player_image = create_card_image(*player.cards)
        markup = create_player_actions(player)
        bot.edit_message_media(chat_id=call.message.chat.id, message_id=player.messageId, media=types.InputMediaPhoto(open(player_image, 'rb')))
        bot.edit_message_caption(chat_id=call.message.chat.id, message_id=player.messageId, caption=f"{player.username} карты", reply_markup=markup)

        player.score = game.calculate_score(player.cards)
    elif call.data.startswith('stand_'):
        player.stand = True
        bot.edit_message_caption(chat_id=call.message.chat.id, message_id=player.messageId, caption=f"{player.username} карты. Игрок остановился ✅")

    if player.score > 21:
        bot.edit_message_caption(chat_id=call.message.chat.id, message_id=player.messageId, caption=f"{player.username} карты. Проиграл ❌")

    check_game_status(call.message.chat.id)

def check_game_status(id):
    if all(p.stand or p.score > 21 for p in game.players):
        if all(p.score > 21 for p in game.players):
            determine_winner(id)
        else:
            dealer_play(id)
            determine_winner(id)
        

def dealer_play(id):
    while game.calculate_score(game.dealer_cards) < 17:
        game.dealer_cards.append(game.deal_card())
        dealer_image = create_card_image(*game.dealer_cards)
        bot.edit_message_media(chat_id=id, message_id=game.dealer_message_id, media=types.InputMediaPhoto(open(dealer_image, 'rb')))
        bot.edit_message_caption(chat_id=id, message_id=game.dealer_message_id, caption="Карты дилера")
        sleep(1.5)
def determine_winner(id):
    dealer_score = game.calculate_score(game.dealer_cards)
    for player in game.players:
        if player.score > 21:
            result = "Проиграл"
        elif dealer_score > 21 or player.score > dealer_score:
            result = "Выиграл ✅"
        elif player.score < dealer_score:
            result = "Проиграл"
        else:
            result = "Ничья"
        bot.send_message(id, f"{player.username}, результат: {result}")    
    game.is_active = False
# Запуск бота
bot.polling()
