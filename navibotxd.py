import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from keyboardsnavi import murkup, murkup_empty
import sqlite3
from confignavi import TOKEN
import random

schet = 0
correct_option_id = 0
balls = 0
bot = Bot(TOKEN)

dp = Dispatcher(bot, storage=MemoryStorage())

logging.basicConfig(level=logging.INFO)


class States(StatesGroup):
    input_id_question = State()


conn = sqlite3.connect('navibot.db')
cur = conn.cursor()
cur.execute("""CREATE TABLE IF NOT EXISTS questions(id INTEGER, question TEXT, answer TEXT);""")
conn.commit()
cur.execute(
    "INSERT INTO questions VALUES ('1', 'В чём разница между списком и кортежом?', 'Разница между списком и кортежем заключается в том, что список объявляется в квадратных скобках и может быть изменен, в то время как кортеж объявляется в скобках и не может быть изменен.')")
conn.commit()
cur.execute(
    "INSERT INTO questions VALUES ('2', 'Как соединить список строк в одну?', 'Чтобы соединить, нужен метод строки .join()')")
conn.commit()
cur.execute(
    "INSERT INTO questions VALUES ('3', 'Можно ли объявлять функцию внутри другой функции? Где она будет видна?', 'Можно. Такая функция будет видна только внутри первой функции.')")
conn.commit()
cur.execute(
    "INSERT INTO questions VALUES ('4', 'Можно ли извлечь элемент генератора по индексу?', 'Нет, будет ошибка. Генератор не поддерживает метод __getitem__.')")
conn.commit()
cur.execute(
    "INSERT INTO questions VALUES ('5', 'Что такое цикл?', 'Цикл – это языковая конструкция, которая может определять участок программы для многократного повторения и количество этих повторений.')")
conn.commit()
cur.execute(
    "INSERT INTO questions VALUES ('6', 'Как итерировать словарь по парам ключ-значение?', 'Метод словаря .iteritems() возвращает генератор кортежей (key, value).')")
conn.commit()
cur.execute(
    "INSERT INTO questions VALUES ('7', 'Как получить список атрибутов объекта?', 'Функция dir возвращает список строк – полей объекта. Поле __dict__ содержит словарь вида {поле -> значение}.')")
conn.commit()
cur.execute(
    "INSERT INTO questions VALUES ('8', 'Каково определение компьютерного программного обеспечения?', 'Програ́ммное обеспе́чение — программа или множество программ, используемых для управления компьютером.')")
conn.commit()
cur.execute(
    "INSERT INTO questions VALUES ('9', 'Что такое модуляризация?', 'модуляризация — Процесс проектирования, основанный на модульном подходе, при котором система разбивается на большое число независимых, но логически взаимо связанных модулей.')")
conn.commit()
cur.execute(
    "INSERT INTO questions VALUES ('10', 'Треды в Питоне — это нативные треды или нет?', 'Да, это нативные Posix-совместимые треды, которые исполняются на уровне операционной системы.')")
conn.commit()


@dp.message_handler(commands="start")
async def start(message: types.Message):
    await message.answer('Привет, меня зовут NAVI BOT.'
                         '\nЯ буду твои верным помошником, могу показать тебе примеры вопросов,'
                         '\n которые могут понадобится на стажировках в какие-нибудь IT-компании.'
                         '\nЧтобы узнать что я умею напиши /help', reply_markup=murkup)


@dp.message_handler(commands="help")
async def help(message: types.Message):
    await message.answer('Я умею: \n''1. /questions - Выдам список вопросов для подготовки к собеседованию \n 2. /help - Расскажу как мной пользоваться ''\n3. /add_question - Если есть вопрос по созданию бота, связь с разработчиком'
'\n4. /quiz - Хочешь проверить свои базовые знания Python, тогда нажми сюда',
                         reply_markup=murkup)


@dp.message_handler(commands="questions")
async def questions(message: types.Message):
    allwrite = ''
    cur.execute("SELECT id from questions")
    resultid = cur.fetchall()
    cur.execute("SELECT question from questions")
    resultquestion = cur.fetchall()
    for write in range(len(resultid)):
        allwrite += str(resultid[write]).strip("( ,)") + ') ' + str(resultquestion[write]).strip("(' ',)") + '\n'
    await message.answer(allwrite, reply_markup=murkup)


@dp.message_handler(content_types=['text'], text='Ввести номер вопроса')
async def input_id_of_question1(message: types.Message):
    allwrite = 'Выберите номер вопроса\n'
    cur.execute("SELECT id from questions")
    resultid = cur.fetchall()
    cur.execute("SELECT question from questions")
    resultquestion = cur.fetchall()
    for write in range(len(resultid)):
        allwrite += str(resultid[write]).strip("( ,)") + ' - ' + str(resultquestion[write]).strip("(' ',)") + '\n'
    await message.answer(allwrite, reply_markup=murkup_empty)
    await States.input_id_question.set()


