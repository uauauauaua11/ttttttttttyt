
import tkinter as tk
from tkinter import ttk, filedialog, simpledialog, messagebox
import pickle
from PIL import Image, ImageTk
from tkinter import Scrollbar
class_chat_messages = []
registration_window = None
login_window = None
personal_cabinet_window = None
user_data = {}
teacher_requests = {}
students_and_teachers = {}
root = tk.Tk()
root.title("Главное окно")
root.attributes('-fullscreen', True)
schools = ["Школа №1", "Школа №2", "Школа №3", "Школа №4"]
def clear_windows(exclude_window=None):
    if registration_window and registration_window.winfo_exists() and registration_window != exclude_window:
        registration_window.withdraw()
    if login_window and login_window.winfo_exists() and login_window != exclude_window:
        login_window.withdraw()
    if personal_cabinet_window and personal_cabinet_window.winfo_exists() and personal_cabinet_window != exclude_window:
        personal_cabinet_window.withdraw()
def load_user_data_from_file():
    global user_data
    try:
        with open('user_data.txt', 'r') as file:
            for line in file:
                data = line.strip().split(':')
                if len(data) == 6:
                    username, password, user_type, email, full_name, school = data
                    user_data[username] = {'password': password, 'user_type': user_type, 'email': email, 'full_name': full_name, 'school': school}
    except FileNotFoundError:
        pass

def load_class_data_from_file():
    global students_and_teachers
    try:
        with open('class_data.txt', 'r') as file:
            for line in file:
                data = line.strip().split(':')
                if len(data) >= 2:
                    teacher, students = data[0], data[1:]
                    students_and_teachers[teacher] = students
    except FileNotFoundError:
        pass

def load_requests_data_from_file():
    global teacher_requests
    try:
        with open('requests_data.txt', 'r') as file:
            for line in file:
                data = line.strip().split(':')
                if len(data) >= 2:
                    teacher, requests = data[0], data[1].split(',')
                    teacher_requests[teacher] = requests
    except FileNotFoundError:
        pass

def save_class_data_to_file():
    with open('class_data.txt', 'w') as file:
        for teacher, students in students_and_teachers.items():
            file.write(f"{teacher}:{':'.join(students)}\n")

def save_requests_data_to_file():
    with open('requests_data.txt', 'w') as file:
        for teacher, requests in teacher_requests.items():
            file.write(f"{teacher}:{','.join(requests)}\n")





def open_registration_window(user_type):
    global registration_window
    if registration_window is not None:
        registration_window.destroy()

   
    clear_windows(exclude_window=registration_window)

    root.withdraw()  

    def register_user():
        username = username_entry.get()
        password = password_entry.get()
        email = email_entry.get()
        full_name = full_name_entry.get()
        school = school_combobox.get()  



        if username and password and email and full_name:
            user_data[username] = {'password': password, 'user_type': user_type, 'email': email, 'full_name': full_name, 'school': school}

            with open('user_data.txt', 'a') as file:
                file.write(f"{username}:{password}:{user_type}:{email}:{full_name}:{school}\n")

          




            if user_type == "Ученик" and teacher_name_entry.get() and teacher_name_entry.get() in user_data:
                send_request_to_teacher(username, teacher_name_entry.get())

            
            username_entry.delete(0, tk.END)
            password_entry.delete(0, tk.END)
            email_entry.delete(0, tk.END)
            full_name_entry.delete(0, tk.END)

            
            open_login_window(user_type)
            root.deiconify()  

    registration_window = tk.Toplevel(root)
    registration_window.title("Регистрация")
    registration_window.attributes('-fullscreen', True)

    tk.Label(registration_window, text="Имя пользователя:").place(relx=0.45, rely=0.3, anchor=tk.E)
    username_entry = tk.Entry(registration_window)
    username_entry.place(relx=0.465, rely=0.3, anchor=tk.W)

    tk.Label(registration_window, text="Пароль:").place(relx=0.45, rely=0.4, anchor=tk.E)
    password_entry = tk.Entry(registration_window, show="*")
    password_entry.place(relx=0.465, rely=0.4, anchor=tk.W)

    tk.Label(registration_window, text="Почта:").place(relx=0.45, rely=0.5, anchor=tk.E)
    email_entry = tk.Entry(registration_window)
    email_entry.place(relx=0.465, rely=0.5, anchor=tk.W)

    tk.Label(registration_window, text="Ф.И.О:").place(relx=0.45, rely=0.6, anchor=tk.E)
    full_name_entry = tk.Entry(registration_window)
    full_name_entry.place(relx=0.465, rely=0.6, anchor=tk.W)

    school_label = tk.Label(registration_window, text="Школа:")
    school_label.place(relx=0.45, rely=0.7, anchor=tk.E)

    school_combobox = ttk.Combobox(registration_window, values=schools)
    school_combobox.place(relx=0.465, rely=0.7, anchor=tk.W)
    school_combobox.set(schools[0])  

    



    if user_type == "Ученик":
        tk.Label(registration_window, text="Имя учителя:").place(relx=0.45, rely=0.8, anchor=tk.E)
        teacher_name_entry = tk.Entry(registration_window)
        teacher_name_entry.place(relx=0.465, rely=0.8, anchor=tk.W)

    register_button = tk.Button(registration_window, text="Зарегистрироваться", command=register_user, height=2, width=20)
    register_button.place(relx=0.5, rely=0.9, anchor=tk.CENTER)

    
    login_button = tk.Button(registration_window, text="Войти", command=lambda: open_login_window(user_type), height=2, width=20)
    login_button.place(relx=0.5, rely=0.95, anchor=tk.CENTER)

