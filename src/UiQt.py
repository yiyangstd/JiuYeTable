import sys
import logging
import sqlite3
from UserDao import UserDao
from ShiYeDetailDAO import ShiYeDetailDao
from PyQt5.QtWidgets import (QFileDialog, QWidget, QDialog, QGridLayout, QPushButton, QLabel, QLineEdit, QDesktopWidget, QMessageBox, QApplication, QTableView, QAbstractItemView)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from ExcelParser import ExcelParser
from role import Role

class MainUI(QWidget):

    def __init__(self, userDao):
        super().__init__()
        self.userDao = userDao
        self.user = None
        self.data = None
        self.showLoginBox()
        print(self.user)
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
        self.openButton = QPushButton("打开")
        self.uploadButton = QPushButton("上传")
        self.openButton.clicked.connect(self.openFile)
        self.uploadButton.clicked.connect(self.uploadFile)
        self.filePathText.setDisabled(True)
        self.uploadButton.setDisabled(True)
        grid.addWidget(self.filePathText, 0, 0)
        grid.addWidget(self.openButton, 0, 3)
        grid.addWidget(self.uploadButton, 0, 4)

        self.headers = ['姓名', '性别', '身份证', '享受月数', '参保时间', '开始发放时间',
                 '失业', '医疗', '生育', '丧葬', '合计', '村社', '账号', '银行']
        datas = []
        self.tableView = QTableView()
        self.tableView.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableMode = self.buildTable(self.headers, datas)
        self.tableView.setModel(self.tableMode)
        grid.addWidget(self.tableView, 1, 0, 6, 1)

        self.insertButton = QPushButton("存储")
        self.insertButton.setDisabled(True)
        self.insertButton.clicked.connect(self.insertData)
        grid.addWidget(self.insertButton, 1, 3, 1, 2)

        self.queryButton = QPushButton("查询")
        self.queryButton.clicked.connect(self.insertData)
        grid.addWidget(self.queryButton, 2, 3, 1, 2)

        self.outputButton = QPushButton("导出")

        grid.addWidget(self.outputButton, 3, 3, 1, 2)

        self.zhichuButton = QPushButton("本月支出")
        grid.addWidget(self.zhichuButton, 4, 3, 1, 2)

        self.userButton = QPushButton("用户管理")
        if self.user and self.user['role'] == Role.ADMIN.value:
            self.userButton.setEnabled(True)
        else:
            self.userButton.setDisabled(True)
        grid.addWidget(self.userButton, 5, 3, 1, 2)

        self.show()

    def buildTable(self, headers, datas):
        model = QStandardItemModel()
        model.setHorizontalHeaderLabels(headers)
        for xindex, row in enumerate(datas):
            for yindex, column in enumerate(headers):
                item = QStandardItem(str(datas[xindex][yindex]))
                model.setItem(xindex, yindex, item)

        print(model.columnCount())
        return model

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def openFile(self):
        fileName = QFileDialog.getOpenFileName(self, "选择你要打开的文件", './', ('电子表格 (*.xls *.XLS)'))
        if fileName[0]:
            self.filePathText.setText(fileName[0])
            self.uploadButton.setEnabled(True)
        else:
            self.filePathText.clear()
            self.uploadButton.setDisabled(True)

    def uploadFile(self):
        parser = ExcelParser()
        try:
            data = parser.computData(self.filePathText.text())
            self.data = data
        except Exception as e:
            QMessageBox.information(self, "错误", "导入的文件格式错误，请根据模板检查并修改后重新导入")
            self.insertButton.setEnabled(False)
            return
        self.tableView.setModel(self.buildTable(self.headers, data))
        self.insertButton.setEnabled(True)

    def insertData(self):
        for row in self.data:
            try:
                print('todo')
            except Exception as e:
                print(e)

        self.insertButton.setDisabled(True)
        print("insert")




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