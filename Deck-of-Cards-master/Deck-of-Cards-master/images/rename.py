import os
import random

# Папка со скриптом
directory = os.path.dirname(os.path.abspath(__file__))

# Определение мастей и значений карт
suits = ["clubs", "spades", "hearts", "diamonds"]
values = ["A", "K", "Q", "J", "10", "9", "8", "7", "6", "5", "4", "3", "2"]

# Создание последовательности карт
cards = []
for value in values:
    for suit in suits:
        cards.append(f"{value}_of_{suit}.png")


# Переименование файлов
for i in range(1, 53):
    old_name = f"{i}.png"
    new_name = cards[i-1]
    old_path = os.path.join(directory, old_name)
    new_path = os.path.join(directory, new_name)
    if os.path.exists(old_path):
        os.rename(old_path, new_path)
        print(f"Renamed {old_name} to {new_name}")
    else:
        print(f"File {old_name} does not exist")

print("Renaming completed.")