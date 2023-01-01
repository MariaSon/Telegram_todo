import random


HELP = """
help - напечатать справку по программе.
add - добавить задачу в список (название задачи запрашиваем у пользователя).
show - напечатать все добавленные строки.
exit - выход из программы ToDo.
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
today = []
tomorrow = []
other = []
run = True


def add_todo(date, task):
    if date in tasks:
        if task in tasks[date]:
            return print(f'Задача "{task}" уже в списке для выполнения по сроку {date}.')
        else:
            tasks[date].append(task)
    else:
        tasks[date] = []
        tasks[date].append(task)
    print(f'Задача "{task}" добавлена в список для выполнения '
          f'со сроком {date}!')


while run:
    command = input('Введите команду: ')

    if command == 'help':
        print(HELP)

    elif command == 'show':
        date = input('Введите дату для отображения списка задач: ')
        if date in tasks:
            for task in tasks[date]:
                print(f'  - {task}')
        else:
            print('Такой даты нет')

    elif command == 'add':
        task = input('Введите название задачи: ')
        date = input('Введите дату для выполнения задачи: ')
        add_todo(date, task)

    elif command == 'exit':
        print('Спасибо за использование! До свидания!')
        run = False

    elif command == 'random':
        random_task = random.choice(RANDOM_TASKS)
        add_todo('сегодня', random_task)

    else:
        print('Неизвестная команда')
        run = False

print('До свидания!')

