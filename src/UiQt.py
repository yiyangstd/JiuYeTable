import sys
import logging
import sqlite3
import datetime
from UserDao import UserDao
from ShiYeDetailDAO import ShiYeDetailDao
from PyQt5.QtWidgets import (QFileDialog, QWidget, QDialog, QGridLayout, QPushButton, QLabel, QLineEdit, QDesktopWidget, QMessageBox, QApplication, QTableView, QAbstractItemView)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QIcon
from ExcelParser import ExcelParser
from ExcelSaver import ExcelSaver
from role import Role
from UserManageUi import UserManageBox
from DataManageUi import DataManageUi

class MainUI(QWidget):

    def __init__(self, userDao, shiYeDetailDao):
        super().__init__()
        self.userDao = userDao
        self.shiYeDetailDao = shiYeDetailDao
        self.user = None
        self.data = None
        self.item = None
        self.showLoginBox()
        print(self.user)
        # if self.user:
        self.initUI()


    def showLoginBox(self):
        loginBox = LoginBox(self.userDao)
        loginBox.exec_()
        self.user = loginBox.user

    def initUI(self):
        self.setWindowTitle('江阳区就业局失业金发放工具（测试版1.0）')
        self.setWindowIcon(QIcon('icon.jpg'))
        self.setGeometry(200, 200, 1000, 800)
        self.center()
        self.grid = QGridLayout()
        self.setLayout(self.grid)
        self.filePathText = QLineEdit("")
        self.openButton = QPushButton("打开")
        self.uploadButton = QPushButton("上传")
        self.openButton.clicked.connect(self.openFile)
        self.uploadButton.clicked.connect(self.uploadFile)
        self.filePathText.setDisabled(True)
        self.uploadButton.setDisabled(True)
        self.grid.addWidget(self.filePathText, 0, 0)
        self.grid.addWidget(self.openButton, 0, 3)
        self.grid.addWidget(self.uploadButton, 0, 4)

        self.headers = ['姓名', '性别', '身份证', '享受月数', '参保时间', '开始发放时间', '结束时间',
                        '失业', '医疗', '生育', '丧葬', '合计', '村社', '账号', '银行']
        datas = []
        self.tableView = QTableView()
        self.tableView.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableMode = self.buildTable(self.headers, datas)
        self.tableView.setModel(self.tableMode)
        self.grid.addWidget(self.tableView, 1, 0, 24, 1)
        if self.user:
            userNameLable = QLabel('用户:' + self.user['name'])
            self.grid.addWidget(userNameLable, 25, 0, 1, 1)

        self.insertButton = QPushButton("存储")
        self.insertButton.setDisabled(True)
        self.insertButton.clicked.connect(self.insertData)
        self.grid.addWidget(self.insertButton, 1, 3, 1, 2)

        self.queryButton = QPushButton("查询")
        self.queryButton.clicked.connect(self.queryData)
        self.grid.addWidget(self.queryButton, 2, 3, 1, 2)

        self.outputButton = QPushButton("导出")
        self.outputButton.clicked.connect(self.outputFile)
        self.grid.addWidget(self.outputButton, 3, 3, 1, 2)

        self.zhichuButton = QPushButton("本月支出")
        self.zhichuButton.clicked.connect(self.expend)
        self.grid.addWidget(self.zhichuButton, 4, 3, 1, 2)

        self.changePasswdButton = QPushButton("修改密码")
        self.changePasswdButton.clicked.connect(self.changePassWd)
        self.grid.addWidget(self.changePasswdButton, 5, 3, 1, 2)

        self.updateDataButton = QPushButton("修改数据")
        self.grid.addWidget(self.updateDataButton, 6, 3, 1, 2)
        self.updateDataButton.clicked.connect(self.manageData)

        self.paramButton = QPushButton("参数管理")
        self.grid.addWidget(self.paramButton, 7, 3, 1, 2)
        self.paramButton.clicked.connect(self.manageParam)

        self.userButton = QPushButton("用户管理")
        if self.user and self.user['role'] == Role.ADMIN.value:
            self.userButton.setEnabled(True)
        else:
            self.userButton.setDisabled(True)
        self.userButton.clicked.connect(self.manageUser)
        self.grid.addWidget(self.userButton, 8, 3, 1, 2)

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
            self.item = parser.item
            self.data = data
        except Exception as e:
            QMessageBox.information(self, "错误", "导入的文件格式错误，请根据模板检查并修改后重新导入")
            self.insertButton.setEnabled(False)
            return
        self.tableView.setModel(self.buildTable(self.headers, data))
        self.insertButton.setEnabled(True)

    def insertData(self):
        self.insertButton.setDisabled(True)
        failData = []
        successData = []
        for row in self.data:
            if self.shiYeDetailDao.add_person(row[0], row[1], row[2], row[3], row[4],
                                          row[5], row[6], row[7], row[8], row[9],
                                          row[10], row[11], row[12], row[13], row[14],
                                          self.item):
                successData.append(row[0])
            else:
                failData.append(row[0])

        self.insertButton.setDisabled(True)
        if failData:
            info = ''
            for data in failData:
                info = info + data + ','
            QMessageBox.information(self, '存储完成', info + '存储失败，请检查')
        else:
            QMessageBox.information(self, '存储完成', '存储完成')

    # 查询数据
    def queryData(self):
        all_data = self.shiYeDetailDao.find_persons()
        if not all_data:
            return
        headers = ['姓名', '性别', '身份证', '享受月数', '参保时间', '开始发放时间', '结束时间',
                   '失业', '医疗', '生育', '丧葬', '合计', '村社', '账号', '银行', '项目']
        tableDatas = []
        for data in all_data:
            tableData = [data['name'], data['sex'], data['id'], data['month'], data['canbaoTime'],
                         data['fafangTime'], data['endTime'], data['shiye'], data['yiliao'],
                         data['shengyu'], data['shangzhang'], data['total'], data['cunse'], data['zhanghao'],
                         data['beizhu'], data['item']]
            tableDatas.append(tableData)

        tableMode = self.buildTable(headers, tableDatas)
        self.tableView.setModel(tableMode)

    # 导出数据
    def outputFile(self):
        all_data = self.shiYeDetailDao.find_persons()
        if not all_data:
            QMessageBox.information(self, '提示', '没有数据可以导出')
            return
        filename = QFileDialog.getSaveFileName(self, '选择你要保存的文件位置', '/', '*.xls')
        if not filename or not filename[0]:
            return
        headers = ['姓名', '性别', '身份证', '享受月数', '参保时间', '开始发放时间', '结束时间',
                   '失业', '医疗', '生育', '丧葬', '合计', '村社', '账号', '银行', '项目']
        tableDatas = []
        for data in all_data:
            tableData = [data['name'], data['sex'], data['id'], data['month'], data['canbaoTime'],
                         data['fafangTime'], data['endTime'], data['shiye'], data['yiliao'],
                         data['shengyu'], data['shangzhang'], data['total'], data['cunse'], data['zhanghao'],
                         data['beizhu'], data['item']]
            tableDatas.append(tableData)
        ExcelSaver.saveFile(filename[0], headers, tableDatas)

    # 修改密码
    def changePassWd(self):
        passwdChangeBox = PasswdChangeBox(self.userDao, self.user['name'])
        passwdChangeBox.exec_()

    def manageData(self):
        dataManageBox = DataManageUi(self.shiYeDetailDao)
        dataManageBox.exec_()

    def manageParam(self):
        print("参数管理")

    # 管理用户
    def manageUser(self):
        userManageBox = UserManageBox(self.userDao)
        userManageBox.exec_()

    # 当月支出
    def expend(self):
        all_data = self.shiYeDetailDao.find_persons(stopFlag=0)
        if not all_data:
            QMessageBox.information(self, '提示', '数据库中没有数据，请先导入数据或检查数据库')
            return

        filename = QFileDialog.getSaveFileName(self, '选择你要保存的文件位置', '/', '*.xls')
        if not filename or not filename[0]:
            return
        now_year = datetime.datetime.year
        now_month = datetime.datetime.month
        now_time = str(now_year) + '.' + str(now_month)
        expendDatas = []
        for data in all_data:
            endTime = data['endTime']
            if float(endTime) >= float(now_time) and data['stopFlag'] != 1:
                expendDatas.append(data)


