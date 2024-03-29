# Notes: 
# 1. Use the following username and password to access the admin rights 
# username: admin
# password: password
# 2. Ensure you open the whole folder for this task in VS Code otherwise the 
# program will look in your root directory for the text files.


# This is program helps users to see, track and organize their tasks

#=====importing libraries===========
import os
from datetime import date, datetime

DATETIME_STRING_FORMAT = "%Y-%m-%d"

# Function to read tasks from file and convert to list of dictionaries
def read_tasks():
    if not os.path.exists("tasks.txt"):
        open("tasks.txt", "w").close()
    
    with open("tasks.txt", 'r') as task_file:
        task_data = [line.strip() for line in task_file if line.strip()]

    task_list = []
    for t_str in task_data:
        components = t_str.split(";")
        task = {
            'username': components[0],
            'title': components[1],
            'description': components[2],
            'due_date': datetime.strptime(components[3], DATETIME_STRING_FORMAT),
            'assigned_date': datetime.strptime(components[4], DATETIME_STRING_FORMAT),
            'completed': components[5] == "Yes"
        }
        task_list.append(task)
    return task_list

# Function to read usernames and passwords from file
def read_user_credentials():
    if not os.path.exists("user.txt"):
        with open("user.txt", "w") as file:
            file.write("admin;password\n")

    with open("user.txt", 'r') as file:
        return dict(line.strip().split(';') for line in file if line.strip())

# Function to write updated username-password pairs to file
def write_user_credentials(username_password):
    with open("user.txt", "w") as file:
        for username, password in username_password.items():
            file.write(f"{username};{password}\n")

# Login function
def login(username_password):
    logged_in = False
    while not logged_in:
        print("LOGIN")
        curr_user = input("Username: ")
        curr_pass = input("Password: ")
        if curr_user not in username_password:
            print("User does not exist.")
        elif username_password[curr_user] != curr_pass:
            print("Wrong password.")
        else:
            print("Login Successful!")
            logged_in = True
    return curr_user

# Function to update tasks.txt file with the current state of task_list
def write_tasks(task_list):
    with open("tasks.txt", "w") as file:
        for task in task_list:
            task_line = f"{task['username']};{task['title']};{task['description']};"
            task_line += f"{task['due_date'].strftime(DATETIME_STRING_FORMAT)};"
            task_line += f"{task['assigned_date'].strftime(DATETIME_STRING_FORMAT)};"
            task_line += "Yes" if task['completed'] else "No"
            file.write(task_line + "\n")


def view_and_modify_tasks(curr_user):
    # Filter tasks for the current user
    user_tasks = [task for task in task_list if task['username'] == curr_user]
    
    # Display tasks
    if not user_tasks:
        print("No tasks assigned to you.")
        return

    for i, task in enumerate(user_tasks, start=1):
        disp_str = f"{i}. Task: \t\t {task['title']}\n"
        disp_str += f"   Assigned to: \t {task['username']}\n"
        disp_str += f"   Date Assigned: \t {task['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
        disp_str += f"   Due Date: \t {task['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
        disp_str += f"   Task Description: \n   {task['description']}\n"
        disp_str += f"   Completed: \t {'Yes' if task['completed'] else 'No'}\n"
        print(disp_str)
    
    # Task selection
    task_number = int(input("Enter task number to select a task, or '-1' to return to the main menu: "))
    if task_number == -1:
        return
    selected_task = user_tasks[task_number - 1]

    # Task action
    action = input("Enter 'c' to mark as complete, or 'e' to edit the task: ").lower()
    if action == 'c':
        selected_task['completed'] = True
        print("Task marked as complete.")
    elif action == 'e' and not selected_task['completed']:
        # Edit task
        new_user = input("Enter new username (leave blank to keep current): ").strip()
        if new_user:
            selected_task['username'] = new_user
        new_due_date = input("Enter new due date (YYYY-MM-DD, leave blank to keep current): ").strip()
        if new_due_date:
            selected_task['due_date'] = datetime.strptime(new_due_date, DATETIME_STRING_FORMAT)
        print("Task updated.")
    else:
        print("Cannot edit a completed task.")

    # Write updated tasks back to file
    write_tasks(task_list)


