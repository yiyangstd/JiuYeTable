import tkinter
import sqlite3
import tkinter.filedialog
from UserDao import UserDao
from tkinter.scrolledtext import ScrolledText
from tkinter.ttk import Treeview, Scrollbar


class UI(tkinter.Tk):

    def __init__(self, userDao):
        super().__init__()
        self.title("失业人员保险自动计算工具")
        self.userDao = userDao
        self.protocol('WM_DELETE_WINDOW', self.closeWindow)
        self.user = None
        self.loginBox = None
        self.inputFilePath = None
        screenwidth = self.winfo_screenwidth()
        screenheight = self.winfo_screenheight()
        self.geometry('%dx%d+%d+%d' % (1200, 700, (screenwidth - 1200) / 2, (screenheight - 700) / 2))
        # self.showLoginBox()
        # if not self.user:
        #     return
        frame1 = tkinter.Frame(self, padx=10, pady=10, width=1200, height=100)
        frame1.grid(row=0, column=0)
        self.fileEntry = tkinter.Text(frame1, font=("Arial, 16"), state='disabled', height=1, width=95, bd=2)
        self.fileEntry.grid(row=0, column=0)
        tkinter.Frame(frame1, width=8).grid(row=0, column=1)
        fileButton = tkinter.Button(frame1, font=("Arial, 15"), text="打开", command=self.openFile)
        fileButton.grid(row=0, column=2)
        tkinter.Frame(frame1, width=8).grid(row=0, column=3)
        self.inputButton = tkinter.Button(frame1, font=("Arial, 15"), text="导入", state='disabled', command=self.inputFile)
        self.inputButton.grid(row=0, column=4)
        frame2 = tkinter.Frame(self, padx=10, width=1055, height=630, bg='red')
        frame2.grid(row=1, column=0, sticky='W')
        frame3 = tkinter.Frame(self, padx=10, width=145, height=630, bg='blue')
        frame3.grid(row=1, column=0, sticky='E')

        # self.showBox = ScrolledText(frame2, font=("Arial, 12"), width=127, height=38)
        # self.showBox.grid(row=0, column=0)

        # columns = ('c1', 'c2', 'c3', 'c4', 'c5', 'c6', 'c7', 'c8', 'c9', 'c10'
        #            'c11', 'c12', 'c13', 'c14', 'c15', 'c16')
        columns = ('c1', 'c2', 'c3', 'c4', 'c5')
        self.table = Treeview(frame2, columns=columns, height=30, show="headings")
        ysb = Scrollbar(frame2, orient="vertical", command=self.table.yview())
        xsb = Scrollbar(frame2, orient="horizontal", command=self.table.xview())
        self.table.configure(yscroll=ysb.set, xscroll=xsb.set)
        self.table.grid(row=0, column=0)
        ysb.grid(row=0, column=1, sticky="ns")
        xsb.grid(row=1, column=0, sticky="ew")
        for i in range(100):
            self.table.insert('', i, values=[str(i)] * 6)



        # 关闭主窗口相应事件
    def closeWindow(self):
        print("close")
        if self.loginBox:
            self.loginBox.destroy()
        self.destroy()

    # 显示登录框
    def showLoginBox(self):
        if not self.user:
            loginBox = LoginBox(self.userDao)
            self.loginBox = loginBox
            self.wait_window(loginBox)
            print(loginBox.user)
            if loginBox.user:
                self.user = loginBox.user
            else:
                self.destroy()

    # 打开按钮相应事件
    def openFile(self):
        fileName = tkinter.filedialog.askopenfilename(filetypes=[("excel", "*.xls")])
        self.fileEntry['state'] = tkinter.NORMAL
        self.fileEntry.delete('0.0', tkinter.END)
        self.fileEntry.insert(0.0, fileName)
        self.inputFilePath = fileName
        self.fileEntry['state'] = tkinter.DISABLED
        if self.inputFilePath:
            self.inputButton['state'] = tkinter.NORMAL
        else:
            self.inputButton['state'] = tkinter.DISABLED

    # 导入excel
    def inputFile(self):
        if self.inputFilePath:
            print(self.inputFilePath)

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
        tkinter.Entry(row1, textvariable=self.name, width=20).grid(row=0, column=1)

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

        screenwidth = self.winfo_screenwidth()
        screenheight = self.winfo_screenheight()
        size = '%dx%d+%d+%d' % (220, 80, (screenwidth - 220) / 2, (screenheight - 80) / 2)
        self.geometry(size)


    def login(self):
        user = self.userDao.find_user(self.name.get(), self.password.get())
        print(user)
        if user:
            self.user = user
            self.destroy()


def main():
    conn = sqlite3.connect('JiuYe.db')
    userDao = UserDao(conn)
    ui = UI(userDao)
    ui.mainloop()


if __name__ == '__main__':
    main()
