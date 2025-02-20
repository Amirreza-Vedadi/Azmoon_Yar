from tkinter import *
from tkinter.messagebox import showinfo
from controller.questions_controller import QuestionsController

class ExamUI:
    def __init__(self):
        self.window = Tk()
        self.window.title("آزمون")
        self.window.geometry("700x500")
        self.window.iconbitmap("exam.ico")
        self.window.configure(bg="#2471a3")
        self.window.resizable(False, False)
        self.questions = []
        self.current_index = 0
        self.user_answers = {}
        self.timer = None
        self.time_left = 0
        self.navigation_enabled = False

        self.question_label = Label(self.window, text="", font=("B Koodak", 16), fg="white", bg="#2471a3", wraplength=600)
        self.question_label.pack(pady=20)

        self.options_var = StringVar()
        self.option_buttons = []
        for i in range(4):
            rb = Radiobutton(self.window, text="", variable=self.options_var, value=str(i+1), bg="#2471a3", font=("B Koodak", 14))
            rb.pack(anchor=W, padx=50)
            self.option_buttons.append(rb)

        self.timer_label = Label(self.window, text="", font=("B Koodak", 14), fg="yellow", bg="#2471a3")
        self.timer_label.pack(pady=10)

        self.btn_prev = Button(self.window, text="سوال قبلی", command=self.prev_question, state=DISABLED, width=15)
        self.btn_prev.pack(side=LEFT, padx=20, pady=20)

        self.btn_next = Button(self.window, text="سوال بعدی", command=self.next_question, width=15)
        self.btn_next.pack(side=RIGHT, padx=20, pady=20)

        self.btn_finish = Button(self.window, text="اتمام آزمون", command=self.finish_exam, width=15)
        self.btn_finish.pack(side=BOTTOM, pady=20)

        self.load_questions()
        self.display_question()

        self.window.mainloop()

    def load_questions(self):
        q_controller = QuestionsController()
        self.questions = q_controller.find_all()
        if not self.questions:
            showinfo("خطا", "هیچ سوالی در دیتابیس وجود ندارد.")
            self.window.destroy()

    def display_question(self):
        if self.timer:
            self.window.after_cancel(self.timer)
            self.timer = None

        question = self.questions[self.current_index]
        self.question_label.config(text=f"سوال {self.current_index + 1}: {question[1]}")

        options = [question[2], question[3], question[4], question[5]]
        for i, option in enumerate(options):
            self.option_buttons[i].config(text=option, value=str(i+1))

        self.navigation_enabled = bool(question[8])
        self.options_var.set(self.user_answers.get(self.current_index, ""))

        if not self.navigation_enabled:
            try:
                self.time_left = int(question[7])
            except ValueError:
                self.time_left = 0
            self.start_timer()
        else:
            self.timer_label.config(text="")

        self.btn_prev.config(state=NORMAL if self.navigation_enabled and self.current_index > 0 else DISABLED)
        self.btn_next.config(state=NORMAL if self.current_index < len(self.questions) - 1 else DISABLED)

    def start_timer(self):
        self.timer_label.config(text=f"زمان باقی‌مانده: {self.time_left} ثانیه")
        if self.time_left > 0:
            self.time_left -= 1
            self.timer = self.window.after(1000, self.start_timer)
        else:
            self.auto_next_question()

    def save_answer(self):
        selected_option = self.options_var.get()
        if selected_option:
            self.user_answers[self.current_index] = selected_option

    def auto_next_question(self):
        self.save_answer()
        if self.current_index < len(self.questions) - 1:
            self.current_index += 1
            self.display_question()
        else:
            self.finish_exam()

    def next_question(self):
        if not self.navigation_enabled and self.timer:
            self.window.after_cancel(self.timer)
            self.timer = None
        self.save_answer()
        if self.current_index < len(self.questions) - 1:
            self.current_index += 1
            self.display_question()

    def prev_question(self):
        if not self.navigation_enabled and self.timer:
            self.window.after_cancel(self.timer)
            self.timer = None
        self.save_answer()
        if self.current_index > 0:
            self.current_index -= 1
            self.display_question()

    def finish_exam(self):
        if self.timer:
            self.window.after_cancel(self.timer)
            self.timer = None
        self.save_answer()

        correct_count = 0
        total_questions = len(self.questions)

        for index, question in enumerate(self.questions):
            try:
                correct_option_index = int(question[6])
            except (ValueError, IndexError):
                showinfo("خطا", "خطایی در پردازش گزینه‌های صحیح رخ داده است.")
                return

            user_answer = self.user_answers.get(index, "")
            if user_answer == str(correct_option_index):
                correct_count += 1

        wrong_count = total_questions - correct_count
        percentage = (correct_count / total_questions) * 100

        showinfo("نتیجه آزمون", f"تعداد کل سوالات: {total_questions}\n"
                                f"پاسخ‌های صحیح: {correct_count}\n"
                                f"پاسخ‌های غلط: {wrong_count}\n"
                                f"درصد: {percentage:.2f}%")

        self.window.destroy()
