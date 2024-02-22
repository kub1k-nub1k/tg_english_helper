import telebot
from telebot import types
from key_token import key, dict_url, youglish_url
from audio_send import download_and_send_audio
from discription import get_word_info
from search_verbs import search_in_database

bot = telebot.TeleBot(key)
user_states1 = {}
user_states2 = {}
user_states3 = {}


@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.InlineKeyboardMarkup()
    command1 = types.InlineKeyboardButton("❔Що це за слово❔", callback_data="command1")
    command2 = types.InlineKeyboardButton("👌Irregular Verbs👌", callback_data="command2")
    command3 = types.InlineKeyboardButton("🎬Подивитися як розмовляють🎬", callback_data="command3")
    markup.row(command1)
    markup.row(command2)
    markup.row(command3)
    bot.send_message(message.chat.id, f"Привіт🖐 я бот🤖 що допоможе тобі з Англійською🇬🇧 \nВибирай, що тобі цікаво👇", reply_markup=markup)


@bot.message_handler(commands=['info'])
def send_info(message):
    text = f'Дякую що використовуєте бота🤗\n\nЦей бот створений для особистого користування та не несе комерційної мети.\n\nЯкщо у вас є бажання підтримати розвиток бота - ви можете перейти за посиланням:https://send.monobank.ua/jar/3VEN7VhyNn'
    bot.send_message(message.chat.id, text)


@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    if call.data == "command1":
        handle_command1(call.message)
    elif call.data == "command2":
        handle_command2(call.message)
    elif call.data == "command3":
        handle_command3(call.message)
    elif call.data == "ext":
        send_welcome(call.message)


def handle_command1(message):
    get_user_input1(message, user_states1)


def handle_command2(message):
    get_user_input2(message, user_states2)


def handle_command3(message):
    get_user_input3(message, user_states3)


def get_user_input1(message, user_states):
    bot.send_message(message.chat.id, f"Напиши мені слово, яке тебе цікавить.\nСпробую дізнатися у носіїв, що воно таке👀")
    user_states[message.chat.id] = {"waiting_for_input": True, "prompt": "Введите слово для команды 1"}


def get_user_input2(message, user_states):
    bot.send_message(message.chat.id, f"Виникли труднощі з дієсловами?\nНапиши мені дієслово, яке тебе цікавить📖\nЯ запитаю свого викладача, які там є 3 форми🤓")
    user_states[message.chat.id] = {"waiting_for_input": True, "prompt": "Введите слово для команды 2"}


def get_user_input3(message, user_states):
    bot.send_message(message.chat.id, f"Давай подивимося, як носії використовують складні слова в реальному спілкуванні📽 \nНапиши мені слово і візьми з собою щось перекусити🍿")
    user_states[message.chat.id] = {"waiting_for_input": True, "prompt": "Введите слово для команды 2"}


@bot.message_handler(func=lambda message: True)
def handle_user_text(message):
    chat_id = message.chat.id

    if chat_id in user_states1 and user_states1[chat_id]["waiting_for_input"]:
        user_text = message.text
        prompt = user_states1[chat_id]["prompt"]

        task = dict_url + user_text
        if user_text:
            result = get_word_info(task)
            if result is not None:
                title, transcription, description = result

                answer = f"📖 Слово: {title}\n\n🎤 Транскрипція: ({transcription}) \n\n💭 Опис: {description} \n\nЯк звучить слово 👇"

                bot.send_message(message.chat.id, answer)
                download_and_send_audio(task, message.chat.id)
            else:
                bot.send_message(message.chat.id, f"Якась помилка😔 \nДавай спробуємо ще раз🔀")

            markup = types.InlineKeyboardMarkup()
            repeat_button = types.InlineKeyboardButton("Ще одне слово", callback_data="command1")
            exit_button = types.InlineKeyboardButton(f"↩️Вихід↩️", callback_data="ext")
            markup.row(repeat_button)
            markup.row(exit_button)

            del user_states1[chat_id]

            bot.send_message(chat_id, "Що будемо робити далі?🧐", reply_markup=markup)

    elif chat_id in user_states2 and user_states2[chat_id]["waiting_for_input"]:
        user_text = message.text
        prompt = user_states2[chat_id]["prompt"]
        user_verbs = user_text.lower()
        data_verb = search_in_database(user_verbs)
        if data_verb is not None and len(data_verb) > 0:
            form1 = data_verb[0][1]
            form2 = data_verb[0][2]
            form3 = data_verb[0][3]
            trans = data_verb[0][4]
            verb_text = f"1️⃣Infinitive: {form1}\n\n2️⃣Past Simple: {form2}\n\n3️⃣Past Participle: {form3}\n\n🇺🇦Переклад: {trans}"
            bot.send_message(message.chat.id, verb_text)
        else:
            bot.send_message(message.chat.id, f'Напевно, я не знаю цього слова😔 \nМожливо, тобі варто додати (-"ed") в кінець слова')

        markup = types.InlineKeyboardMarkup()
        repeat_button = types.InlineKeyboardButton("Ще одне слово", callback_data="command2")
        exit_button = types.InlineKeyboardButton(f"↩️Вихід↩️", callback_data="ext")
        markup.row(repeat_button)
        markup.row(exit_button)

        del user_states2[chat_id]

        bot.send_message(chat_id, "Що будемо робити далі?🧐", reply_markup=markup)

    elif chat_id in user_states3 and user_states3[chat_id]["waiting_for_input"]:
        user_text = message.text
        url_text = "-".join(user_text.split())
        url_video = youglish_url+url_text

        markup = types.InlineKeyboardMarkup()
        url_button = types.InlineKeyboardButton(text="▶️Дивитися відео▶️", url=url_video)
        exit_button = types.InlineKeyboardButton(f"↩️Вихід↩️", callback_data="ext")
        markup.row(url_button)
        markup.row(exit_button)

        bot.send_message(message.chat.id, f"Натисни на кнопку, щоб переглянути відео▶️\nПриємного перегляду🤗", reply_markup=markup)


@bot.message_handler(commands=['info'])
def send_info(message):
    text = 'Цей бот створений для особистого користування та не несе комерційної мети. Дякую що використовуєте бота. Відгуки та пропозиції можна надіслати у особистих повідомленнях @артем_pindich'
    bot.send_message(message.chat.id, text)


bot.polling(none_stop=True)
