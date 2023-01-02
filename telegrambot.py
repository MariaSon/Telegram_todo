import datetime
import time
import telebot
import random

HELP = """
/help - вывод справки по работе бота.
/add - добавление задачи в список на определенную дату. 
    Заполняется в формате "/add дд.мм.гггг Задача".
/show - вывод списка задачи на определенную дату. 
    Заполняется в формате "/show дд.мм.гггг".
/random - добавляет случайную задачу на текущую дату.
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

token = open('token.txt', 'r').readline()

bot = telebot.TeleBot(token)


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


def global_person_id(chat_id):
    global person_id
    person_id = chat_id


def try_valid_date(date):
    try:
        time.strptime(date, '%d.%m.%Y')
        today = datetime.datetime.now().strftime('%d.%m.%Y')
        if date < today:
            return bot.send_message(person_id,
                                    f'Ошибка! Указанная Вами дата "{date}" меньше текущей "{today}"!')
    except ValueError:
        return bot.send_message(person_id,
                                f'Дата {date} не существует, либо указан некорректный формат'), False


@bot.message_handler(commands=['help'])
def help_tg(message):
    global_person_id(message.chat.id)
    bot.send_message(person_id, HELP)


@bot.message_handler(commands=['add', 'random'])
def add_random_tg(message):
    global_person_id(message.chat.id)
    if '/add' in message.text:
        split_com = message.text.split(maxsplit=2)
        try:
            split_com[1]
        except IndexError:
            return bot.send_message(person_id,
                                    f'Ошибка! Указан неверный формат для добавления задачи в список!'
                                    f'Заполняется в формате "/add дд.мм.гггг Задача".')
        date = split_com[1]
        if try_valid_date(date):
            return bot.send_message(person_id,
                                    f'Попробуйте еще раз!')

        task = split_com[2]
    elif message.text == '/random':
        task = random.choice(RANDOM_TASKS)
        date = datetime.datetime.now().strftime('%d.%m.%Y')
    add_todo(date, task)


@bot.message_handler(commands=['show'])
def show_tg(message):
    global_person_id(message.chat.id)
    try:
        message.text.split(maxsplit=1)[1]
    except IndexError:
        return bot.send_message(person_id,
                                f'Ошибка! Указан неверный формат для вывода списка задач!'
                                f'Заполняется в формате "/show дд.мм.гггг".')
    date = message.text.split(maxsplit=1)[1]
    if try_valid_date(date):
        return bot.send_message(person_id,
                                f'Попробуйте еще раз!')
    if date in tasks:
        text = f'Задачи для выполнения по сроку {date}:' + '\n'
        for task in tasks[date]:
            text = text + ' - ' + task + '\n'
    else:
        text = f'Задачи на дату {date} отсутстуют. Можете отдохнуть!'
    bot.send_message(person_id, text)


@bot.message_handler(content_types=['text'])
def incorrect_command(message):
    help_tg(message)


bot.polling(none_stop=True)