class_chats = {}


def open_login_window(user_type):
    global login_window
    if login_window is not None:
        login_window.destroy()

    clear_windows(exclude_window=login_window)

    root.withdraw()  

    def login_user():
        username = username_entry.get()
        password = password_entry.get()

        if username in user_data and user_data[username]['password'] == password and user_data[username]['user_type'] == user_type:
            print(f"Пользователь {username} успешно вошел как {user_type}")
            open_personal_cabinet(username, user_type)
            root.deiconify()  
        else:
            messagebox.showerror("Ошибка", "Неправильное имя пользователя или пароль. Пожалуйста, попробуйте снова.")

    login_window = tk.Toplevel(root)
    login_window.title("Вход")
    login_window.attributes('-fullscreen', True)

    tk.Label(login_window, text="Имя пользователя:").place(relx=0.45, rely=0.3, anchor=tk.E)
    username_entry = tk.Entry(login_window)
    username_entry.place(relx=0.465, rely=0.3, anchor=tk.W)


    tk.Label(login_window, text="Пароль:").place(relx=0.45, rely=0.4, anchor=tk.E)
    password_entry = tk.Entry(login_window, show="*")
    password_entry.place(relx=0.465, rely=0.4, anchor=tk.W)

    login_button = tk.Button(login_window, text="Войти", command=login_user, height=2, width=20)
    login_button.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
