import sys
from PyQt5 import QtWidgets, QtGui

from loginDialog import Ui_loginDialog
from mainApp import MainAppProgram


class LoginProgram(Ui_loginDialog):
    def __init__(self, dialog):
        Ui_loginDialog.__init__(self)
        self.setupUi(dialog)

        self.loginButton.clicked.connect(self.loginSubmit)

    def loginSubmit(self):
        username = self.usernameLineEdit.text()
        password = self.passwordLineEdit.text()
        if username != "test":
            self.loginMsgLabel.setText("Username is wrong")
        elif password != "test123":
            self.loginMsgLabel.setText("Password is wrong")
        else:
            dialog.close()
            self.window = QtWidgets.QMainWindow()
            self.mainAppWindow = MainAppProgram(self.window)
            self.window.show()

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    app.setWindowIcon(QtGui.QIcon("robobot-icon.png"))
    dialog = QtWidgets.QDialog()
    loginProg = LoginProgram(dialog)
    dialog.show()
    sys.exit(app.exec_())