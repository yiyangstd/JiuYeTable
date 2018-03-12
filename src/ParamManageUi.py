from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon

class ParamManageUi(QDialog):

    def __init__(self, paramDao):
        super().__init__()
        self.paramDao = paramDao
        self.initUI()

    def initUI(self):
        self.setWindowTitle('修改参数')
        self.setWindowIcon(QIcon('icon.jpg'))
        self.setGeometry(200, 200, 600, 500)
        self.grid = QGridLayout()

        self.center()
        self.show()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())