def open_personal_cabinet(username, user_type, teacher_name=None):
    global user_data

    

    def create_anonymous_chat():
        chat_window = tk.Toplevel(personal_cabinet_window)
        chat_window.title("Анонимный чат")

        chat_frame = tk.Frame(chat_window)
        chat_frame.pack(side=tk.LEFT, padx=10, pady=10)

        chat_text = tk.Text(chat_frame, height=15, width=50, wrap=tk.WORD, font=("Helvetica", 14))
        chat_text.pack(padx=10, pady=10)

        scrollbar = Scrollbar(chat_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        chat_text.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=chat_text.yview)

        message_entry = tk.Entry(chat_window, font=("Helvetica", 14))
        message_entry.pack(padx=10, pady=10)

        send_button = tk.Button(chat_window, text="Отправить", command=send_message_anonymously, height=2, width=20,
                                font=("Helvetica", 14))
        send_button.pack(padx=10, pady=10)

    def send_message_anonymously():
            message = message_entry.get()
            if message:
                message_to_send = f"Аноним: {message}"
                chat_text.insert(tk.END, message_to_send + "\n")
                message_entry.delete(0, tk.END)


    def upload_photo():
        schedule_text = simpledialog.askstring("Создание расписания", "Введите расписание:")

        if schedule_text:
          
            with open("schedule.txt", "a") as schedule_file:
                schedule_file.write(f"{username} ({user_type}) создал(а) расписание:\n{schedule_text}\n\n")
                messagebox.showinfo("Успешно", "Расписание создано и сохранено.")

    def create_event():
        event_text = simpledialog.askstring("Создание события", "Введите текст события:")

        if event_text:
            
            with open("events.txt", "a") as file:
                file.write(f"{username} ({user_type}) создал(а) событие: {event_text}\n")
                messagebox.showinfo("Успешно", "Событие создано и сохранено.")

    def post_news():
        news_text = simpledialog.askstring("Публикация новости", "Введите текст новости:")

        if news_text:
            
            with open("news.txt", "a") as file:
                file.write(f"{username} ({user_type}) опубликовал(а) новость: {news_text}\n")
                messagebox.showinfo("Успешно", "Новость опубликована и сохранена.")
    global personal_cabinet_window
    global registration_window

    def send_message_to_class_chat():
        message = message_entry.get()
        if message:
            if user_type == "Учитель":
                message_to_send = f"Учитель {username}: {message}"
            elif user_type == "Ученик":
                message_to_send = f"Ученик {username}: {message}"

            class_chat_messages.append(message_to_send)
            message_entry.delete(0, tk.END)

            update_class_chat()


        update_class_chat()

    def save_messages_to_file(filename, messages):
         with open(filename, 'wb') as file:
                pickle.dump(messages, file)

    def send_message_to_class_chat():
        message = message_entry.get()
        if message:
            
            if teacher_name not in class_chats:
                class_chats[teacher_name] = []

            message_to_send = f"Ученик {username}: {message}"
            class_chats[teacher_name].append(message_to_send)
            update_class_chat(teacher_name)  
            message_entry.delete(0, tk.END)

    def update_class_chat(teacher_name):
        chat_text.config(state=tk.NORMAL)  
        chat_text.delete(1.0, tk.END)  

        
        messages = class_chats.get(teacher_name, [])

        for message in messages:
            chat_text.insert(tk.END, message + "\n")

        chat_text.config(state=tk.DISABLED)

  
    personal_cabinet_window = tk.Toplevel(root)
    personal_cabinet_window.title(f"Личный кабинет - {user_type}")
    personal_cabinet_window.configure()


    personal_cabinet_window.attributes("-fullscreen", True)

    tk.Label(personal_cabinet_window, text=f"Добро пожаловать, {username}!").pack()
    tk.Label(personal_cabinet_window, text=f"Логин: {username}", ).pack()
    tk.Label(personal_cabinet_window, text=f"Почта: {user_data[username]['email']}").pack()
    tk.Label(personal_cabinet_window, text=f"Ф.И.О: {user_data[username]['full_name']}").pack()
    tk.Label(personal_cabinet_window, text=f"Школа: {user_data[username]['school']}").pack()
    def load_messages_from_file(filename):
        try:
            with open(filename, 'rb') as file:
                messages = pickle.load(file)
            return messages
        except FileNotFoundError:
            return []

    
    class_chat_messages = load_messages_from_file('messages.pkl')

 
    if user_type in ["Учитель"]:
        tk.Label(personal_cabinet_window, text="Чат класса:                                                            ",  font=("Helvetica", 18)).pack(anchor=tk.NE,
                                                                                                       padx=10, pady=10)
        upload_photo_button = tk.Button(
            personal_cabinet_window, text="расписание",
            command=upload_photo, height=2, width=7, font=("Helvetica", 14)
        )
        upload_photo_button.pack(side=tk.RIGHT, padx=10, pady=10, anchor="s", )

        create_event_button = tk.Button(
            personal_cabinet_window, text=" событие",
            command=create_event, height=2, width=7, font=("Helvetica", 14)
        )
        create_event_button.pack(side=tk.RIGHT , padx=10, pady=10, anchor="s",)

        post_news_button = tk.Button(
            personal_cabinet_window, text=" новость",
            command=post_news, height=2, width=7, font=("Helvetica", 14)
        )
        post_news_button.pack(side=tk.RIGHT, padx=10, pady=10, anchor="s", )

        chat_frame = tk.Frame(personal_cabinet_window)
        chat_frame.pack(side=tk.RIGHT, anchor=tk.NE, padx=10, pady=10)

        chat_text = tk.Text(chat_frame, height=15, width=50, wrap=tk.WORD, font=("Helvetica", 14))
        chat_text.pack(padx=10, pady=10)

        scrollbar = Scrollbar(chat_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        chat_text.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=chat_text.yview)

        message_entry = tk.Entry(chat_frame, font=("Helvetica", 14))
        message_entry.pack(padx=10, pady=10)

        send_button = tk.Button(chat_frame, text="Отправить", command=send_message_to_class_chat, height=2, width=20,
                                 font=("Helvetica", 14))
        send_button.pack(padx=10, pady=10)

        def send_message_to_class_chat():
            message = message_entry.get()
            if message:
                if user_type == "Учитель":
                    message_to_send = f"Учитель {username}: {message}"
                elif user_type == "Ученик":
                    message_to_send = f"Ученик {username}: {message}"

                class_chat_messages.append(message_to_send)
                update_class_chat()  
                message_entry.delete(0, tk.END)
        def confirm_request():
            selected_request = requests_listbox.get(requests_listbox.curselection())
            if selected_request:
                if user_type == "Учитель":
                    anonymous_chat_button = tk.Button(
                        personal_cabinet_window, text="Анонимный чат",
                        command=create_anonymous_chat, height=2, width=20, font=("Helvetica", 14)
                    )
                    anonymous_chat_button.pack(side=tk.RIGHT, padx=10, pady=10, anchor="s")
                    
                    news_button = tk.Button(
                        personal_cabinet_window, text="Новости",
                        command=display_news, height=2, width=10, font=("Helvetica", 14)
                    )
                    news_button.pack(side=tk.RIGHT, padx=10, pady=10, anchor="s")

                    events_button = tk.Button(
                        personal_cabinet_window, text="События",
                        command=display_events, height=2, width=10, font=("Helvetica", 14)
                    )
                    events_button.pack(side=tk.RIGHT, padx=10, pady=10, anchor="s")
                    
                    if username in students_and_teachers:
                        students_and_teachers[username].append(selected_request)
                    else:
                        students_and_teachers[username] = [selected_request]

                    
                    if selected_request in teacher_requests[username]:
                        teacher_requests[username].remove(selected_request)

                    save_class_data_to_file()
                    save_requests_data_to_file()

                    messagebox.showinfo("Успешно", f"Запрос от {selected_request} подтвержден.")

        requests_listbox = tk.Listbox(personal_cabinet_window, font=("Helvetica", 14))
        requests_listbox.pack(anchor=tk.W, padx=10, pady=10)

        confirm_button = tk.Button(personal_cabinet_window, text="Подтвердить запрос", command=confirm_request, height=2, width=20, bg="white", font=("Helvetica", 14))
        confirm_button.pack(anchor=tk.W, padx=10, pady=10)

        def update_requests_listbox():
            requests_listbox.delete(0, tk.END)
            if username in teacher_requests:
                for request in teacher_requests[username]:
                    requests_listbox.insert(tk.END, request)

        update_requests_listbox()

    elif user_type == "Ученик":
       
        events_button = tk.Button(
            personal_cabinet_window, text="События",
            command=display_events, height=2, width=10, font=("Helvetica", 14)
        )
        events_button.pack(side=tk.RIGHT, padx=10, pady=10, anchor="s")

        schedule_button = tk.Button(
            personal_cabinet_window, text="Расписание",
            command=display_schedule, height=2, width=10, font=("Helvetica", 14)
        )
        schedule_button.pack(side=tk.RIGHT, padx=10, pady=10, anchor="s")
        news_button = tk.Button(
            personal_cabinet_window, text="Новости",
            command=display_news, height=2, width=10, font=("Helvetica", 14)
        )
        news_button.pack(side=tk.RIGHT, padx=10, pady=10, anchor="s")

        tk.Label(personal_cabinet_window, text="Чат класса:", font=("Helvetica", 18)).pack(anchor=tk.NE, padx=10,
                                                                                           pady=10)
        chat_frame = tk.Frame(personal_cabinet_window)
        chat_frame.pack(side=tk.RIGHT, anchor=tk.NE, padx=10, pady=10)

        chat_text = tk.Text(chat_frame, height=15, width=50, wrap=tk.WORD, font=("Helvetica", 14))
        chat_text.pack(padx=10, pady=10)

        scrollbar = Scrollbar(chat_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        chat_text.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=chat_text.yview)

        message_entry = tk.Entry(chat_frame, font=("Helvetica", 14))
        message_entry.pack(padx=10, pady=10)

        send_button = tk.Button(chat_frame, text="Отправить", command=send_message_to_class_chat, height=2, width=20,
                                font=("Helvetica", 14))
        send_button.pack(padx=10, pady=10)

    back_button = tk.Button(
        personal_cabinet_window, text="Назад",
        command=lambda: back_to_main_window(personal_cabinet_window),
        height=2, width=10, bg="white", font=("Helvetica", 10)


    )


    back_button.pack(side="bottom", padx=10, pady=10, anchor="sw")

