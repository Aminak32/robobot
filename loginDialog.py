# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'loginDialog.ui'
#
# Created by: PyQt5 UI code generator 5.10
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

from mainAppWindow import Ui_MainAppWindow


class Ui_loginDialog(object):
    def setupUi(self, loginDialog):
        # for login dialog
        loginDialog.setObjectName("loginDialog")
        loginDialog.resize(378, 251)

        # for username label
        self.usernameLabel = QtWidgets.QLabel(loginDialog)
        self.usernameLabel.setGeometry(QtCore.QRect(36, 76, 100, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.usernameLabel.setFont(font)
        self.usernameLabel.setObjectName("usernameLabel")

        # for username line edit
        self.usernameLineEdit = QtWidgets.QLineEdit(loginDialog)
        self.usernameLineEdit.setGeometry(QtCore.QRect(140, 79, 210, 29))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.usernameLineEdit.setFont(font)
        self.usernameLineEdit.setObjectName("usernameLineEdit")

        # for password line edit
        self.passwordLineEdit = QtWidgets.QLineEdit(loginDialog)
        self.passwordLineEdit.setGeometry(QtCore.QRect(140, 125, 210, 28))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.passwordLineEdit.setFont(font)
        self.passwordLineEdit.setCursor(QtGui.QCursor(QtCore.Qt.IBeamCursor))
        self.passwordLineEdit.setEchoMode(QtWidgets.QLineEdit.Password)
        self.passwordLineEdit.setObjectName("passwordLineEdit")

        # for password label
        self.passwordLabel = QtWidgets.QLabel(loginDialog)
        self.passwordLabel.setGeometry(QtCore.QRect(36, 125, 100, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.passwordLabel.setFont(font)
        self.passwordLabel.setObjectName("passwordLabel")

        # for login submit button
        self.loginButton = QtWidgets.QPushButton(loginDialog)
        self.loginButton.setGeometry(QtCore.QRect(230, 190, 121, 41))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.loginButton.setFont(font)
        self.loginButton.setMouseTracking(True)
        self.loginButton.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.loginButton.setObjectName("loginButton")

        # self.loginButton.clicked.connect(self.loginSubmit)

        # for login message label
        self.loginMsgLabel = QtWidgets.QLabel(loginDialog)
        self.loginMsgLabel.setGeometry(QtCore.QRect(40, 30, 311, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.loginMsgLabel.setFont(font)
        self.loginMsgLabel.setStyleSheet("color: rgb(255, 2, 18);")
        self.loginMsgLabel.setText("")
        self.loginMsgLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.loginMsgLabel.setObjectName("loginMsgLabel")

        self.retranslateUi(loginDialog)
        QtCore.QMetaObject.connectSlotsByName(loginDialog)

    def retranslateUi(self, loginDialog):
        _translate = QtCore.QCoreApplication.translate
        loginDialog.setWindowTitle(_translate("loginDialog", "RoboBot - Login"))
        self.usernameLabel.setText(_translate("loginDialog", "Username:"))
        self.passwordLabel.setText(_translate("loginDialog", "Password:"))
        self.loginButton.setText(_translate("loginDialog", "Login"))


# if __name__ == "__main__":
#     import sys
#     app = QtWidgets.QApplication(sys.argv)
#     loginDialog = QtWidgets.QDialog()
#     ui = Ui_loginDialog()
#     ui.setupUi(loginDialog)
#     loginDialog.show()
#     sys.exit(app.exec_())