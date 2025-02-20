from tkinter import *
from tkinter.ttk import *
from view.sign_up import Sign_up_UI
from view.sign_in import Sign_in_UI


def type_text(label, text, index=0):
    if index <= len(text):
        label.config(text=text[:index])
        index += 1
        label.after(70, type_text, label, text, index)
        
class Mainui :
    def __init__(self):
        self.win_loggin = Tk()
        self.win_loggin.title("azmoon yar")
        self.win_loggin.geometry("300x200")
        self.win_loggin.resizable(False, False)
        self.win_loggin.iconbitmap("exam.ico")
        self.win_loggin.configure(bg="#2471a3")

        self.label = Label(self.win_loggin, text="", anchor="e", justify="right", foreground="white", background="#2471a3", font=("B Koodak", 14))
        self.label.pack(pady=5)

        type_text(self.label, "به آزمونیار خوش اومدین")

        b1 = Button(self.win_loggin,text="ورورد",width=10,command=self.sign_in)
        b1.pack(pady=5)
        b2 = Button(self.win_loggin, text="ثبت نام", width=10, command=self.sign_up)
        b2.pack(pady=5)

        self.win_loggin.mainloop()
        
    def sign_up(self):
        self.win_loggin.destroy()
        Sign_up_UI()

    def sign_in(self):
        self.win_loggin.destroy()
        Sign_in_UI()
        

Mainui()

