# Task Manager

## Description
The Task Manager is a Python-based command-line application designed to help users manage their daily tasks efficiently. It allows users to view, track, and organize tasks with features such as adding new tasks, viewing all tasks, viewing their tasks, marking tasks as complete, and editing tasks. Additionally, it provides functionality for admin users to generate detailed reports on tasks and user statistics. This project emphasizes file handling, date manipulation, and basic user authentication in Python.

## Table of Contents
- [Installation](#installation)
- [Usage](#usage)
- [Generating Reports](#generating-reports)
- [Credits](#credits)

## Installation
To run the Task Manager, you will need Python installed on your system. Python 3.6 or higher is recommended.

1. **Clone the Repository:**
git clone https://github.com/<yourusername>/finalCapstone.git

Replace `<yourusername>` with your actual GitHub username.

2. **Navigate to the Project Directory:**
cd finalCapstone

3. **Install Required Libraries:**
The Task Manager uses the built-in libraries `os` and `datetime`, so no additional installations are required.

## Usage
To start the Task Manager, run the following command in your terminal:

Upon launching, the application will prompt you to log in. Use the following default admin credentials for the first login:

- **Username:** admin
- **Password:** password

After logging in, follow the on-screen prompts to interact with the application. Here are some of the actions you can perform:

- **r** - Register a new user (admin only)
- **a** - Add a new task
- **va** - View all tasks
- **vm** - View tasks assigned to you
- **gr** - Generate reports (admin only)
- **ds** - Display statistics (admin only)
- **e** - Exit the application

## Generating Reports
Admin users can generate reports on task and user statistics by selecting the "gr" option. Reports generated will be saved to `task_overview.txt` and `user_overview.txt` files.

## Credits
The Task Manager was developed as part of a capstone project to demonstrate practical skills in Python, specifically in file handling, date manipulation, and implementing basic authentication and authorization.

- **Developer:** Carlos Coelho
- **GitHub Profile:** https://github.com/coelhoo7
