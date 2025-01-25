from tkinter import *
from tkinter.messagebox import showinfo, showerror, askyesno
from tkinter.ttk import Combobox
from controller.questions_controller import QuestionsController
from table import Table


class QuestionsUI:
    def clear(self):
        self.question_txt.delete(0, END)
        self.option1_txt.delete(0, END)
        self.option2_txt.delete(0, END)
        self.option3_txt.delete(0, END)
        self.option4_txt.delete(0, END)
        self.correct_option_cmb.set("گزینه ۱")
        self.exam_time_txt.delete(0, END)

    def test(self, selected):
        self.clear()
        self.question_txt.insert(0, selected[1])
        self.option1_txt.insert(0, selected[2])
        self.option2_txt.insert(0, selected[3])
        self.option3_txt.insert(0, selected[4])
        self.option4_txt.insert(0, selected[5])
        self.correct_option_cmb.set(selected[6])
        self.exam_time_txt.insert(0, selected[7])
        self.navigation_enabled_var.set(selected[8])
        self.selected_id = selected[0]

    def search_question(self):
        question_id = self.id_txt.get()
        if not question_id.isdigit():
            showinfo("خطا", "لطفاً یک عدد صحیح برای ID وارد کنید.")
            return

        q_controller = QuestionsController()
        question = q_controller.search(question_id)

        if question:

            self.clear()
            self.question_txt.insert(0, question[1])
            self.option1_txt.insert(0, question[2])
            self.option2_txt.insert(0, question[3])
            self.option3_txt.insert(0, question[4])
            self.option4_txt.insert(0, question[5])
            self.correct_option_cmb.set(question[6])
            self.exam_time_txt.insert(0, question[7])
        else:
            showinfo("جستجو", "سوالی با این ID پیدا نشد.")

    def save_question(self):
        question = self.question_txt.get()
        option1 = self.option1_txt.get()
        option2 = self.option2_txt.get()
        option3 = self.option3_txt.get()
        option4 = self.option4_txt.get()
        correct_option = self.correct_option_cmb.get()
        exam_time = self.exam_time_txt.get()
        navigation_enabled = self.navigation_enabled_var.get()
        if not question or not option1 or not correct_option or not exam_time:
            showerror("خطا", "لطفاً تمام فیلدها را پر کنید")
            return

        q_controller = QuestionsController()
        result = q_controller.save(question, option1, option2, option3, option4, correct_option, exam_time,
                                   navigation_enabled)
        if result["status"] == "error":
            showerror("خطا", result["message"])
        else:
            showinfo("ذخیره", "سوال با موفقیت ذخیره شد")
            self.refresh_table()
            self.clear()

    def edit_question(self):
        if not hasattr(self, "selected_id"):
            showerror("خطا", "لطفاً یک سوال را از جدول انتخاب کنید")
            return

        question = self.question_txt.get()
        option1 = self.option1_txt.get()
        option2 = self.option2_txt.get()
        option3 = self.option3_txt.get()
        option4 = self.option4_txt.get()
        correct_option = self.correct_option_cmb.get()
        exam_time = self.exam_time_txt.get()
        navigation_enabled = self.navigation_enabled_var.get()

        if not question or not option1 or not correct_option or not exam_time:
            showerror("خطا", "تمام فیلدها را پر کنید")
            return

        q_controller = QuestionsController()
        result = q_controller.edit(self.selected_id, question, option1, option2, option3, option4, correct_option,
                                   exam_time, navigation_enabled)
        if result["status"] == "error":
            showerror("خطا", result["message"])
        else:
            showinfo("ویرایش", "سوال با موفقیت ویرایش شد")
            self.refresh_table()
            self.clear()

    def remove_question(self):
        if not hasattr(self, "selected_id"):
            showerror("خطا", "لطفاً یک سوال را از جدول انتخاب کنید")
            return

        if askyesno("حذف", "آیا از حذف سوال مطمئن هستید؟"):
            q_controller = QuestionsController()
            result = q_controller.remove(self.selected_id)
            if result["status"] == "success":
                showinfo("حذف", "سوال با موفقیت حذف شد")
            else:
                showerror("خطا", result["message"])
            self.refresh_table()
            self.clear()

    def refresh_table(self):
        q_controller = QuestionsController()
        questions_list = q_controller.find_all()
        self.table.set_items(questions_list)

    def __init__(self):
        self.win = Tk()
        self.win.geometry("900x800")
        self.win.title("مدیریت سوالات")
        self.win.configure(bg="#2471a3")
        self.win.iconbitmap("exam.ico")
        self.win.resizable(False, False)


        fields = [
            ("صورت سوال", 50, "question_txt"),
            ("گزینه ۱", 100, "option1_txt"),
            ("گزینه ۲", 150, "option2_txt"),
            ("گزینه ۳", 200, "option3_txt"),
            ("گزینه ۴", 250, "option4_txt"),
            ("زمان سوال (ثانیه)", 350, "exam_time_txt")
        ]

        for text, y, attr in fields:
            Label(self.win, text=text, fg="white", bg="#2471a3", font=("B Koodak", 14)).place(x=600, y=y)
            setattr(self, attr, Entry(self.win, width=40))
            getattr(self, attr).place(x=200, y=y + 5)

        Label(self.win, text="اجازه جابجایی بین سوالات", fg="white", bg="#2471a3", font=("B Koodak", 14)).place(x=600, y=695)
        self.navigation_enabled_var = IntVar(value=0)
        self.navigation_checkbox = Checkbutton(self.win, variable=self.navigation_enabled_var, bg="#2471a3")
        self.navigation_checkbox.place(x=550, y=700)

        Label(self.win, text="گزینه صحیح", fg="white", bg="#2471a3", font=("B Koodak", 14)).place(x=600, y=300)
        self.correct_option_cmb = Combobox(self.win, values=["گزینه ۱", "گزینه ۲", "گزینه ۳", "گزینه ۴"], state="readonly")
        self.correct_option_cmb.place(x=200, y=305)
        self.correct_option_cmb.set("گزینه ۱")

        Label(self.win, text="ID سوال", fg="white", bg="#2471a3", font=("B Koodak", 14)).place(x=600, y=10)
        self.id_txt = Entry(self.win, width=20)
        self.id_txt.place(x=200, y=15)

        Button(self.win, text="جستجو", command=self.search_question).place(x=350, y=12)
        Button(self.win, text="ذخیره", command=self.save_question).place(x=600, y=400)
        Button(self.win, text="ویرایش", command=self.edit_question).place(x=500, y=400)
        Button(self.win, text="حذف", command=self.remove_question).place(x=400, y=400)
        Button(self.win, text="خروج", command=self.win.destroy).place(x=300, y=400)

        self.table = Table(self.win, 10, 8, ["ID", "سوال", "گزینه۱", "گزینه۲", "گزینه۳", "گزینه۴", "صحیح", "زمان"],
                           [50, 200, 100, 100, 100, 100, 100, 50], 25, 450)
        self.refresh_table()
        self.table.on_click(self.test)

        self.win.mainloop()


