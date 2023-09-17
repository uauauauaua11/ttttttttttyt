from tkinter import *
import tkinter as tk
import pickle

# Функция для перехода к следующему окну
def switch_to_next_window():
    # Скрываем текущее окно
    main_window.withdraw()
    
    # Показываем новое окно
    second_window.deiconify()

# Функция для возвращения к первому окну
def switch_to_main_window():
    # Скрываем текущее окно
    second_window.withdraw()
    
    # Показываем первое окно
    main_window.deiconify()

def switch_to_student_window():
    second_window.withdraw()
    student_window.deiconify()

def switch_to_parent_window():
    second_window.withdraw()
    parent_window.deiconify()

def switch_to_teacher_window():
    second_window.withdraw()
    teacher_window.deiconify()

def register_student():
    student_name = student_name_entry.get()
    student_id = student_id_entry.get()
    # Ваши действия по регистрации ученика

def register_parent():
    parent_name = parent_name_entry.get()
    parent_email = parent_email_entry.get()
    # Ваши действия по регистрации родителя

def register_teacher():
    teacher_name = teacher_name_entry.get()
    teacher_subject = teacher_subject_entry.get()
    # Ваши действия по регистрации учителя

def save_student():
    login_pass_save_student = {}
    login_pass_save_student[student_name_entry.get()] = student_password_entry.get()
    base = open("login.txt", "wb")
    pickle.dump(login_pass_save_student, base)
    base.close()
    register_student()

def save_parent():
    login_pass_save_parent = {}
    login_pass_save_parent[parent_name_entry.get()] = parent_password_entry.get()
    base = open("login.txt", "wb")
    pickle.dump(login_pass_save_parent, base)
    base.close()
    register_parent()

def save_teacher():
    login_pass_save_teacher = {}
    login_pass_save_teacher[teacher_name_entry.get()] = teacher_password_entry.get()
    base = open("login.txt", "wb")
    pickle.dump(login_pass_save_teacher, base)
    base.close()
    register_teacher()

# Создаем основное окно
main_window = tk.Tk()
main_window.title("Главное окно")
main_window.attributes('-fullscreen', True)

# Создаем кнопку для перехода ко второму окну
switch_button = tk.Button(main_window, text="Перейти к следующему окну", command=switch_to_next_window)
switch_button.pack()

# Создаем второе окно
second_window = tk.Toplevel(main_window)
second_window.title("Второе окно")
second_window.withdraw()
second_window.attributes('-fullscreen', True)

# Создаем кнопку для возврата к главному окну
back_button = tk.Button(second_window, text="Вернуться к главному окну", command=switch_to_main_window)
back_button.pack()

# Создаем кнопку для перехода к окну "Ученик"
student_button = tk.Button(second_window, text="Ученик", command=switch_to_student_window)
student_button.pack()

# Создаем окно "Ученик"
student_window = tk.Toplevel(main_window)
student_window.title("Окно Ученика")
student_window.withdraw()
student_window.attributes('-fullscreen', True)

# Добавляем поля ввода для регистрации ученика
student_name_label = Label(student_window, text="Ф.И.О ученика:")
student_name_label.pack()
student_name_entry = Entry(student_window)
student_name_entry.pack()
student_password_label = Label(student_window, text="Пароль ученика:")
student_password_label.pack()
student_password_entry = Entry(student_window, show="*")  # Пароль скрывается
student_password_entry.pack()
student_id_label = Label(student_window, text="ID ученика:")
student_id_label.pack()
student_id_entry = Entry(student_window)
student_id_entry.pack()
register_student_button = Button(student_window, text="Зарегистрировать ученика", command=save_student)
register_student_button.pack()

# Создаем кнопку для перехода к окну "Родитель"
parent_button = tk.Button(second_window, text="Родитель", command=switch_to_parent_window)
parent_button.pack()

# Создаем окно "Родитель"
parent_window = tk.Toplevel(main_window)
parent_window.title("Окно Родителя")
parent_window.withdraw()
parent_window.attributes('-fullscreen', True)

# Добавляем поля ввода для регистрации родителя
parent_name_label = Label(parent_window, text="Ф.И.О родителя:")
parent_name_label.pack()
parent_name_entry = Entry(parent_window)
parent_name_entry.pack()
parent_password_label = Label(parent_window, text="Пароль родителя:")
parent_password_label.pack()
parent_password_entry = Entry(parent_window, show="*")  # Пароль скрывается
parent_password_entry.pack()
parent_email_label = Label(parent_window, text="Email родителя:")
parent_email_label.pack()
parent_email_entry = Entry(parent_window)
parent_email_entry.pack()
register_parent_button = Button(parent_window, text="Зарегистрировать родителя", command=save_parent)
register_parent_button.pack()

# Создаем кнопку для перехода к окну "Учитель"
teacher_button = tk.Button(second_window, text="Учитель", command=switch_to_teacher_window)
teacher_button.pack()

# Создаем окно "Учитель"
teacher_window = tk.Toplevel(main_window)
teacher_window.title("Окно Учителя")
teacher_window.withdraw()
teacher_window.attributes('-fullscreen', True)

# Добавляем поля ввода для регистрации учителя
teacher_name_label = Label(teacher_window, text="Имя учителя:")
teacher_name_label.pack()
teacher_name_entry = Entry(teacher_window)
teacher_name_entry.pack()
teacher_password_label = Label(teacher_window, text="Пароль учителя:")
teacher_password_label.pack()
teacher_password_entry = Entry(teacher_window, show="*")  # Пароль скрывается
teacher_password_entry.pack()
teacher_subject_label = Label(teacher_window, text="Предмет учителя:")
teacher_subject_label.pack()
teacher_subject_entry = Entry(teacher_window)
teacher_subject_entry.pack()
register_teacher_button = Button(teacher_window, text="Зарегистрировать учителя", command=save_teacher)
register_teacher_button.pack()

# Запускаем главный цикл приложения
main_window.mainloop()
