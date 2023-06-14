import telebot
from random import *
from telebot import types
from copy import deepcopy


# создаем объект бота
bot = telebot.TeleBot('token')

# создаем словарь с вопросами и заданиями, разделенными по категориям
questions = {
    'личная жизнь': [
        'Какой самый романтичный подарок, который тебе когда-либо дарили?',
        'Какие безумные поступки совершал?',
        'Какую книгу ты прочитал в последний раз?',
    ],
    'работа': [
        'Какую работу ты мечтаешь получить?',
        'Какую работу ты не любишь делать?',
        'Какой была твоя первая работа?',
    ],
    'друзья': [
        'Кто твой лучший друг?',
        'Какая самая странная привычка у твоего друга?',
        'Как давно ты знаешь своих друзей?',
    ],
}

tasks = {
    'личная жизнь': [
        'Сделай комплимент своему партнеру',
        'Напиши письмо своему бывшему/бывшей',
        'Сходи на первое свидание с человеком, которого выберет твой друг',
    ],
    'работа': [
        'Напиши письмо своему начальнику, в котором попроси повышения',
        'Сходи на интервью на работу, которую ты совсем не хочешь',
        'Попроси у коллеги помощи с трудной задачей',
    ],
    'друзья': [
        'Проведи целый день вместе со своим лучшим другом',
        'Покажи своему другу, как приготовить блюдо, которое ты умеешь готовить лучше всего',
        'Пригласи друга на ужин в ресторан',
    ],
}

temp_questions = deepcopy(questions)
temp_tasks = deepcopy(tasks)


# создаем функцию для отправки вопросов
def send_question(message, category):
    if len(questions[category]) != 0:
        question1 = choice(questions[category])
        questions[category].remove(question1)
        bot.send_message(message.chat.id, question1)
        bot.register_next_step_handler(message, ask_question_category)
    else:
        bot.send_message(message.chat.id, "В этой категории закончились вопросы!")
        bot.register_next_step_handler(message, ask_question_category)


# создаем функцию для отправки заданий
def send_task(message, category):
    if len(tasks[category]) != 0:
        task1 = choice(tasks[category])
        tasks[category].remove(task1)
        bot.send_message(message.chat.id, task1)
        bot.register_next_step_handler(message, ask_task_category)
    else:
        bot.send_message(message.chat.id, "В этой категории закончились вопросы!")
        bot.register_next_step_handler(message, ask_task_category)


# создаем функцию для отправки сообщений с кнопками
def send_message_with_buttons(message, text, buttons):
    markup = types.ReplyKeyboardMarkup(row_width=2)
    for button in buttons:
        markup.add(types.KeyboardButton(button))
    bot.send_message(message.chat.id, text, reply_markup=markup)


# обрабатываем команду /start
@bot.message_handler(commands=['start'])
def start(message):
    text = 'Привет! Я бот для игры "Правда или Действие". Выбери режим игры:'
    buttons = ['Правда', 'Действие']
    send_message_with_buttons(message, text, buttons)


# обрабатываем все команды
@bot.message_handler(content_types=["text"])
def question(message):
    global questions, tasks
    if message.text == "Правда":
        text = 'Выбери категорию вопросов:'
        buttons = list(questions.keys())
        buttons.append("Назад")
        send_message_with_buttons(message, text, buttons)
        bot.register_next_step_handler(message, ask_question_category)
    elif message.text == "Действие":
        text = 'Выбери категорию заданий:'
        buttons = list(tasks.keys())
        buttons.append("Назад")
        send_message_with_buttons(message, text, buttons)
        bot.register_next_step_handler(message, ask_task_category)
    elif message.text == "Сбросить игру":
        questions = deepcopy(temp_questions)
        tasks = deepcopy(temp_tasks)
        bot.send_message(message.chat.id, "Игра успешно сброшена!")
        start(message)
    else:
        bot.send_message(message.chat.id, 'Извините, я не знаю такой команды. Попробуйте еще раз.')
        bot.register_next_step_handler(message, question)


# создаем функцию для сброса игры
@bot.message_handler(content_types=["text"])
def start_menu(message):
    text = 'Правда или действие?'
    buttons = ['Правда', 'Действие', 'Сбросить игру']
    send_message_with_buttons(message, text, buttons)


# обрабатываем выбор категории вопросов
def ask_question_category(message):
    category = message.text
    if category in questions:
        send_question(message, category)
    elif category == "Назад":
        start_menu(message)
    else:
        bot.send_message(message.chat.id, 'Извините, я не знаю такой категории. Попробуйте еще раз.')
        bot.register_next_step_handler(message, ask_question_category)


# обрабатываем выбор категории заданий
def ask_task_category(message):
    category = message.text
    if category in tasks:
        send_task(message, category)
    elif category == "Назад":
        start_menu(message)
    else:
        bot.send_message(message.chat.id, 'Извините, я не знаю такой категории. Попробуйте еще раз.')
        bot.register_next_step_handler(message, ask_task_category)


# запускаем бота
bot.polling(none_stop=True)