def generate_task_overview(task_list):
    # Calculate the total number of tasks in the task list
    total_tasks = len(task_list)

    # Count the number of tasks that have been completed
    completed_tasks = sum(task['completed'] for task in task_list)

    # Calculate the number of tasks that are uncompleted
    uncompleted_tasks = total_tasks - completed_tasks

    # Count the number of tasks that are overdue and not completed
    overdue_tasks = sum(not task['completed'] and task['due_date'] < datetime.now() for task in task_list)

    # Calculate the percentage of tasks that are incomplete
    percent_incomplete = (uncompleted_tasks / total_tasks * 100) if total_tasks else 0

    # Calculate the percentage of tasks that are overdue
    percent_overdue = (overdue_tasks / total_tasks * 100) if total_tasks else 0

    # Open the task_overview.txt file for writing
    with open("task_overview.txt", "w") as file:
        file.write(f"Total number of tasks: {total_tasks}\n")
        file.write(f"Total number of completed tasks: {completed_tasks}\n")
        file.write(f"Total number of uncompleted tasks: {uncompleted_tasks}\n")
        file.write(f"Total number of tasks that haven’t been completed and are overdue: {overdue_tasks}\n")
        file.write(f"Percentage of tasks that are incomplete: {percent_incomplete:.2f}%\n")
        file.write(f"Percentage of tasks that are overdue: {percent_overdue:.2f}%\n")


    
def generate_user_overview(task_list, username_password):
    # Calculate the total number of users and tasks
    total_users = len(username_password)
    total_tasks = len(task_list)
    # Initialize dictionaries to track user-specific task statistics
    user_task_counts = {user: 0 for user in username_password}
    user_completed_tasks = {user: 0 for user in username_password}
    user_incomplete_tasks = {user: 0 for user in username_password}
    user_overdue_tasks = {user: 0 for user in username_password}

    # Populate the dictionaries with task data
    for task in task_list:
        user_task_counts[task['username']] += 1
        if task['completed']:
            user_completed_tasks[task['username']] += 1
        else:
            user_incomplete_tasks[task['username']] += 1
            if task['due_date'] < datetime.now():
                user_overdue_tasks[task['username']] += 1

    # Write user-specific task statistics to user_overview.txt
    with open("user_overview.txt", "w") as file:
        file.write(f"Total number of users: {total_users}\n")
        file.write(f"Total number of tasks: {total_tasks}\n")
        for user in username_password:
            total = user_task_counts[user]
            completed = user_completed_tasks[user]
            incomplete = user_incomplete_tasks[user]
            overdue = user_overdue_tasks[user]
            file.write(f"\nUser: {user}\n")
            file.write(f"Total tasks assigned: {total}\n")
            file.write(f"Percentage of total tasks assigned: {(total / total_tasks * 100) if total_tasks > 0 else 0:.2f}%\n")
            file.write(f"Tasks completed: {completed} ({(completed / total * 100) if total > 0 else 0:.2f}%)\n")
            file.write(f"Tasks still to complete: {incomplete} ({(incomplete / total * 100) if total > 0 else 0:.2f}%)\n")
            file.write(f"Tasks overdue: {overdue} ({(overdue / total * 100) if total > 0 else 0:.2f}%)\n")



def display_statistics(task_list, username_password):
    # Check if reports exist, generate if not
    if not os.path.exists("task_overview.txt") or not os.path.exists("user_overview.txt"):
        print("Generating reports...")
        generate_task_overview(task_list)
        generate_user_overview(task_list, username_password)

    # Display Task Overview
    print("\nTask Overview:\n")
    with open("task_overview.txt", "r") as file:
        print(file.read())

    # Display User Overview
    print("\nUser Overview:\n")
    with open("user_overview.txt", "r") as file:
        print(file.read())
   