def create_schedule(username,user_type):
        schedule_text = simpledialog.askstring("Создание расписания", "Введите расписание:")

        if schedule_text:
           
            with open("schedule.txt", "a") as schedule_file:
                schedule_file.write(f"{username} ({user_type}) создал(а) расписание:\n{schedule_text}\n\n")
                messagebox.showinfo("Успешно", "Расписание создано и сохранено.")
def display_schedule():
    schedule_window = tk.Toplevel(personal_cabinet_window)
    schedule_window.title("Расписание")
    schedule_text = tk.Text(schedule_window, wrap=tk.WORD, font=("Helvetica", 14))
    schedule_text.pack(padx=10, pady=10)

    with open("schedule.txt", "r") as schedule_file:
        schedule_data = schedule_file.read()
        schedule_text.insert(tk.END, schedule_data)
def display_events():
    events_window = tk.Toplevel(personal_cabinet_window)
    events_window.title("События")
    events_text = tk.Text(events_window, wrap=tk.WORD, font=("Helvetica", 14))
    events_text.pack(padx=10, pady=10)

    with open("events.txt", "r") as events_file:
        events_data = events_file.read()
        events_text.insert(tk.END, events_data)



def clear_personal_cabinet(window):
    for widget in window.winfo_children():
        widget.destroy()

