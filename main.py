import logging
import random

import telebot
from telebot import types

import bot_tools.qr_code_recognition
from questions import text_question_data_1, text_question_data_2, qr_question_data_1, qr_question_data_2, \
    statistic_question_data_1, choose_question_data_1, choose_question_data_2, choose_question_data_3, \
    choose_question_data_4, choose_question_data_5, statistic_question_data_2, choose_question_data_6, \
    choose_question_data_7, text_question_data_3

bot = telebot.TeleBot('5982836012:AAF_2PY0Ys-EGpJ5eCEGZWunnQpltJqhoHk')

logger = logging.getLogger(__name__)
current_quiz = {}
all_answers = {}  # для выбора вариантов ответа
user_answers = {}  # для выбора вариантов ответа
chosen_answers = {}  # для выбора вариантов ответа
chosen_answers_stat = {}
all_questions = [choose_question_data_1, qr_question_data_1, text_question_data_1, choose_question_data_2,
                 statistic_question_data_1, choose_question_data_3, qr_question_data_2, choose_question_data_4,
                 choose_question_data_5, statistic_question_data_2, text_question_data_2, choose_question_data_6,
                 choose_question_data_7, text_question_data_3]
user_data = {}
current_quiz_number = {}  #
total_points = {}  #


@bot.message_handler(commands=['start'])
def start(message):
    current_quiz_number[message.from_user.id] = 0
    total_points[message.from_user.id] = 0
    user_data[message.from_user.id] = {}
    bot.send_message(message.chat.id,
                     text="Как можно к тебе обращаться?")
    bot.register_next_step_handler(message, name_answer)


