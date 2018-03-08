from PyQt5.QtWidgets import QDialog, QGridLayout, QDesktopWidget
from PyQt5.QtGui import QIcon

class UserManageBox(QDialog):

    def __init__(self, userDao):
        super().__init__()
        self.userDao = userDao
        self.initUI()

    def initUI(self):
        self.setGeometry(300, 300, 500, 400)
        self.setWindowIcon(QIcon('icon.jpg'))
        self.setWindowTitle("用户管理")
        self.center()
        grid = QGridLayout()
        self.setLayout(grid)

        self.show()

    # 将登录窗口移动到中心
    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())