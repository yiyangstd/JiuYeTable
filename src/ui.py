import tkinter
import sqlite3
from UserDao import UserDao

class UI(object):

    def __init__(self, userDao):
        self.userDao = userDao
        self.loginBox = tkinter.Tk()
        self.loginBox.title("登录")

    def showLoginBox(self):
        tkinter.mainloop()

    #用户登录逻辑
    def loginLogic(self, name, password):
        user = self.userDao.find_user(name, password)
        if user:
            print(user)
        else:
            print("用户名或密码错误")

def main():
    conn = sqlite3.connect('JiuYe.db')
    userDao = UserDao(conn)
    ui = UI(userDao)
    # ui.showLoginBox()
    ui.loginLogic("yangyi", "123213")
    # print(userDao.add_user("yangyi","123213","admin"))

if __name__ == '__main__':
    main()