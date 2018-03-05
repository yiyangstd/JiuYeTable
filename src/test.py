from PyQt5.QtWidgets import *
import sys

class userForm(QDialog):
    def __init__(self, parent = None):
        super(userForm, self).__init__(parent)
        usrName = QLabel("UserName")
        passWd = QLabel("PassWd")
        self.userNameLineEdit = QLineEdit()
        self.passWdLineEdit = QLineEdit()
        self.passWdLineEdit.setEchoMode(QLineEdit.Password)

        gridLayout = QGridLayout()
        gridLayout.addWidget(usrName, 0, 0, 1, 1)
        gridLayout.addWidget(passWd, 1, 0, 1, 1)
        gridLayout.addWidget(self.userNameLineEdit,0,1,1,3)
        gridLayout.addWidget(self.passWdLineEdit,1,1,1,3)

        okPushBtn = QPushButton("OK")
        cancelPushBtn = QPushButton("Cancle")
        btnLayout = QHBoxLayout()
        btnLayout.setSpacing(60)
        btnLayout.addWidget(okPushBtn)
        btnLayout.addWidget(cancelPushBtn)

        dlgLayout = QVBoxLayout()
        dlgLayout.setContentsMargins(40,40,40,40)
        dlgLayout.addLayout(gridLayout)
        dlgLayout.addStretch(40)
        dlgLayout.addLayout(btnLayout)
        self.setLayout(dlgLayout)
        self.setWindowTitle("user WinForm")
        self.resize(200,200)

class loginDlg(QDialog):
    def __init__(self, parent = None):
        super(loginDlg, self).__init__(parent)
        usrName = QLabel("UserName")
        passWd = QLabel("PassWd")
        self.userNameLineEdit = QLineEdit()
        self.passWdLineEdit = QLineEdit()
        self.passWdLineEdit.setEchoMode(QLineEdit.Password)

        gridLayout = QGridLayout()
        gridLayout.addWidget(usrName, 0, 0, 1, 1)
        gridLayout.addWidget(passWd, 1, 0, 1, 1)
        gridLayout.addWidget(self.userNameLineEdit,0,1,1,3)
        gridLayout.addWidget(self.passWdLineEdit,1,1,1,3)

        okPushBtn = QPushButton("OK")
        cancelPushBtn = QPushButton("Cancle")
        btnLayout = QHBoxLayout()
        btnLayout.setSpacing(60)
        btnLayout.addWidget(okPushBtn)
        btnLayout.addWidget(cancelPushBtn)

        dlgLayout = QVBoxLayout()
        dlgLayout.setContentsMargins(40,40,40,40)
        dlgLayout.addLayout(gridLayout)
        dlgLayout.addStretch(40)
        dlgLayout.addLayout(btnLayout)
        self.setLayout(dlgLayout)
        okPushBtn.clicked.connect(self.okClicked)
        cancelPushBtn.clicked.connect(self.cancleClicked)
        self.setWindowTitle("Login WinForm")
        self.resize(200,200)

    def okClicked(self):
        if self.userNameLineEdit.text().strip() == "1" and self.passWdLineEdit.text() == "1":
             #loginDlg.hide()
             newForm = userForm()
             newForm.show()

             newForm.exec_()

        else:
            QMessageBox.warning(self,
                                "Warning",
                                "User name or passWord error",
                                QMessageBox.Yes
                                )
            self.userNameLineEdit.clear()
            self.passWdLineEdit.clear()
            self.userNameLineEdit.setFocus()

    def cancleClicked(self):
        QMessageBox.warning(self,
                            "Warning",
                            "your are going to exit",
                            QMessageBox.Yes
                            )

if __name__ == "__main__":
    app = QApplication(sys.argv)
    dlg = loginDlg()
    dlg.show()
    dlg.exec_()
    app.exit()
