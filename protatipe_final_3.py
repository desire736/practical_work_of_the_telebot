import telebot
from token_file import token, admin_chat_id

API_TOKEN = token
bot = telebot.TeleBot(API_TOKEN)

user_survey = {}
user_answers = {}

questions = [
    "Как тебя зовут?",
    "Сколько тебе лет?",
    "Какой твой любимый цвет?"
]


def send_question(message):
    chat_id = message.chat.id
    current_poll = user_survey.get(chat_id)
    current_answers = user_answers.get(chat_id, [])
    question_number = len(current_answers)

    if question_number == len(questions):
        bot.send_message(chat_id, "Спасибо за участие в опросе!")
        send_answers_to_creator(chat_id)
        return

    bot.send_message(chat_id, questions[question_number])
    user_survey[chat_id] = current_poll

def send_answers_to_creator(user_chat_id):
    answers = user_answers.get(user_chat_id)
    if answers:
        message_text = f"Ответы пользователя с chat_id {user_chat_id}: \n"
        for i, answer in enumerate(answers, start=1):
            message_text += f"Вопрос {i}: {answer}\n"
        bot.send_message(admin_chat_id, message_text)

@bot.message_handler(commands=['start'])
def start_survey(message):
    chat_id = message.chat.id

    user_survey[chat_id] = True
    user_answers[chat_id] = []
    send_question(message)



@bot.message_handler(func=lambda message: True)
def handle_message(message):
    chat_id = message.chat.id
    current_poll = user_survey.get(chat_id)

    if current_poll:
        user_answers[chat_id].append(message.text)
        send_question(message)

bot.polling()


