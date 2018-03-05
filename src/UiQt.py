import sys
from PyQt5.QtWidgets import (QMainWindow, QDialog, QGridLayout, QPushButton, QLabel, QLineEdit, QDesktopWidget, QApplication)
from PyQt5.QtCore import Qt

class MainUI(QMainWindow):

    def __init__(self):
        super().__init__()
        self.user = None
        self.setGeometry(200, 200, 400, 300)
        self.showLoginBox()
        self.initUI()


    def showLoginBox(self):
        loginBox = LoginBox()
        loginBox.exec_()

    def initUI(self):

        self.center()
        self.show()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())



class LoginBox(QDialog):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(300,300,200,200)
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
        grid.addWidget(nameLabel, 0, 0)
        grid.addWidget(self.nameLineEdit, 0, 1, 1, 2)
        grid.addWidget(passwdLabel, 1, 0)
        grid.addWidget(self.passLineEdit, 1, 1, 1, 2)
        grid.addWidget(button, 2, 2)
        self.center()
        self.show()

    def login(self):
        print("登录")

    # 将登录窗口移动到中心
    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    box = MainUI()
    app.exit(app.exec_())