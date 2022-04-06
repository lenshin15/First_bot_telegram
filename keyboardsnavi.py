from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

# Клавиатура
item1 = KeyboardButton('Ввести номер вопроса')
item2 = KeyboardButton('Рандомный вопрос')
murkup = ReplyKeyboardMarkup(resize_keyboard=True)
murkup.add(item1, item2)

# Пустая клавиатура
murkup_empty = ReplyKeyboardRemove()