# Main program
task_list = read_tasks()  # Load tasks
username_password = read_user_credentials()  # Load user credentials

logged_in_user = login(username_password)  # Handle login

while True:
    print()
    menu = input('''Select one of the following Options below:
r - Registering a user
a - Adding a task
va - View all tasks
vm - View my task
gr - generate reports
ds - Display statistics
e - Exit
: ''').lower()

    if menu == 'r' and logged_in_user == 'admin':
        # Registering a new user
        new_username = input("New Username: ")
        if new_username in username_password:
            print("Username already exists.")
            continue

        new_password = input("New Password: ")
        confirm_password = input("Confirm Password: ")
        if new_password == confirm_password:
            print("New user added.")
            username_password[new_username] = new_password
            write_user_credentials(username_password)  # Update user.txt
        else:
            print("Passwords do not match.")


    elif menu == 'a':
        '''
        Allow a user to add a new task to task.txt file
            Prompt a user for the following: 
             - A username of the person whom the task is assigned to,
             - A title of a task,
             - A description of the task and 
             - the due date of the task.
        '''
        task_username = input("Name of person assigned to task: ")
        if task_username not in username_password.keys():
            print("User does not exist. Please enter a valid username")
            continue
        task_title = input("Title of Task: ")
        task_description = input("Description of Task: ")
        while True:
            try:
                task_due_date = input("Due date of task (YYYY-MM-DD): ")
                due_date_time = datetime.strptime(task_due_date, DATETIME_STRING_FORMAT)
                break

            except ValueError:
                print("Invalid datetime format. Please use the format specified")


        # Then get the current date.
        curr_date = date.today()
        ''' 
        Add the data to the file task.txt and
        Include 'No' to indicate if the task is complete.
        '''
        new_task = {
            "username": task_username,
            "title": task_title,
            "description": task_description,
            "due_date": due_date_time,
            "assigned_date": curr_date,
            "completed": False
        }

        task_list.append(new_task)
        with open("tasks.txt", "w") as task_file:
            task_list_to_write = []
            for t in task_list:
                str_attrs = [
                    t['username'],
                    t['title'],
                    t['description'],
                    t['due_date'].strftime(DATETIME_STRING_FORMAT),
                    t['assigned_date'].strftime(DATETIME_STRING_FORMAT),
                    "Yes" if t['completed'] else "No"
                ]
                task_list_to_write.append(";".join(str_attrs))
            task_file.write("\n".join(task_list_to_write))
        print("Task successfully added.")


    elif menu == 'va':
        '''
        Allows users to see all the tasks in the program
        '''

        for t in task_list:
            disp_str = f"Task: \t\t {t['title']}\n"
            disp_str += f"Assigned to: \t {t['username']}\n"
            disp_str += f"Date Assigned: \t {t['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
            disp_str += f"Due Date: \t {t['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
            disp_str += f"Task Description: \n {t['description']}\n"
            print(disp_str)
            

    elif menu == 'vm':
        view_and_modify_tasks(logged_in_user)


    elif menu == 'gr' and logged_in_user == 'admin':
        '''
        If the user is an admin they can generate reports with detailed infor
        about tasks and users
        '''
        generate_task_overview(task_list)
        generate_user_overview(task_list, username_password)
        print("Reports generated successfully.")
        print("\nTask Overview Report:\n")
        with open("task_overview.txt", "r") as file:
            print(file.read())
        print("\nUser Overview Report:\n")
        with open("user_overview.txt", "r") as file:
            print(file.read())


    elif menu == 'ds' and logged_in_user == 'admin': 
        '''If the user is an admin they can display statistics about number of users
            and tasks.'''
        display_statistics(task_list, username_password)  


    elif menu == 'e':
        print('Goodbye!!!')
        exit()

    else:
        print("You have made a wrong choice, Please Try again")