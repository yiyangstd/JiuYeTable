from ShiYeDetailDAO import ShiYeDetailDao
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
import datetime

class DataManageUi(QDialog):

    def __init__(self, shiYeDetailDao):
        super().__init__()
        self.shiYeDetailDao = shiYeDetailDao
        self.initUI()
        self.id = None


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
        zhanghaoLabel = QLabel("银行账号：")
        self.zhanghao = QLineEdit()
        self.zhanghao.setDisabled(True)
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
        self.saveButton.clicked.connect(self.saveData)

        self.grid.addWidget(idLabel, 0, 0)
        self.grid.addWidget(self.idText, 0, 1, 1, 4)
        self.grid.addWidget(self.searchButton, 0, 5)
        self.grid.addWidget(nameLabel, 1, 0)
        self.grid.addWidget(self.nameText, 1, 1, 1, 4)
        self.grid.addWidget(sexLabel, 2, 0)
        self.grid.addWidget(self.sex1, 2, 1)
        self.grid.addWidget(self.sex2, 2, 2)
        self.grid.addWidget(zhanghaoLabel, 3, 0)
        self.grid.addWidget(self.zhanghao, 3, 1, 1, 4)
        self.grid.addWidget(monthLabel, 4, 0)
        self.grid.addWidget(self.monthText, 4, 1, 1, 4)
        self.grid.addWidget(stopLabel, 5, 0)
        self.grid.addWidget(self.stop, 5, 1)
        self.grid.addWidget(shengyuLabel, 6, 0)
        self.grid.addWidget(self.shengyu, 6, 1)
        self.grid.addWidget(shangzhangLabel, 7, 0)
        self.grid.addWidget(self.shangzhang, 7, 1)
        self.grid.addWidget(self.saveButton, 8, 5)
        self.center()
        self.show()

    def search(self):
        id = self.idText.text().strip()
        self.id = id
        if not id:
            QMessageBox.information(self, "提示", "请先输入需要修改的数据的身份证号码")
            return
        user = self.shiYeDetailDao.find_by_id(id)
        if not user:
            QMessageBox.information(self, "提示", "没有找到数据")
            return
        print(user)
        self.nameText.clear()
        self.nameText.insert(str(user['name']))
        self.nameText.setEnabled(True)
        if user['sex'] == '男':
            self.sex1.setChecked(True)
            self.sex2.setChecked(False)
        else:
            self.sex1.setChecked(False)
            self.sex2.setChecked(True)
        self.monthText.clear()
        self.monthText.insert(str(user['month']))
        self.zhanghao.clear()
        self.zhanghao.insert(str(user['zhanghao']))
        self.zhanghao.setEnabled(True)
        if user['stopFlag'] == 0:
            self.stop.setChecked(False)
        else:
            self.stop.setChecked(True)
        if user['shangzhangFlag'] == self.getNetMonth():
            self.shangzhang.setChecked(True)
        else:
            self.shangzhang.setChecked(False)
        if user['shengyuFlag'] == self.getNetMonth():
            self.shengyu.setChecked(True)
        else:
            self.shengyu.setChecked(False)
        if user['id'] and self.id:
            self.saveButton.setEnabled(True)

    def saveData(self):
        if not self.idText.text().strip() or not self.zhanghao.text().strip():
            QMessageBox.information(self, '警告', '请输入完整数据')
            return
        id = self.idText.text().strip()
        stopFlag = None
        if self.stop.isChecked():
            stopFlag = 1
        else:
            stopFlag = 0
        zhanghao = self.zhanghao.text().strip()
        shangzhang = None
        if self.shangzhang.isChecked():
            shangzhang = self.getNetMonth()
        shengyu = None
        if self.shengyu.isChecked():
            shengyu = self.getNetMonth()
        saveResult = self.shiYeDetailDao.update_person_by_id(id=str(self.id), newId=id, name=self.nameText.text().strip(),
                                                             stopFlag=stopFlag, shangzhangFlag=shangzhang, shengyuFlag=shengyu,
                                                             zhanghao=zhanghao)
        if saveResult:
            QMessageBox.information(self, '成功', '保存数据成功')
        else:
            QMessageBox.information(self, '失败', '保存数据失败')


    def getNetMonth(self):
        year = datetime.datetime.now().year
        month = datetime.datetime.now().month
        if str(month) == '12':
            year = str(int(year) + 1)
            month = '1'
        else:
            month = str(int(month) + 1)
        return int(str(year) + str(month))

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
