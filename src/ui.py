import tkinter
import sqlite3
from UserDao import UserDao


class UI(tkinter.Tk):

    def __init__(self, userDao):
        super().__init__()
        self.title("Test")
        self.userDao = userDao
        self.user = None
        self.showLoginBox()

    def showLoginBox(self):
        if not self.user:
            loginBox = LoginBox(self.userDao)
            self.wait_window(loginBox)
            print(loginBox.user)


    # 用户登录逻辑
    def loginLogic(self, name, password):
        user = self.userDao.find_user(name, password)
        if user:
            print(user)
        else:
            print("用户名或密码错误")


class LoginBox(tkinter.Toplevel):

    def __init__(self, userDao):
        super().__init__()
        self.userDao = userDao
        self.title('登录')
        self.setUI()
        self.resizable(0, 0)
        self.user = {}

    def setUI(self):
        row1 = tkinter.Frame(self)
        row1.grid(row=0)
        tkinter.Label(row1, text='用户名', width=8).grid(row=0, column=0)
        self.name = tkinter.StringVar()
        tkinter.Entry(row1, textvariable = self.name, width=20).grid(row=0, column=1)

        row2 = tkinter.Frame(self)
        row2.grid(row=1)
        tkinter.Label(row2, text='密码 ', width=8).grid(row=0, column=0)
        self.password = tkinter.StringVar()
        tkinter.Entry(row2, textvariable=self.password, show='*', width=20).grid(row=0, column=1)

        row3 = tkinter.Frame(self)
        row3.grid(row=2)
        tkinter.Button(row3, text='登录', command=self.login).grid()
        # 将登录窗口置于最前
        self.wm_attributes("-topmost", 1)

    def login(self):
        user = self.userDao.find_user(self.name.get(), self.password.get())
        print(user)
        if user:
            self.user = user
            self.destroy()
        else:
            print('用户名或密码不正确')



def main():
    conn = sqlite3.connect('JiuYe.db')
    userDao = UserDao(conn)
    ui = UI(userDao)
    ui.mainloop()


if __name__ == '__main__':
    main()
