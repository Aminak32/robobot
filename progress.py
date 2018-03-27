import sys, threading

import time
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import QThread

from progressDialog import Ui_progressDialog


class ProgressProgram(Ui_progressDialog):
    def __init__(self, dialog):
        Ui_progressDialog.__init__(self)
        self.setupUi(dialog)


class ProgressProgramOperation(QThread):
    def __init__(self):
        QThread.__init__(self)


    def __del__(self):
        self.wait()


    def run(self):
        self.showProgressProcess()


    def showProgressProcess(self):
        self.progressDialog = QtWidgets.QDialog()
        self.progressDialogProgram = ProgressProgram(self.progressDialog)
        self.progressDialog.show()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    app.setWindowIcon(QtGui.QIcon("robobot-icon.png"))
    dialog = QtWidgets.QDialog()
    progressProg = ProgressProgram(dialog)
    dialog.show()
    sys.exit(app.exec_())