@dp.message_handler(content_types=['text'], state=States.input_id_question)
async def input_id_of_question2(message: types.Message, state: FSMContext):
    cur.execute(f"SELECT question FROM questions WHERE id = {message.text}")
    result = cur.fetchone()
    if result is None:
        await message.answer('Не нашёл такого вопроса! Введите пожалуйста снова!')
    else:
        cur.execute(f"SELECT answer FROM questions WHERE id = {message.text}")
        resultanswer = cur.fetchone()
        await message.answer(
            'Ваш вопрос:\n' + str(result).strip("(' ',)") + '\nОтвет на вопрос:\n' + str(resultanswer).strip(
                "(' ',)").replace(r'\n', '\n'), reply_markup=murkup)
        await state.finish()


@dp.message_handler(content_types=['text'], text='Рандомный вопрос')
async def random_questions(message: types.Message):
    cur.execute(f"SELECT question FROM questions")
    result = cur.fetchall()
    randomquestion = str(random.choice(result)).strip("(' ,')")
    cur.execute(f"SELECT answer FROM questions WHERE question = '{randomquestion}'")
    resultanswer = cur.fetchone()
    await message.answer('Ваш рандомный вопрос: \n' + randomquestion + '\nОтвет на вопрос:\n' + str(resultanswer).strip(
        "(' ,')").replace(r'\n', '\n'), reply_markup=murkup)


@dp.message_handler(commands="add_question")
async def add_question(message: types.Message):
    await message.answer('Если есть предложения по изменению бота, свяжитесь с его разработчиком.\n@lenshin15',
                         reply_markup=murkup)


@dp.message_handler(commands="quiz")
async def quiz(message: types.Message):
    global correct_option_id
    correct_option_id = 2
    await bot.send_poll(message.from_user.id,
                        '1)Имеется кортеж вида T = (4, 2, 3). Какая из операций приведёт к тому, что имя T будет ссылаться на кортеж (1, 2, 3)? ',
                        ['1) T[0] = 1', '2) T = (1) + T[1:]', '3) T = (1,) + T[1:]'], type='quiz',
                        correct_option_id=correct_option_id, is_anonymous=False)
    global schet
    schet += 1
    global balls
    balls = 0


@dp.poll_answer_handler()
async def some_poll_answer_handler(poll_answer: types.PollAnswer):
    global schet
    global balls
    global correct_option_id
    if int(poll_answer.option_ids[0]) == correct_option_id:
        balls += 1
        await bot.send_message(poll_answer.user.id, f'Вы ответили верно! +1 балл! Всего баллов {balls}')
    else:
        await bot.send_message(poll_answer.user.id, 'К сожалению вы ответили неверно!')
    if schet == 5:
        await bot.send_message(poll_answer.user.id,
                               f'Вы прошли опросы! У вас {balls} баллов! Чтобы снова пройти опросы напишите /quiz')
        schet = 0
    elif schet == 1:
        correct_option_id = 1
        await bot.send_poll(poll_answer.user.id, '2)Для чего в Python используется встроенная функция enumerate()? ',
                            ['а) Для определения количества элементов последовательности. ',
                             'б) Для одновременного итерирования по самим элементам и их индексам. ',
                             'в) Для сортировки элементов по значениям id.'], type='quiz',
                            correct_option_id=correct_option_id, is_anonymous=False)
        schet += 1
    elif schet == 2:
        correct_option_id = 1
        await bot.send_poll(poll_answer.user.id,
                            '3) Необходимо собрать и вывести все уникальные слова из строки рекламного текста. Какой из перечисленных типов данных Python подходит лучше всего? ',
                            ['а) кортеж (tuple)', 'б) множество (set)', 'в) словарь (dict)'], type='quiz',
                            correct_option_id=correct_option_id, is_anonymous=False)
        schet += 1
    elif schet == 3:
        correct_option_id = 1
        await bot.send_poll(poll_answer.user.id,
                            '4) Какой результат выведет следующий код? \ndef f(a, *pargs, **kargs): \n    print(a, pargs, kargs)',
                            ["а) 1, 2, 3, {'x': 4, 'y': 5}", "б) 1 (2, 3) {'x': 4, 'y': 5}", 'в) 1, 2, 3, 4, 5'],
                            type='quiz',
                            correct_option_id=correct_option_id, is_anonymous=False)
        schet += 1
    elif schet == 4:
        correct_option_id = 2
        await bot.send_poll(poll_answer.user.id, '5)Как вывести список методов и атрибутов объекта x?',
                            ['а) help(x)', 'б) info(x)', 'в) dir(x)'], type='quiz',
                            correct_option_id=correct_option_id, is_anonymous=False)
        schet += 1


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
