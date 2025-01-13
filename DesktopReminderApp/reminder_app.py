import tkinter as tk
from tkinter import messagebox
from plyer import notification
from datetime import datetime
import time
import threading
import sqlite3

# Function to send reminder notifications
def send_reminder(title, message):
    notification.notify(
        title=title,
        message=message,
        timeout=10  # Notification duration
    )

# Function to check tasks and send reminders
def check_tasks(tasks):
    while tasks:
        now = datetime.now().strftime("%H:%M")
        for task in tasks[:]:  # Iterate through a copy of the list
            if task['time'] == now:
                send_reminder(task['title'], task['message'])
                tasks.remove(task)
        time.sleep(60)  # Check every minute

# GUI for adding tasks
def add_task():
    title = title_entry.get()
    message = message_entry.get()
    time = time_entry.get()
    if title and message and time:
        tasks.append({'title': title, 'message': message, 'time': time})
        messagebox.showinfo("Task Added", f"Task '{title}' has been added.")
    else:
        messagebox.showwarning("Invalid Input", "Please fill in all fields.")

# Set up Tkinter window
app = tk.Tk()
app.title("Desktop Reminder App")

# Input fields and button
tk.Label(app, text="Task Title").grid(row=0, column=0)
title_entry = tk.Entry(app)
title_entry.grid(row=0, column=1)

tk.Label(app, text="Task Message").grid(row=1, column=0)
message_entry = tk.Entry(app)
message_entry.grid(row=1, column=1)

tk.Label(app, text="Time (HH:MM)").grid(row=2, column=0)
time_entry = tk.Entry(app)
time_entry.grid(row=2, column=1)

tk.Button(app, text="Add Task", command=add_task).grid(row=3, columnspan=2)

# Load tasks from database if SQLite is used
tasks = []

# Optional: Load tasks from SQLite database
def load_tasks_from_db():
    conn = sqlite3.connect('database/tasks.db')
    cursor = conn.cursor()
    cursor.execute("SELECT title, message, time FROM tasks")
    tasks.extend(cursor.fetchall())
    conn.close()

# Optional: Create SQLite database and table
def create_db():
    conn = sqlite3.connect('database/tasks.db')
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        message TEXT,
        time TEXT
    )
    ''')
    conn.commit()
    conn.close()

# Start the database and task checker
create_db()
load_tasks_from_db()

# Start the task checking in a separate thread
def start_checking():
    check_tasks(tasks)

# Start the background task checker
threading.Thread(target=start_checking, daemon=True).start()

# Start the Tkinter main loop
app.mainloop()
