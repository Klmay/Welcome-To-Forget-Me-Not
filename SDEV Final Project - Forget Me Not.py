"""
Name: Kylin May
Date Finished: 5/8/2025

App: Forget Me Not

App explanation: A Task Manager that prioritizes tasks in order of "Highest" to "Lowest".
"""


import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import Calendar, DateEntry
from datetime import datetime, timedelta
from PIL import Image, ImageTk

"""
This is everything regarding the main section of the application
"""
class ForgetMeNotApp:
    # Main Functions/Variables
    def __init__(self, master):
        self.master = master
        self.tasks = []
        self.images = []
        self.priority = {
            "Low": 0,
            "Normal": 0,
            "High": 0
        }

        # Main Window
        self.master.title("Forget Me Not")
        self.master.geometry("800x600")
        self.master.resizable(True, True)

        # Welcome Frame
        self.welcome_frame = ttk.Frame(self.master, padding="10")

        welcome_label = ttk.Label(self.welcome_frame, text="Welcome to Forget Me Not!", font=("Arial", 24), padding=10)
        welcome_image = self.create_image_label(self.welcome_frame, "Forget-me-not-welcome-image.jpg", "Welcome Image")
        welcome_image.config(font=("Arial", 20), padding="10")

        welcome_image.pack()
        welcome_label.pack()

        # Start Button
        self.start_button = ttk.Button(self.master, text="Add Task", command=self.open_task_manager)

        # Remove Task Button
        self.remove_button = ttk.Button(self.master, text="Remove Task", command=self.remove_task)

        # Exit Button
        self.exit_button = ttk.Button(self.master, text="Exit", command=self.exit_app)



        """
        After clicking 'Start', the Task Window will open.
        This is everything regarding the Task Window.
        """
        # Task Manager Window
        self.task_manager = ttk.Frame(root, padding="10")
        self.task_list = ttk.Treeview(self.task_manager, columns=("Task", "Priority", "Due Date"), show="headings")

        # Tooltip Label
        self.tooltip = None

        # Task Manager Headings
        self.task_list.heading("Task", text="Task")
        self.task_list.heading("Priority", text="Priority")
        self.task_list.heading("Due Date", text="Due Date")

        self.task_list.pack(fill="both", expand=True)

        self.task_window = None

        self.master.protocol("WM_DELETE_WINDOW", self.exit_app)
        

    def create_image_label(self, window, file_name, alt_text=None):
        label = ttk.Label(window, text=alt_text)

        # Hover over image to show alt text
        def show_tooltip(event):
            tooltip = tk.Toplevel(self.master)
            tooltip.wm_overrideredirect(True)
            tooltip_label = ttk.Label(tooltip, text=alt_text, background="#97c989", relief="solid", borderwidth=1)
            tooltip_label.pack()

            tooltip.geometry(f"+{event.x_root + 10}+{event.y_root + 10}")
            self.tooltip = tooltip

        # Hide alt text
        def hide_tooltip(event):
            if self.tooltip is not None:
                self.tooltip.destroy()

        # Binds for Enter and Leave events for image label
        label.bind("<Enter>", show_tooltip)
        label.bind("<Leave>", hide_tooltip)

        # Try to load image file
        try:
            img = Image.open(file_name).resize((100,100))
            img = ImageTk.PhotoImage(img)
            label.config(image=img)
            self.images.append(img)
        except FileNotFoundError:
            # Show warning if image not found
            messagebox.showwarning("Warning", f"{alt_text}\n Not Found!")
            img = ImageTk.PhotoImage(Image.new("RGBA", (100,100)))         

        return label

    # To Remove A Task
    def remove_task(self):
        self.task_list.delete(*self.task_list.selection())

    # To Close The Application
    def exit_app(self):
        if messagebox.askokcancel("Closing Down?", "Are you sure you're done here?"):
            self.master.destroy()

    # To Add A New Task
    def add_task(self, task):
        def get_index(p):
            match p:
                case "High":
                    return self.priority["High"] # reorders to put designated tasks labeled 'high' at top of list
                case "Normal":
                    return self.priority["Normal"] + self.priority["High"] # reorders to put designated tasks labeled 'normal' in middle of list
                case "Low":
                    return self.priority["Low"] + self.priority["Normal"] + self.priority["High"] # reorders to put designated tasks labeled 'low' at bottom of list

        print(task, self.priority)

        # task = [name, priority, due date]
        self.task_list.insert("", get_index(task[1]), None, values=[task[0], task[1], task[2]])
        self.priority[task[1]] += 1

        print(task, self.priority)

        self.tasks.append(task)

        

    # The Functions within the Task Manager window
    def open_task_manager(self):
        if self.task_window: return self.task_window.focus_set()
                    
                
        self.task_window = tk.Toplevel(self.master)
        self.task_window.title("Add Task")
        self.task_window.geometry("400x300")

        # Task Name
        entry = tk.StringVar()
        task_name = ttk.Entry(self.task_window, textvariable=entry, font=("Arial", 12), width=20, justify="center")
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

        # Check For Errors
        def add_task_error():
            name = task_name.get()
            if name.strip() == "":
                messagebox.showerror("Error", "Task name cannot be blank!")
                self.task_window.focus_set()
            else:
                self.add_task([task_name.get(), priority_var.get(), due_date.get()])

            entry.set("")

        # Add Task Button
        ttk.Button(self.task_window, text="Add Task", command=add_task_error).pack()

        # Add Task Image
        task_label = self.create_image_label(self.task_window, "Forget-Me-Not-Task-Manager-Image.png", "Pencil and Notepad")
        task_label.config(padding=10, font=("Arial", 8))
        task_label.pack()

        self.task_window.protocol("WM_DELETE_WINDOW", self.close_task_manager)

    def close_task_manager(self):
        # Check if window should really close
        window_should_really_close = True

        if messagebox.askokcancel("Quitting", "Are you sure you're done?"):
            self.task_window.destroy()
            self.task_window = None

# Create new window
root = tk.Tk()
app = ForgetMeNotApp(root)
app.welcome_frame.pack(fill="x")
app.start_button.pack()
app.remove_button.pack()
app.exit_button.pack()
app.task_manager.pack(fill='both', expand=True)
root.mainloop()
