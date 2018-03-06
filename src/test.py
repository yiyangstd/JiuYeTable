# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys
class myDialog(QDialog):
    """docstring for myDialog"""
    def __init__(self, arg=None):
        super(myDialog, self).__init__(arg)
        self.setWindowTitle("first window")
        self.setWindowFlags(Qt.WindowMaximizeButtonHint|Qt.WindowMinimizeButtonHint|Qt.WindowCloseButtonHint)
        self.resize(500,300);
        self.model=QStandardItemModel(4,4);
        self.model.setHorizontalHeaderLabels(['标题1','标题2','标题3','标题4','标题1','标题2','标题3','标题4'])
        for row in range(8):
            for column in range(8):
                item = QStandardItem("row %s, column %s"%(row,column))
                self.model.setItem(row, column, item)
        self.tableView=QTableView();
        self.tableView.setModel(self.model)
        #下面代码让表格100填满窗口
        #self.tableView.horizontalHeader().setStretchLastSection(True)
        #self.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        dlgLayout=QVBoxLayout();
        dlgLayout.addWidget(self.tableView)
        self.tableView.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.setLayout(dlgLayout)
app = QApplication(sys.argv)
#全局设置QPushButton的背景样式
dlg = myDialog()
dlg.show()
dlg.exec_()
app.exit()