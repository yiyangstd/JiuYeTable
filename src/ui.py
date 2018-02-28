import tkinter


class UI(object):

    def __init__(self):
        self.loginBox = tkinter.Tk()
        self.loginBox.title("登录")

    def showLoginBox(self):
        tkinter.mainloop()

def main():
    ui = UI()
    ui.showLoginBox()

if __name__ == '__main__':
    main()