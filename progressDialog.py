# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'progressDialog.ui'
#
# Created by: PyQt5 UI code generator 5.10
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap


class Ui_progressDialog(object):
    def setupUi(self, progressDialog):
        progressDialog.setObjectName("progressDialog")
        progressDialog.resize(260, 60)
        progressDialog.setWindowFlags(Qt.WindowTitleHint | Qt.MSWindowsFixedSizeDialogHint | Qt.CustomizeWindowHint | Qt.NoDropShadowWindowHint)
        self.loaderLabel = QtWidgets.QLabel(progressDialog)
        self.loaderLabel.setGeometry(QtCore.QRect(20, 3, 240, 50))
        self.loaderLabel.setText("")
        self.loaderLabel.setObjectName("loaderLabel")

        self.loaderMovie = QtGui.QMovie('ajax-loader.gif')
        self.loaderLabel.setMovie(self.loaderMovie)
        self.loaderMovie.start()

        self.retranslateUi(progressDialog)
        QtCore.QMetaObject.connectSlotsByName(progressDialog)

    def retranslateUi(self, progressDialog):
        _translate = QtCore.QCoreApplication.translate
        progressDialog.setWindowTitle(_translate("progressDialog", "Progress..."))


# if __name__ == "__main__":
#     import sys
#     app = QtWidgets.QApplication(sys.argv)
#     app.setWindowIcon(QtGui.QIcon("robobot-icon.png"))
#     progressDialog = QtWidgets.QDialog()
#     ui = Ui_progressDialog()
#     ui.setupUi(progressDialog)
#     progressDialog.show()
#     sys.exit(app.exec_())