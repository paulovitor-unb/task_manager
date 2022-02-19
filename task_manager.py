import csv
from datetime import datetime

def main():
    # File .csv to save list of tasks
    file_name = 'tarefas.csv'
    # Data for each task (keys for the tasks list of dictionaries)
    task_info = ['name', 'status', 'due_date']

    # Function to import tasks saved previously on the .csv file (if any) into a list od dictionaries
    tasks = read_csv_file(file_name)
        
    # Shows options and keep script running (update tasks) until option 0 -> save and exit
    while True:
        option = show_menu()
        print()
        if option == 0:
            break
        elif option == 1:
            show_tasks(tasks)
        elif option == 2:
            show_to_do(tasks)
        elif option == 3:
            show_done(tasks)
        elif option == 4:
            tasks.append(add_task(task_info))
        elif option == 5:
            tasks = do_task(tasks)
        elif option == 6:
            tasks = delete_tasks(tasks)
        print()

    # End of script (saves the tasks dictionary into the .csv file)
    save_csv_file(file_name, task_info, tasks)
    print('End!')

    
def read_csv_file(file_name):
    tasks = []
    # Tries to read .csv file
    try:
        file = open(file_name)
    # File doesn´t exist -> task list is empty
    except FileNotFoundError:
        pass
    # File exists -> load tasks from .csv file to list of tasks
    else:
        with file as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                tasks.append(row)
        file.close()
    return tasks


def show_menu():
    options = list(range(7))
    print('Type 1 to see all tasks')
    print('Type 2 to see tasks to do')
    print('Type 3 to see tasks done')
    print('Type 4 to add new task')
    print('Type 5 to do a task')
    print('Type 6 to delete tasks')
    print('Type 0 to save tasks and exit')
    # Keeps prompting user until option is in valid range (integer from 0 to 6)
    while True:
        try:
            option = int(input('Option: '))
        except ValueError:
            print('\nInvalid option!')
        else:
            if option in options:
                return option
            else:
                print('\nInvalid option!')


def show_tasks(tasks):
    print('List of tasks:')
    for task in tasks:
        print('Name: ' + task['name'] + ' | Status: ' + task['status'] + ' | Due date: ' + task['due_date'])

def show_to_do(tasks):
    print('List of tasks to do:')
    for task in tasks:
        if task['status'] == 'To do':
            print('Name: ' + task['name'] + ' | Due date: ' + task['due_date'])


def show_done(tasks):
    print('List of tasks done:')
    for task in tasks:
        if task['status'] == 'Done':
            print('Name: ' + task['name'] + ' | Due date: ' + task['due_date'])


def add_task(task_info):
    print('Add new task')
    # Creates dictionary for new task
    task = dict.fromkeys(task_info, '')
    task['status'] = 'To do'
    # string.strip() function used to get rid of leadind and trailing whitespaces
    task['name'] = input('Name of new task: ').strip()
    while task['name'] == "":
        print('\nName cannot be empty!')
        task['name'] = input('Name of new task: ').strip()
    due = input('Due date (in DD-MM-YYYY format): ').strip()
    # Keeps prompting user until date is empty or valid
    while True:
        try:
            task['due_date'] = datetime.strptime(due, "%d-%m-%Y").date()
        except ValueError:
            if due == "":
                task['due_date'] = ""
                break
            else:
                print('\nDue date must be in DD-MM-YYYY format!')
                due = input('Due date: ').strip()
        else:
            if task['due_date'] < datetime.today().date():
                print('\nDue date must today or later!')
                due = input('Due date (in DD-MM-YYYY format): ').strip()
            else:
                task['due_date'] = task['due_date'].strftime('%d/%m/%Y')
                break
    return task


def do_task(tasks):
    names = input('Type the name of tasks to do (separated by comma): ').strip()
    # Gets list with names of tasks (separating by comma)
    names = list(names.split(','))
    # Removes leadind and trailing whitespaces and uppercases names (standard for comparison)
    for i in range(len(names)):
        names[i] = names[i].strip().upper()
    for task in tasks:
        #  Comparison is case insensitive (design choice)
        if task['name'].upper() in names:
            task['status'] = 'Done'
    return tasks


def delete_tasks(tasks):
    names = input('Type the name of tasks to delete (separated by comma): ').strip()
    names = list(names.split(','))
    for i in range(len(names)):
        names[i] = names[i].strip().upper()
    for task in tasks:
        if task['name'].upper() in names:
            tasks.remove(task)
    return tasks


def save_csv_file(file_name, task_info, tasks):
    file = open(file_name, 'w', newline='')
    with file as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=task_info)
        writer.writeheader()
        for task in tasks:
            writer.writerow(task)
    file.close()


main()