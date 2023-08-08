from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import sqlite3

class ToDoListApp:
    def __init__(self, root):
        self.root = root
        self.root.title('To-Do List')
        self.root.geometry('1310x515+0+0')
        self.root.resizable(False, False)
        self.root.configure(bg='#2c3e50')

        self.name = StringVar()
        self.Task = StringVar()
        self.Priority = StringVar()
        self.Date = StringVar()

        self.create_database()
        self.create_widgets()

    def create_database(self):
        self.con = sqlite3.connect('tasks.db')
        self.cour = self.con.cursor()
        self.cour.execute('''
            CREATE TABLE IF NOT EXISTS TASKS(
                id INTEGER PRIMARY KEY,
                name TEXT,
                priority TEXT,
                date TEXT,
                task TEXT
            ) 
        ''')
        self.con.commit()

    def insert(self):
        if self.name.get() == "" or self.Task.get() == "" or self.Priority.get() == "" or self.Date.get() == "":
            messagebox.showerror("Error", "Please fill all the Entry")
            return

        self.cour.execute("INSERT INTO TASKS (name, priority, date, task) VALUES (?,?,?,?)",
                          (self.name.get(), self.Priority.get(), self.Date.get(), self.Task.get())
                          )
        self.con.commit()
        messagebox.showinfo("Success", "Added New Task")
        self.clear_entries()
        self.display_all_tasks()

    def fetch(self):
        self.cour.execute("SELECT * FROM TASKS")
        rows = self.cour.fetchall()
        return rows

    def remove(self):
        selected_row = self.tree.focus()
        if not selected_row:
            messagebox.showerror("Error", "Please select a task to remove.")
            return

        data = self.tree.item(selected_row)
        row = data["values"]

        self.cour.execute("DELETE FROM TASKS WHERE id=?", (row[0],))
        self.con.commit()
        self.display_all_tasks()

    def update_task(self):
        selected_row = self.tree.focus()
        if not selected_row:
            messagebox.showerror("Error", "Please select a task to update.")
            return

        data = self.tree.item(selected_row)
        row = data["values"]

        if self.name.get() == "" or self.Task.get() == "" or self.Priority.get() == "" or self.Date.get() == "":
            messagebox.showerror("Error", "Please fill all the Entry")
            return

        self.cour.execute("UPDATE TASKS SET name=?, priority=?, date=?, task=? WHERE id=?",
                          (self.name.get(), self.Priority.get(), self.Date.get(), self.Task.get(), row[0]))
        self.con.commit()
        messagebox.showinfo("Success", "The Task data is updated")
        self.clear_entries()
        self.display_all_tasks()

    def display_all_tasks(self):
        self.tree.delete(*self.tree.get_children())
        for row in self.fetch():
            self.tree.insert("", END, values=row)

    def clear_entries(self):
        self.name.set("")
        self.Task.set("")
        self.Priority.set("")
        self.Date.set("")

    def create_widgets(self):
        entries_frame = Frame(self.root, bg='#2c3e50')
        entries_frame.place(x=1, y=1, width=360, height=510)
        title = Label(entries_frame, text='To-Do List App',bg='#2c3e50',fg='#48CCCD', font=('Andalus', 18, 'bold'))
        title.place(x=10, y=1)

        lb1Name = Label(entries_frame, text='Name', font=('Century', 16), bg='#2c3e50', fg='white')
        lb1Name.place(x=10, y=50)
        txtName = Entry(entries_frame, textvariable=self.name, width=19, font=('Century', 16))
        txtName.place(x=130, y=50)

        lb1Task = Label(entries_frame, text='Task', font=('Century', 16), bg='#2c3e50', fg='white')
        lb1Task.place(x=10, y=90)
        txtTask = Entry(entries_frame, textvariable=self.Task, width=19, font=('Century', 16))
        txtTask.place(x=130, y=90)

        lb1priority = Label(entries_frame, text='Priority', font=('Century', 16), bg='#2c3e50', fg='white')
        lb1priority.place(x=10, y=130)
        combopriority = ttk.Combobox(entries_frame, textvariable=self.Priority, state='readonly', width=17, font=('Century', 16))
        combopriority['values'] = ("Low", "Medium", "High")
        combopriority.place(x=130, y=130)

        lb1date = Label(entries_frame, text='Date', font=('Century', 16), bg='#2c3e50', fg='white')
        lb1date.place(x=10, y=170)
        txtdate = Entry(entries_frame, textvariable=self.Date, width=19, font=('Century', 16))
        txtdate.place(x=130, y=170)

        def hide():
            root.geometry('360x515+0+0')

        def show():
            root.geometry('1310x515+0+0')

        btnhide = Button(entries_frame, text='HIDE', cursor='hand2', command=hide, bg='#ADDFFF')
        btnhide.place(x=270, y=10)

        btnshow = Button(entries_frame, text='SHOW', cursor='hand2', command=show, bg='#ADDFFF')
        btnshow.place(x=310, y=10)


        btn_frame = Frame(entries_frame, bg='white', bd=1, relief=SOLID)
        btn_frame.place(x=10, y=400, width=350, height=100)
        btnAdd = Button(btn_frame,
                        text='Add Task',
                        width=14,
                        height=1,
                        font=('Perpetua', 16),
                        fg='white',
                        bg='#3B9C9C',
                        bd=0,
                        command=self.insert
                        )
        btnAdd.place(x=4, y=5)

        btnRemove = Button(btn_frame,
                           text='Remove Task',
                           width=14,
                           height=1,
                           font=('Perpetua', 16),
                           fg='white',
                           bg='#46C7C7',
                           bd=0,
                           command=self.remove
                           )
        btnRemove.place(x=182, y=5)

        btnUpdate = Button(btn_frame,
                           text='Edit Task',
                           width=14,
                           height=1,
                           font=('Perpetua', 16),
                           fg='white',
                           bg='#46C7C7',
                           bd=0,
                           command=self.update_task
                           )
        btnUpdate.place(x=4, y=51)

        btnClear = Button(btn_frame,
                          text='Clear Entries',
                          width=14,
                          height=1,
                          font=('Perpetua', 16),
                          fg='white',
                          bg='#3B9C9C',
                          bd=0,
                          command=self.clear_entries
                          )
        btnClear.place(x=182, y=51)

        tree_frame = Frame(self.root, bg='white')
        tree_frame.place(x=365, y=1, width=940, height=510)
        style = ttk.Style()
        style.configure("mystyle.Treeview", font=('calibri', 12), rowheight=50)
        style.configure("mystyle.Treeview.Heading", font=('calibri', 12))
        self.tree = ttk.Treeview(tree_frame, columns=(1, 2, 3, 4, 5), style="mystyle.Treeview")

        self.tree.heading("1", text="ID")
        self.tree.column("1", width=90)
        self.tree.heading("2", text="Name")
        self.tree.column("2", width=120)
        self.tree.heading("3", text="Priority")
        self.tree.column("3", width=120)
        self.tree.heading("4", text="Date")
        self.tree.column("4", width=160)
        self.tree.heading("5", text="Tasks")
        self.tree.column("5", width=450)

        self.tree['show'] = 'headings'

        self.tree.bind("<ButtonRelease-1>", self.get_data)
        self.tree.pack()

        self.display_all_tasks()

    def get_data(self, event):
        selected_row = self.tree.focus()
        data = self.tree.item(selected_row)
        row = data["values"]
        self.name.set(row[1])
        self.Priority.set(row[2])
        self.Date.set(row[3])
        self.Task.set(row[4])

if __name__ == "__main__":
    root = Tk()
    todo_app = ToDoListApp(root)
    root.mainloop()