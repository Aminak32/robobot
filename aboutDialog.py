# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'aboutDialog.ui'
#
# Created by: PyQt5 UI code generator 5.10
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QPixmap


class Ui_aboutDialog(object):
    def setupUi(self, aboutDialog):
        aboutDialog.setObjectName("aboutDialog")
        aboutDialog.setWindowModality(QtCore.Qt.NonModal)
        aboutDialog.resize(378, 216)
        aboutDialog.setModal(True)
        self.aboutOkButton = QtWidgets.QPushButton(aboutDialog)
        self.aboutOkButton.setGeometry(QtCore.QRect(280, 180, 75, 23))
        self.aboutOkButton.setObjectName("aboutOkButton")
        self.label = QtWidgets.QLabel(aboutDialog)
        self.label.setGeometry(QtCore.QRect(170, 20, 81, 31))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        font.setStrikeOut(False)
        font.setKerning(True)
        font.setStyleStrategy(QtGui.QFont.PreferDefault)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(aboutDialog)
        self.label_2.setGeometry(QtCore.QRect(170, 62, 181, 111))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_2.setFont(font)
        self.label_2.setFrameShadow(QtWidgets.QFrame.Plain)
        self.label_2.setTextFormat(QtCore.Qt.AutoText)
        self.label_2.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.label_2.setWordWrap(True)
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(aboutDialog)
        self.label_3.setGeometry(QtCore.QRect(260, 30, 101, 16))
        self.label_3.setObjectName("label_3")
        self.imageLabel = QtWidgets.QLabel(aboutDialog)
        self.imageLabel.setGeometry(QtCore.QRect(40, 30, 101, 121))
        self.imageLabel.setText("")
        self.imageLabel.setObjectName("imageLabel")

        pixmap = QPixmap('robobot-icon.png')
        self.imageLabel.setPixmap(pixmap)

        self.retranslateUi(aboutDialog)
        QtCore.QMetaObject.connectSlotsByName(aboutDialog)

    def retranslateUi(self, aboutDialog):
        _translate = QtCore.QCoreApplication.translate
        aboutDialog.setWindowTitle(_translate("aboutDialog", "About RoboBot"))
        self.aboutOkButton.setText(_translate("aboutDialog", "OK"))
        self.label.setText(_translate("aboutDialog", "RoboBot"))
        self.label_2.setText(_translate("aboutDialog", "RoboBot is craiglist auto post robot.\n"
"\n"
"Developer: Abdullah Al Arafat\n"
"Cell:+8801712192445\n"
"Email: imbipul9@gmail.com"))
        self.label_3.setText(_translate("aboutDialog", "Version: 2.1.0"))


# if __name__ == "__main__":
#     import sys
#     app = QtWidgets.QApplication(sys.argv)
#     aboutDialog = QtWidgets.QDialog()
#     ui = Ui_aboutDialog()
#     ui.setupUi(aboutDialog)
#     aboutDialog.show()
#     sys.exit(app.exec_())