from tkinter import *
from tkinter.ttk import *
from tkinter.messagebox import *
from controller.users_controller import *
from table import Table


def type_text(label, text, index=0):
    if index <= len(text):
        label.config(text=text[:index])
        index += 1
        label.after(70, type_text, label, text, index)


class Sign_up_UI:

    def clear(self):
        self.id_txt.delete(0, END)
        self.name_txt.delete(0, END)
        self.family_txt.delete(0, END)
        self.role_combobox.set("")

    def test(self, selected):
        self.clear()
        self.id_txt.insert(0, selected[0])
        self.name_txt.insert(0, selected[1])
        self.family_txt.insert(0, selected[2])
        self.role_combobox.set(selected[3])

    def __init__(self):
        self.win = Tk()
        self.win.geometry("600x600")
        self.win.title("ثبت نام")
        self.win.iconbitmap("exam.ico")
        self.win.configure(bg="#2471a3")
        self.win.resizable(False, False)
        self.label = Label(self.win, text="", anchor="e", justify="right", foreground="white", background="#2471a3",
                           font=("B Koodak", 18))
        self.label.pack(pady=20)

        Button(self.win, text="جستجو", command=self.search_click).place(x=90, y=249)
        Button(self.win, text="ذخیره", command=self.save_click).place(x=415, y=540)
        Button(self.win, text="ویرایش", command=self.edit_click).place(x=315, y=540)
        Button(self.win, text="حذف", command=self.remove_click).place(x=215, y=540)
        Button(self.win, text="خروج", command=self.exit_click).place(x=115, y=540)

        type_text(self.label, "برای ثبت نام اطلاعات خواسته شده را وارد کنین")

        Label(self.win, text="کد ملی", foreground="white", background="#2471a3", font=("B Koodak", 14)).place(x=350,
                                                                                                              y=93)
        self.id_txt = Entry(self.win, width=20)
        self.id_txt.place(x=200, y=100)

        Label(self.win, text="نام", foreground="white", background="#2471a3", font=("B Koodak", 14)).place(x=350, y=143)
        self.name_txt = Entry(self.win, width=20)
        self.name_txt.place(x=200, y=150)

        Label(self.win, text="نام خانوادگی", foreground="white", background="#2471a3", font=("B Koodak", 14)).place(
            x=350, y=193)
        self.family_txt = Entry(self.win, width=20)
        self.family_txt.place(x=200, y=200)

        Label(self.win, text="نقش", foreground="white", background="#2471a3", font=("B Koodak", 14)).place(x=350, y=243)
        self.role_combobox = Combobox(self.win, values=["دانش‌آموز", "استاد"], state="readonly", width=18)
        self.role_combobox.place(x=200, y=250)
        self.role_combobox.set("دانش‌آموز")

        self.table = Table(self.win, 10, 4, ["id", "name", "family", "role"], [100, 150, 150, 100], 50, 300)
        u_c = Users_controller()
        users_list = u_c.find_all()
        self.table.set_items(users_list)
        self.table.on_click(self.test)

        self.win.mainloop()

    def search_click(self):
        id = self.id_txt.get()
        if not id:
            showerror("خطا", "لطفاً کد ملی را وارد کنید")
            return
        u_c = Users_controller()
        user = u_c.search(id)
        if user:
            self.id_txt.delete(0, END)
            self.name_txt.delete(0, END)
            self.family_txt.delete(0, END)

            self.id_txt.insert(0, user[0])
            self.name_txt.insert(0, user[1])
            self.family_txt.insert(0, user[2])
            self.role_combobox.set(user[3])
        else:
            showinfo("جستجو", "کاربر یافت نشد")

    def save_click(self):
        id = self.id_txt.get()
        name = self.name_txt.get()
        family = self.family_txt.get()
        role = self.role_combobox.get()

        u_c = Users_controller()
        result = u_c.save(id, name, family, role)

        if result["status"] == "error":
            showerror("خطا", result["message"])
        else:
            showinfo("ذخیره", result["message"])

            users = u_c.find_all()
            self.table.set_items(users)
            self.clear()

    def edit_click(self):
        id = self.id_txt.get()
        name = self.name_txt.get()
        family = self.family_txt.get()
        role = self.role_combobox.get()

        u_c = Users_controller()
        u_c.edit(id, name, family, role)
        showinfo("edit", "اطلاعات ویرایش شد")

        users = u_c.find_all()
        self.table.set_items(users)
        self.clear()

    def remove_click(self):
        if askyesno("remove", "آیا مطمئن هستید؟"):
            id = int(self.id_txt.get())
            u_c = Users_controller()
            u_c.remove(id)
            showinfo("remove", "اطلاعات حذف شد")

            self.clear()
            user_list = u_c.find_all()
            self.table.set_items(user_list)

    def exit_click(self):
        if askyesno("exit", "آیا برای خروج مطمئن هستید؟"):
            self.win.destroy()
