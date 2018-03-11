from ShiYeDetailDAO import ShiYeDetailDao
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon

class DataManageUi(QDialog):

    def __init__(self, shiYeDetailDao):
        super().__init__()
        self.shiYeDetailDao = shiYeDetailDao
        self.initUI()


    def initUI(self):
        self.setWindowTitle('修改数据')
        self.setWindowIcon(QIcon('icon.jpg'))
        self.setGeometry(200, 200, 600, 500)
        self.grid = QGridLayout()
        self.setLayout(self.grid)
        idLabel = QLabel("身份证：")
        self.idText = QLineEdit()
        self.searchButton = QPushButton("查询")
        self.searchButton.clicked.connect(self.search)
        nameLabel = QLabel("姓名：")
        self.nameText = QLineEdit()
        self.nameText.setDisabled(True)
        sexLabel = QLabel("性别：")
        self.sex1 = QRadioButton("男")
        self.sex2 = QRadioButton("女")
        self.sexGroup = QButtonGroup()
        self.sexGroup.addButton(self.sex1, 1)
        self.sexGroup.addButton(self.sex2, 2)
        monthLabel = QLabel("享受月数：")
        self.monthText = QLineEdit()
        self.monthText.setDisabled(True)
        stopLabel = QLabel("终止发放：")
        self.stop = QCheckBox("终止")
        shengyuLabel = QLabel("生育保险：")
        self.shengyu = QCheckBox("下月发放")
        shangzhangLabel = QLabel("丧葬：")
        self.shangzhang = QCheckBox("下月发放")
        self.saveButton = QPushButton("保存")
        self.saveButton.setDisabled(True)

        self.grid.addWidget(idLabel, 0, 0)
        self.grid.addWidget(self.idText, 0, 1, 1, 4)
        self.grid.addWidget(self.searchButton, 0, 5)
        self.grid.addWidget(nameLabel, 1, 0)
        self.grid.addWidget(self.nameText, 1, 1, 1, 4)
        self.grid.addWidget(sexLabel, 2, 0)
        self.grid.addWidget(self.sex1, 2, 1)
        self.grid.addWidget(self.sex2, 2, 2)
        self.grid.addWidget(monthLabel, 3, 0)
        self.grid.addWidget(self.monthText, 3, 1, 1, 4)
        self.grid.addWidget(stopLabel, 4, 0)
        self.grid.addWidget(self.stop, 4, 1)
        self.grid.addWidget(shengyuLabel, 5, 0)
        self.grid.addWidget(self.shengyu, 5, 1)
        self.grid.addWidget(shangzhangLabel, 6, 0)
        self.grid.addWidget(self.shangzhang, 6, 1)
        self.grid.addWidget(self.saveButton, 7, 5)
        self.center()
        self.show()

    def search(self):
        id = self.idText.text()
        if not id:
            QMessageBox.information(self, "提示", "请先输入需要修改的数据的身份证号码")
            return
        user = self.shiYeDetailDao.find_by_id(id)
        if not user:
            QMessageBox.information(self, "提示", "没有找到数据")
            return
        self.nameText.clear()
        self.nameText.insert(user['name'])

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
