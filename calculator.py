from tkinter import *
from tkinter import messagebox
import sqlite3 as sql
from tkinter.simpledialog import askstring
from datetime import datetime

# Function to add a task
def add_task():
    task_string = task_field.get()
    due_date = due_date_field.get()
    priority = priority_var.get()

    if len(task_string) == 0 or len(due_date) == 0:
        messagebox.showinfo('Error', 'Task or Due Date is Empty.')
    else:
        task = (task_string, due_date, priority)
        tasks.append(task)
        the_cursor.execute('INSERT INTO tasks (title, due_date, priority) VALUES (?, ?, ?)', task)
        list_update()
        task_field.delete(0, 'end')
        due_date_field.delete(0, 'end')

# Function to update the task listbox
def list_update():
    clear_list()
    for task in tasks:
        task_listbox.insert('end', f"{task[0]} (Due: {task[1]}, Priority: {task[2]})")

# Function to clear the listbox
def clear_list():
    task_listbox.delete(0, 'end')

# Function to delete a selected task
def delete_task():
    try:
        selected_task = task_listbox.get(task_listbox.curselection())
        task_title = selected_task.split(' (Due: ')[0]
        tasks[:] = [task for task in tasks if task[0] != task_title]
        list_update()
        the_cursor.execute('DELETE FROM tasks WHERE title = ?', (task_title,))
    except:
        messagebox.showinfo('Error', 'No Task Selected. Cannot Delete.')

# Function to delete all tasks
def delete_all_tasks():
    message_box = messagebox.askyesno('Delete All', 'Are you sure?')
    if message_box:
        tasks.clear()
        the_cursor.execute('DELETE FROM tasks')
        list_update()

# Function to edit a selected task
def edit_task():
    try:
        selected_task = task_listbox.get(task_listbox.curselection())
        task_title = selected_task.split(' (Due: ')[0]
        
        new_title = askstring("Edit Task", "Enter new task title:", initialvalue=task_title)
        if new_title:
            new_due_date = askstring("Edit Task", "Enter new due date (YYYY-MM-DD):", initialvalue=selected_task.split('Due: ')[1].split(',')[0])
            new_priority = askstring("Edit Task", "Enter new priority (High, Medium, Low):", initialvalue=selected_task.split('Priority: ')[1].split(')')[0])

            tasks[:] = [(new_title, new_due_date, new_priority) if task[0] == task_title else task for task in tasks]
            list_update()
            the_cursor.execute('UPDATE tasks SET title = ?, due_date = ?, priority = ? WHERE title = ?', (new_title, new_due_date, new_priority, task_title))
    except:
        messagebox.showinfo('Error', 'No Task Selected. Cannot Edit.')

# Function to close the application
def close():
    guiWindow.destroy()

# Function to retrieve tasks from the database
def retrieve_database():
    tasks.clear()
    for row in the_cursor.execute('SELECT title, due_date, priority FROM tasks'):
        tasks.append(row)

if __name__ == "__main__":
    # Setting up the GUI window
    guiWindow = Tk()
    guiWindow.title("To-Do List")
    guiWindow.geometry("700x450+550+250")
    guiWindow.resizable(0, 0)
    guiWindow.configure(bg="#B5E5CF")

    # Setting up the database
    the_connection = sql.connect('enhanced_listOfTasks.db')
    the_cursor = the_connection.cursor()
    the_cursor.execute('CREATE TABLE IF NOT EXISTS tasks (title TEXT, due_date TEXT, priority TEXT)')

    tasks = []

    # Creating frames
    functions_frame = Frame(guiWindow, bg="#8EE5EE")
    functions_frame.pack(side="top", expand=True, fill="both")

    # Task input label and field
    task_label = Label(functions_frame, text="TO-DO-LIST\nEnter the Task Title:", font=("arial", "14", "bold"), background="#8EE5EE", foreground="#FF6103")
    task_label.place(x=20, y=30)

    task_field = Entry(functions_frame, font=("Arial", "14"), width=42, foreground="black", background="white")
    task_field.place(x=180, y=30)

    # Due date input label and field
    due_date_label = Label(functions_frame, text="Due Date (YYYY-MM-DD):", font=("arial", "14", "bold"), background="#8EE5EE", foreground="#FF6103")
    due_date_label.place(x=20, y=80)

    due_date_field = Entry(functions_frame, font=("Arial", "14"), width=20, foreground="black", background="white")
    due_date_field.place(x=220, y=80)

    # Priority selection
    priority_var = StringVar(value="Medium")
    priority_label = Label(functions_frame, text="Priority:", font=("arial", "14", "bold"), background="#8EE5EE", foreground="#FF6103")
    priority_label.place(x=450, y=80)

    priority_dropdown = OptionMenu(functions_frame, priority_var, "High", "Medium", "Low")
    priority_dropdown.config(font=("Arial", 14), width=10)
    priority_dropdown.place(x=530, y=76)

    # Buttons
    add_button = Button(functions_frame, text="Add", width=15, bg='#D4AC0D', font=("arial", "14", "bold"), command=add_task)
    del_button = Button(functions_frame, text="Remove", width=15, bg='#D4AC0D', font=("arial", "14", "bold"), command=delete_task)
    edit_button = Button(functions_frame, text="Edit", width=15, bg='#D4AC0D', font=("arial", "14", "bold"), command=edit_task)
    del_all_button = Button(functions_frame, text="Delete All", width=15, font=("arial", "14", "bold"), bg='#D4AC0D', command=delete_all_tasks)
    exit_button = Button(functions_frame, text="Exit / Close", width=52, bg='#D4AC0D', font=("arial", "14", "bold"), command=close)

    add_button.place(x=20, y=130)
    edit_button.place(x=240, y=130)
    del_button.place(x=460, y=130)
    del_all_button.place(x=240, y=330)
    exit_button.place(x=20, y=380)

    # Task listbox
    task_listbox = Listbox(functions_frame, width=90, height=9, font="bold", selectmode='SINGLE', background="WHITE", foreground="BLACK", selectbackground="#FF8C00", selectforeground="BLACK")
    task_listbox.place(x=20, y=190)

    # Retrieve tasks from database and update listbox
    retrieve_database()
    list_update()

    # Main loop to run the application
    guiWindow.mainloop()
    
    # Commit changes to the database and close the cursor
    the_connection.commit()
    the_cursor.close()
