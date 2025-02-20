from tkinter import *
from tkinter.ttk import *
from tkinter.messagebox import showerror, showinfo
from controller.users_controller import Users_controller
from exam_ui import ExamUI
from question_ui import QuestionsUI


def type_text(label, text, index=0):
    if index <= len(text):
        label.config(text=text[:index])
        index += 1
        label.after(70, type_text, label, text, index)


class Sign_in_UI:
    def __init__(self):
        self.win = Tk()
        self.win.title("ورود کاربر")
        self.win.geometry("300x300")
        self.win.iconbitmap("exam.ico")
        self.win.resizable(False, False)
        self.win.configure(bg="#2471a3")


        self.label = Label(self.win, text="", anchor="e", justify="right", foreground="white",
                           background="#2471a3", font=("B Koodak", 14))
        self.label.pack(pady=5)
        type_text(self.label, "برای ورود اطلاعات خواسته شده را وارد کنین")


        Label(self.win, text="کد ملی", foreground="white", background="#2471a3", font=("B Koodak", 14)).pack(pady=5)
        self.id_txt = Entry(self.win, width=20)
        self.id_txt.pack(pady=5)

        self.student_btn = Button(self.win, text="دانش‌آموز", command=lambda: self.login("دانش‌آموز"))
        self.student_btn.pack(pady=5)

        self.teacher_btn = Button(self.win, text="استاد", command=lambda: self.login("استاد"))
        self.teacher_btn.pack(pady=5)

        self.win.mainloop()

    def login(self, role):
        id = self.id_txt.get().strip()
        if not id:
            showerror("خطا", "لطفاً کد ملی را وارد کنین")
            return

        user_controller = Users_controller()
        result = user_controller.validate_user(id, role)

        if result:
            showinfo("موفقیت", f"خوش آمدید! شما به عنوان {role} وارد شدید")
            self.win.destroy()

            if role == "استاد":
                QuestionsUI()
            elif role == "دانش‌آموز":
                ExamUI()
        else:
            showerror("خطا", "کد ملی یا نقش انتخاب‌شده صحیح نیست")