# 登录窗口
class LoginBox(QDialog):
    def __init__(self, userDao):
        super().__init__()
        self.userDao = userDao
        self.user = None
        self.initUI()

    def initUI(self):
        self.setGeometry(300,300,200,100)
        self.setWindowIcon(QIcon('icon.jpg'))
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


# 修改密码窗口
class PasswdChangeBox(QDialog):

    def __init__(self, userDao, userName):
        super().__init__()
        self.userDao = userDao
        self.userName = userName
        self.initUI()


    def initUI(self):
        self.setGeometry(300, 300, 300, 200)
        self.setWindowIcon(QIcon('icon.jpg'))
        self.setWindowTitle("密码修改")
        grid = QGridLayout()
        self.setLayout(grid)
        self.oldPasswdLabel = QLabel("原密码：")
        self.oldPasswdLine = QLineEdit()
        self.oldPasswdLine.setEchoMode(QLineEdit.Password)
        self.newPasswdLabel = QLabel("新密码：")
        self.newPasswdLine = QLineEdit()
        self.newPasswdLine.setEchoMode(QLineEdit.Password)
        self.comfirmPasswdLabel = QLabel("确认密码：")
        self.comfirmPasswdLine = QLineEdit()
        self.comfirmPasswdLine.setEchoMode(QLineEdit.Password)
        self.okButton = QPushButton("确定")
        self.okButton.clicked.connect(self.changePasswd)
        grid.addWidget(self.oldPasswdLabel, 0, 0)
        grid.addWidget(self.oldPasswdLine, 0, 1, 1, 2)
        grid.addWidget(self.newPasswdLabel, 1, 0)
        grid.addWidget(self.newPasswdLine, 1, 1, 1, 2)
        grid.addWidget(self.comfirmPasswdLabel, 2, 0)
        grid.addWidget(self.comfirmPasswdLine, 2, 1, 1, 2)
        grid.addWidget(self.okButton, 3, 2, 1, 1)

        self.center()
        self.show()

    def changePasswd(self):
        if not self.oldPasswdLine.text().strip():
            QMessageBox.information(self, '提示', '请输入原密码')
            return
        if not self.newPasswdLine.text().strip():
            QMessageBox.information(self, '提示', '请输入新密码')
            return
        if not self.comfirmPasswdLine.text().strip():
            QMessageBox.information(self, '提示', '请再次输入新密码')
            return
        if self.newPasswdLine.text() != self.comfirmPasswdLine.text():
            QMessageBox.information(self, '提示', '两次输入的密码不一致')
            return

        if self.userDao.modify_user_password(self.userName, self.oldPasswdLine.text().strip(),
                                             self.newPasswdLine.text().strip()):
            QMessageBox.information(self, '修改密码', '修改密码成功')
        else:
            QMessageBox.information(self, '修改密码', '修改密码失败')
        self.destroy()


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
    shiYeDetailDao = ShiYeDetailDao(conn)
    box = MainUI(userDao, shiYeDetailDao)
    app.exit(app.exec_())