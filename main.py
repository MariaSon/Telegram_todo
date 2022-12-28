HELP = """
help - напечатать справку по программе.
add - добавить задачу в список (название задачи запрашиваем у пользователя).
show - напечатать все добавленные строки.
exit - выход из программы ToDo.
"""
tasks = {}
today = []
tomorrow = []
other = []
run = True

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
        if date in tasks:
            tasks[date].append(task)
        else:
            tasks[date] = []
            tasks[date].append(task)
        print(f'Задача "{task}" добавлена в список для выполнения со сроком {date}!')
    elif command == 'exit':
        print('Спасибо за использование! До свидания!')
        run = False
    else:
        print('Неизвестная команда')
        run = False

print('До свидания!')

