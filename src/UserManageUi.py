from PyQt5.QtWidgets import QDialog, QGridLayout, QDesktopWidget, QTableView, QPushButton, QAbstractItemView
from PyQt5.QtGui import QIcon
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from role import Role

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
        self.tableView = QTableView()
        self.tableView.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tableView.setEditTriggers(QAbstractItemView.NoEditTriggers)
        grid.addWidget(self.tableView, 0, 0, 7, 3)

        self.addButton = QPushButton("增加用户")
        self.deleteButton = QPushButton("删除用户")
        self.deleteButton.clicked.connect(self.deleteUser)
        self.resetButton = QPushButton("重置密码")
        grid.addWidget(self.addButton, 0, 4)
        grid.addWidget(self.deleteButton, 1, 4)
        grid.addWidget(self.resetButton, 2, 4)
        self.refreshTable()

        self.show()

    def deleteUser(self):
        index = self.tableView.selectedIndexes()
        print(index)

    def refreshTable(self):
        datas = self.userDao.find_all_user()
        users = []
        for data in datas:
            users.append([data['name'], data['role']])
        headers = ['用户名', '角色']
        model = QStandardItemModel()
        model.setHorizontalHeaderLabels(headers)
        for xindex, row in enumerate(users):
            for yindex, column in enumerate(headers):
                item = QStandardItem(str(users[xindex][yindex]))
                model.setItem(xindex, yindex, item)
        self.tableView.setModel(model)

    # 将登录窗口移动到中心
    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