def name_answer(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Начать квиз")
    btn2 = types.KeyboardButton("О боте")
    markup.add(btn1, btn2)
    if message.from_user.id is not None:
        bot.send_message(message.chat.id, text="Привет, {}, рад знакомству! Добро пожаловать в библиотеку на "
                                               "Покровском бульваре! Ты в игре, то есть на библиотечном квизе. Не "
                                               "забудь оставить верхнюю одежду в гардеробе! С собой можно захватить "
                                               "бутылку воды или термос с кофе, а вот еду лучше не надо. Если по ходу "
                                               "игры у тебя будут возникать вопросы - обращайся к библиотекарям, "
                                               "они всегда готовы помочь!".format(message.text), reply_markup=markup)
        user_data[message.from_user.id]["name"] = message.text
    else:
        bot.send_message(message.chat.id, text="Ваш аккаунт непубличен! Чтобы сохранить ваши результаты нам нужен ваш "
                                               "Username в Телеграме. Создать Username можно в настройках Телеграма. "
                                               "Затем просто перейдите в бота и нажмите: /start!")


def cleaner(message):
    current_quiz_number[message.from_user.id] = 0
    total_points[message.from_user.id] = 0
    all_answers[message.from_user.id] = None
    user_answers.clear()
    chosen_answers[message.from_user.id] = None


@bot.message_handler(
    func=lambda message: message.text in ["О боте", "Главное меню", "Квиз", "Начать квиз", "Следующий вопрос",
                                          "Пройти заново"])
def func(message):
    if message.text == "О боте":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Главное меню")
        markup.add(btn1)
        bot.send_message(message.chat.id, text="Бла-бла-бла", reply_markup=markup)
    elif message.text == "Главное меню":
        cleaner(message)
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Начать квиз")
        btn2 = types.KeyboardButton("О боте")
        markup.add(btn1, btn2)
        bot.send_message(message.chat.id,
                         text="Привет, {}, рад знакомству! Добро пожаловать в библиотеку на "
                              "Покровском бульваре! Ты в игре, то есть на библиотечном квизе. Не "
                              "забудь оставить верхнюю одежду в гардеробе! С собой можно захватить "
                              "бутылку воды или термос с кофе, а вот еду лучше не надо. Если по ходу "
                              "игры у тебя будут возникать вопросы - обращайся к библиотекарям, "
                              "они всегда готовы помочь!".format(
                             user_data[message.from_user.id]["name"]), reply_markup=markup)
    elif message.text == "Начать квиз" or message.text == "Следующий вопрос":
        quiz_transition(message)
    elif message.text == "Пройти заново":
        cleaner(message)
        quiz_transition(message)


def quiz_transition(message):
    if len(all_questions) <= current_quiz_number[message.from_user.id]:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Пройти заново")
        btn2 = types.KeyboardButton("Главное меню")
        markup.add(btn1, btn2)
        bot.send_message(message.chat.id,
                         text="Поздравляем тебя с прохождением квиза!".format(
                             message.from_user), reply_markup=types.ReplyKeyboardRemove())
        bot.send_message(message.chat.id,
                         text=f'Всего у тебя: {total_points[message.from_user.id]} баллов!'.format(
                             message.from_user), reply_markup=markup)
    else:
        current_quiz[message.from_user.id] = all_questions[current_quiz_number[message.from_user.id]]
        if current_quiz[message.from_user.id]["quiz_type"] == "text":
            text_question(message, current_quiz[message.from_user.id])
        elif current_quiz[message.from_user.id]["quiz_type"] == "qr":
            qr_question(message, current_quiz[message.from_user.id])
        elif current_quiz[message.from_user.id]["quiz_type"] == "choose":
            choose_question(message)
        elif current_quiz[message.from_user.id]["quiz_type"] == "statistic":
            statistic_question(message)
        current_quiz_number[message.from_user.id] += 1


def text_question(message, data):
    total_points[message.from_user.id] += int(data["points"])
    msg = bot.send_message(message.chat.id, text=data["question"].format(
        message.from_user), reply_markup=types.ReplyKeyboardRemove())
    bot.register_next_step_handler(msg, text_answer)


def text_answer(message):
    if message.text in current_quiz[message.from_user.id]["right_answers"] or len(
            current_quiz[message.from_user.id]["right_answers"]) == 0:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Следующий вопрос")
        markup.add(btn1)
        bot.send_message(message.chat.id, text=str(current_quiz[message.from_user.id]["right_answer_reply"]).format(
            message.from_user), reply_markup=markup)
    else:
        msg = bot.send_message(message.chat.id,
                               text=str(current_quiz[message.from_user.id]["wrong_answer_reply"]).format(
                                   message.from_user))
        bot.register_next_step_handler(msg, text_answer)


def qr_question(message, data):
    total_points[message.from_user.id] += int(data["points"])
    msg = bot.send_message(message.chat.id, text=data["question"].format(
        message.from_user), reply_markup=types.ReplyKeyboardRemove())
    bot.register_next_step_handler(msg, qr_answer)


def qr_answer(message):
    if bot_tools.qr_code_recognition.photo(bot, message) == current_quiz[message.from_user.id]["qr_text"]:
        total_points[message.from_user.id] += int(current_quiz[message.from_user.id]["points"])
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Следующий вопрос")
        markup.add(btn1)
        bot.send_message(message.chat.id, text=str(current_quiz[message.from_user.id]["right_answer_reply"]).format(
            message.from_user), reply_markup=markup)
    else:
        msg = bot.send_message(message.chat.id,
                               text=str(current_quiz[message.from_user.id]["wrong_answer_reply"]).format(
                                   message.from_user))
        bot.register_next_step_handler(msg, qr_answer)


def statistic_question(message):
    total_points[message.from_user.id] += int(current_quiz[message.from_user.id]["points"])
    all_answers[message.from_user.id] = current_quiz[message.from_user.id]["answers"]
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn = types.KeyboardButton("Далее")
    markup.add(btn)
    msg = bot.send_poll(message.chat.id, current_quiz[message.from_user.id]["question"],
                        all_answers[message.from_user.id],
                        allows_multiple_answers=True,
                        is_anonymous=False, reply_markup=markup)
    user_data[message.from_user.id]["poll"] = msg.poll.id
    bot.register_next_step_handler(msg, statistic_answer)


def statistic_answer(message):
    chosen_answers_stat[message.from_user.id] = []
    if user_data[message.from_user.id]["poll"] in user_answers.keys():
        for i in user_answers[user_data[message.from_user.id]["poll"]]:
            chosen_answers_stat[message.from_user.id].append(all_answers[message.from_user.id][int(i)])
        total_points[message.from_user.id] += int(current_quiz[message.from_user.id]["points"])
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Следующий вопрос")
        markup.add(btn1)
        bot.send_message(message.chat.id, text=str(current_quiz[message.from_user.id]["answer_reply"]).format(
            message.from_user), reply_markup=markup)
    else:
        bot.send_message(message.chat.id,
                         text='Опрос не пройден',
                         reply_markup=types.ReplyKeyboardRemove())
        statistic_question(message)


@bot.poll_answer_handler()
def handle_poll_answer(answer):
    user_answers.clear()
    user_answers[answer.poll_id] = answer.option_ids


def choose_question(message):
    all_answers[message.from_user.id] = (
            current_quiz[message.from_user.id]["right_answers"] + current_quiz[message.from_user.id][
        "wrong_answers"])
    random.shuffle(all_answers[message.from_user.id])
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn = types.KeyboardButton("Далее")
    markup.add(btn)
    msg = bot.send_poll(message.chat.id, current_quiz[message.from_user.id]["question"],
                        all_answers[message.from_user.id],
                        allows_multiple_answers=True,
                        is_anonymous=False, reply_markup=markup)
    user_data[message.from_user.id]["poll"] = msg.poll.id
    bot.register_next_step_handler(msg, choose_answer)


def choose_answer(message):
    chosen_answers[message.from_user.id] = []
    if user_data[message.from_user.id]["poll"] in user_answers.keys():
        for i in user_answers[user_data[message.from_user.id]["poll"]]:
            chosen_answers[message.from_user.id].append(all_answers[message.from_user.id][int(i)])
        if sorted(chosen_answers[message.from_user.id]) == sorted(current_quiz[message.from_user.id]["right_answers"]):
            total_points[message.from_user.id] += int(current_quiz[message.from_user.id]["points"])
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = types.KeyboardButton("Следующий вопрос")
            markup.add(btn1)
            bot.send_message(message.chat.id, text=str(current_quiz[message.from_user.id]["right_answer_reply"]).format(
                message.from_user), reply_markup=markup)
        else:
            bot.send_message(message.chat.id,
                             text=str(current_quiz[message.from_user.id]["wrong_answer_reply"]).format(
                                 message.from_user),
                             reply_markup=types.ReplyKeyboardRemove())
            choose_question(message)
    else:
        bot.send_message(message.chat.id,
                         text=str(current_quiz[message.from_user.id]["wrong_answer_reply"]).format(
                             message.from_user),
                         reply_markup=types.ReplyKeyboardRemove())
        choose_question(message)


bot.polling(none_stop=True)