def back_to_main_window(window):
    window.destroy()
    root.deiconify()  
def choose_user_type():
    start_frame.pack_forget()
    type_frame.place(relx=0.5, rely=0.5,
                     anchor=tk.CENTER)  
    button_width = 20
    button_height = 5

    teacher_button = tk.Button(type_frame, text="Учитель", command=lambda: open_registration_window("Учитель"),
                               width=button_width, height=button_height)
    student_button = tk.Button(type_frame, text="Ученик", command=lambda: open_registration_window("Ученик"),
                               width=button_width, height=button_height)
    parent_button = tk.Button(type_frame, text="Родитель", command=lambda: open_registration_window("Родитель"),
                              width=button_width, height=button_height)

  
    teacher_button.pack(side=tk.LEFT, padx=10)
    student_button.pack(side=tk.LEFT, padx=10)
    parent_button.pack(side=tk.LEFT, padx=10)

def send_request_to_teacher(student_username, teacher_name):
    if teacher_name in teacher_requests:
        teacher_requests[teacher_name].append(student_username)
    else:
        teacher_requests[teacher_name] = [student_username]

    save_requests_data_to_file()


def view_and_confirm_requests(teacher_username):
    global teacher_requests

    if teacher_username in teacher_requests and teacher_requests[teacher_username]:
        requests = teacher_requests[teacher_username]
        requests_str = "\n".join(requests)

        result = messagebox.askquestion("Запросы на добавление", f"У вас есть запросы на добавление от следующих учеников:\n\n{requests_str}\n\nХотите подтвердить их добавление в ваш класс?")

        if result == "yes":
            if teacher_username in students_and_teachers:
                students_and_teachers[teacher_username].extend(requests)
            else:
                students_and_teachers[teacher_username] = requests

            del teacher_requests[teacher_username]

            save_class_data_to_file()
            save_requests_data_to_file()
            messagebox.showinfo("Успешно", "Запросы на добавление учеников подтверждены.")
    else:
        messagebox.showinfo("Запросы на добавление", "У вас нет текущих запросов на добавление учеников.")

start_frame = tk.Frame(root, highlightbackground="white", highlightthickness=0)
start_frame.pack(pady=20)

def on_start_click(event):
    x, y = event.x, event.y
    if 00 <= x <= 1400 and 100 <= y <= 1300:
        canvas.unbind("<Button-1>")  
        canvas.delete("all")  
        choose_user_type()

start_button_image = Image.open("старт.png")  
start_button_image = start_button_image.resize((600, 500)) 
start_button_photo = ImageTk.PhotoImage(start_button_image)

canvas = tk.Canvas(root, width=400, height=300, borderwidth=0, highlightthickness=0)
canvas.place(x=650, y=250)  

canvas.create_image(0, 0, anchor=tk.NW, image=start_button_photo)

canvas.bind("<Button-1>", on_start_click)

def display_schedule():
    schedule_window = tk.Toplevel(personal_cabinet_window)
    schedule_window.title("Расписание")
    schedule_text = tk.Text(schedule_window, wrap=tk.WORD, font=("Helvetica", 14))
    schedule_text.pack(padx=10, pady=10)

    with open("schedule.txt", "r") as schedule_file:
        schedule_data = schedule_file.read()
        schedule_text.insert(tk.END, schedule_data)
def display_news():
    events_window = tk.Toplevel(personal_cabinet_window)
    events_window.title("Новости")
    events_text = tk.Text(events_window, wrap=tk.WORD, font=("Helvetica", 14))
    events_text.pack(padx=10, pady=10)

    with open("news.txt", "r") as events_file:
        events_data = events_file.read()
        events_text.insert(tk.END, events_data)
def display_events():
    events_window = tk.Toplevel(personal_cabinet_window)
    events_window.title("События")
    events_text = tk.Text(events_window, wrap=tk.WORD, font=("Helvetica", 14))
    events_text.pack(padx=10, pady=10)

    with open("events.txt", "r") as events_file:
        events_data = events_file.read()
        events_text.insert(tk.END, events_data)
type_frame = tk.Frame(root)

 
type_frame.place_forget()

load_user_data_from_file()

load_class_data_from_file()


load_requests_data_from_file()

root.mainloop()

