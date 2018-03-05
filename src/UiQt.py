import sys
import sqlite3
from UserDao import UserDao
from PyQt5.QtWidgets import (QMainWindow,QWidget, QDialog, QGridLayout, QPushButton, QLabel, QLineEdit, QDesktopWidget, QMessageBox, QApplication)
from PyQt5.QtCore import Qt

class MainUI(QWidget):

    def __init__(self, userDao):
        super().__init__()
        self.userDao = userDao
        self.user = None
        self.showLoginBox()
        # if self.user:
        self.initUI()


    def showLoginBox(self):
        loginBox = LoginBox(self.userDao)
        loginBox.exec_()
        self.user = loginBox.user

    def initUI(self):
        self.setGeometry(200, 200, 1000, 800)
        self.center()
        grid = QGridLayout()
        self.setLayout(grid)
        self.filePathText = QLineEdit("")
        self.openButon = QPushButton("打开")
        grid.addWidget(self.filePathText, 0, 0)
        grid.addWidget(self.openButon, 0, 3)

        self.show()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())



class LoginBox(QDialog):
    def __init__(self, userDao):
        super().__init__()
        self.userDao = userDao
        self.user = None
        self.initUI()

    def initUI(self):
        self.setGeometry(300,300,250,100)
        self.setWindowTitle("登录")
        grid = QGridLayout()
        self.setLayout(grid)
        nameLabel = QLabel("姓名:")
        self.nameLineEdit = QLineEdit("")
        passwdLabel = QLabel("密码:")
        self.passLineEdit = QLineEdit("")

        # 密码窗口禁止右键菜单
        self.passLineEdit.setContextMenuPolicy(Qt.NoContextMenu)
        # 密码框输入返显
        self.passLineEdit.setEchoMode(QLineEdit.Password)
        button = QPushButton("登录")
        button.clicked.connect(self.login)
        grid.addWidget(nameLabel, 0, 0)
        grid.addWidget(self.nameLineEdit, 0, 1, 1, 2)
        grid.addWidget(passwdLabel, 1, 0)
        grid.addWidget(self.passLineEdit, 1, 1, 1, 2)
        grid.addWidget(button, 2, 2)
        self.center()
        self.show()

    def login(self):
        self.user = self.userDao.find_user(self.nameLineEdit.text(), self.passLineEdit.text())
        if self.user:
            self.destroy()
        else:
            QMessageBox.information(self, "登录失败", "用户名或密码错误，\n请检查后重新登录")

    # 将登录窗口移动到中心
    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    conn = sqlite3.connect('JiuYe.db')
    userDao = UserDao(conn)
    box = MainUI(userDao)
    app.exit(app.exec_())