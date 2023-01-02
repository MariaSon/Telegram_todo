import datetime
import telebot
import random

token = open('token.txt', 'r').readline()

bot = telebot.TeleBot(token)

HELP = """
help - напечатать справку по программе.
add - добавить задачу в список (название задачи запрашиваем у пользователя).
show - напечатать все добавленные строки.
random - добавлять случайную задачу на текущую дату.
"""
RANDOM_TASKS = ('Посмотреть новый фильм.',
                'Прогуляться в парке.',
                'Сходить в бассейн.',
                'Прочитать статью.',
                'Выучить 20 слов на англиском.',
                'Помедитировать.',
                'Погадать кроссворд.',
                'Посмотреть несколько вебинаров.',
                'Приготовить тортик.',)
tasks = {}
person_id = ''


def add_todo(date, task):
    if date in tasks:
        if task in tasks[date]:
            return bot.send_message(person_id, f'Задача "{task}" уже в списке для выполнения по сроку {date}.')
        else:
            tasks[date].append(task)
    else:
        tasks[date] = []
        tasks[date].append(task)
    text = f'Задача "{task}" добавлена в список для выполнения со сроком {date}!'
    bot.send_message(person_id, text)


@bot.message_handler(commands=['help'])
def help_tg(message):
    bot.send_message(message.chat.id, HELP)


@bot.message_handler(commands=['add', 'random'])
def add_random_tg(message):
    global person_id
    person_id = message.chat.id
    if '/add' in message.text:
        split_com = message.text.split(maxsplit=2)
        date = split_com[1]
        task = split_com[2]
    elif message.text == '/random':
        task = random.choice(RANDOM_TASKS)
        date = datetime.datetime.now().strftime('%d/%m/%Y').replace('/', '.')
    add_todo(date, task)


@bot.message_handler(commands=['show'])
def show_tg(message):
    try:
        date = message.text.split(maxsplit=1)[1]
    except IndexError:
        return bot.send_message(message.chat.id, 'Для просмотра задач необходимо ввести '
                                                 'команду в формате "/show дд.мм.гггг"')
    if date in tasks:
        text = f'Задачи для выполнения по сроку {date}:' + '\n'
        for task in tasks[date]:
            text = text + ' - ' + task + '\n'
    else:
        text = f'Задачи на дату {date} отсутстуют. Можете отдохнуть!'
    bot.send_message(message.chat.id, text)


bot.polling(none_stop=True)

