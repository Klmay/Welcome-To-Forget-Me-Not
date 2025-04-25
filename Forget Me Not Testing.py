import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import Calendar, DateEntry
from datetime import datetime, timedelta
from PIL import Image, ImageTk

class ForgetMeNotApp:
    def __init__(self, master):
        self.master = master
        self.tasks = []
        self.priority = {
            "Low": 0,
            "Normal": 0,
            "High": 0
        }

        self.master.title("Forget Me Not")
        self.master.geometry("800x600")
        self.master.resizable(True, True)

        # Welcome Frame
        self.welcome_frame = ttk.Frame(self.master, padding="10")

        # Welcome Image
        image = Image.open("Forget-me-not-welcome-image.jpg")
        image = image.resize((100,100))
        self.welcome_image = ImageTk.PhotoImage(image)

        welcome_label = ttk.Label(self.welcome_frame, text="Welcome to Forget Me Not!", font=("Arial", 24), padding=10,
                                  compound="left", image=self.welcome_image)

        welcome_label.pack()

        # Start Button
        self.start_button = ttk.Button(self.master, text="Start", command=self.open_task_manager)

        # Task Manager Window
        self.task_manager = ttk.Frame(root, padding="10")
        self.task_list = ttk.Treeview(self.task_manager, columns=("Task", "Priority", "Due Date"), show='headings')

        # Task Manager Headings
        self.task_list.heading("Task", text="Task")
        self.task_list.heading("Priority", text="Priority")
        self.task_list.heading("Due Date", text="Due Date")

        self.task_list.pack(fill="both", expand=True)

        self.task_window = None

    def add_task(self, task):
        def get_index(p):
            match p:
                case "High":
                    return self.priority["High"]
                case "Normal":
                    return self.priority["Normal"] + self.priority["High"]
                case "Low":
                    return self.priority["Low"] + self.priority["Normal"] + self.priority["High"]


        # task = [name, priority, due date]
        self.task_list.insert("", get_index(task[1]), None, values=[task[0], task[1], task[2]])
        self.priority[task[1]] += 1

        self.tasks.append(task)

    def open_task_manager(self):
        if self.task_window is None or not self.task_window.winfo_exists():
            self.task_window = tk.Toplevel(self.master)
            self.task_window.title("Add Task")
            self.task_window.geometry("400x300")

            # Task Name
            task_name = ttk.Entry(self.task_window, font=("Arial", 12), width=20, justify="center")
            task_name.pack()

            # Priority Options
            priority_var = tk.StringVar(value="Normal")
            priority_options = ["Low", "Normal", "High"]
            for option in priority_options:
                ttk.Radiobutton(self.task_window, text=option, variable=priority_var, value=option).pack()

            # Due Date Input
            due_date = DateEntry(self.task_window, font=("Arial", 12), width=20, justify="center",
                                 date_pattern="mm-dd-yyyy", mindate=datetime.now(), showweeknumbers=False, showmonthdays=False)
            due_date_label = ttk.Label(self.task_window, text="Due Date:")

            # Fix Calendar Month Picker
            due_date._top_cal.wm_overrideredirect(True)

            due_date_label.pack()
            due_date.pack()

            # Add Task Button
            ttk.Button(self.task_window, text="Add Task", command=lambda: self.add_task([task_name.get(), priority_var.get(), due_date.get()])).pack()

            self.task_window.protocol("WM_DELETE_WINDOW", self.close_task_manager)

    def close_task_manager(self):
        # Check if window should really close
        window_should_really_close = True

        if window_should_really_close:
            self.task_window.destroy()
            self.task_window = None

# Create a new Tkinter window
root = tk.Tk()
app = ForgetMeNotApp(root)
app.welcome_frame.pack(fill="x")
app.start_button.pack()
app.task_manager.pack(fill='both', expand=True)
root.mainloop()
