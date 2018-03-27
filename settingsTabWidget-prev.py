# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'settingsTabWidget.ui'
#
# Created by: PyQt5 UI code generator 5.10
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QHeaderView


class Ui_settingsTabWidget(object):
    def setupUi(self, settingsTabWidget):
        settingsTabWidget.setObjectName("settingsTabWidget")
        settingsTabWidget.setEnabled(True)
        settingsTabWidget.resize(451, 450)
        self.locationTab = QtWidgets.QWidget()
        self.locationTab.setObjectName("locationTab")
        self.downloadLocGroupBox = QtWidgets.QGroupBox(self.locationTab)
        self.downloadLocGroupBox.setGeometry(QtCore.QRect(10, 20, 421, 91))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.downloadLocGroupBox.setFont(font)
        self.downloadLocGroupBox.setObjectName("downloadLocGroupBox")
        self.downloadLocPushButton = QtWidgets.QPushButton(self.downloadLocGroupBox)
        self.downloadLocPushButton.setGeometry(QtCore.QRect(110, 30, 191, 41))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.downloadLocPushButton.setFont(font)
        self.downloadLocPushButton.setObjectName("downloadLocPushButton")
        settingsTabWidget.addTab(self.locationTab, "")
        self.proxyTab = QtWidgets.QWidget()
        self.proxyTab.setObjectName("proxyTab")
        self.proxyTableWidget = QtWidgets.QTableWidget(self.proxyTab)
        self.proxyTableWidget.setGeometry(QtCore.QRect(10, 130, 421, 281))
        self.proxyTableWidget.setObjectName("tableWidget")
        self.proxyTableWidget.setColumnCount(4)
        # self.proxyTableWidget.setRowCount(0)
        self.proxyTableWidget.setHorizontalHeaderLabels(['IP', 'Port', 'Type', 'Status'])

        self.proxyUploadGroupBox = QtWidgets.QGroupBox(self.proxyTab)
        self.proxyUploadGroupBox.setGeometry(QtCore.QRect(10, 9, 421, 111))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.proxyUploadGroupBox.setFont(font)
        self.proxyUploadGroupBox.setObjectName("proxyUploadGroupBox")
        self.proxyDeletePrevCheckBox = QtWidgets.QCheckBox(self.proxyUploadGroupBox)
        self.proxyDeletePrevCheckBox.setGeometry(QtCore.QRect(30, 40, 151, 21))
        self.proxyDeletePrevCheckBox.setChecked(True)
        self.proxyDeletePrevCheckBox.setObjectName("proxyDeletePrevCheckBox")
        self.proxyUploadPushButton = QtWidgets.QPushButton(self.proxyUploadGroupBox)
        self.proxyUploadPushButton.setGeometry(QtCore.QRect(230, 40, 151, 51))
        self.proxyUploadPushButton.setObjectName("proxyUploadPushButton")
        self.proxyIPVersionComboBox = QtWidgets.QComboBox(self.proxyUploadGroupBox)
        self.proxyIPVersionComboBox.setGeometry(QtCore.QRect(30, 70, 151, 22))
        self.proxyIPVersionComboBox.setObjectName("proxyIPVersionComboBox")
        self.proxyIPVersionComboBox.addItem("Select IP Version", "")
        self.proxyIPVersionComboBox.addItem("Http", "http")
        self.proxyIPVersionComboBox.addItem("Socks 5", "socks5")
        self.proxyIPVersionComboBox.addItem("Socks 4", "socks4")
        settingsTabWidget.addTab(self.proxyTab, "")

        self.retranslateUi(settingsTabWidget)
        settingsTabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(settingsTabWidget)

    def retranslateUi(self, settingsTabWidget):
        _translate = QtCore.QCoreApplication.translate
        settingsTabWidget.setWindowTitle(_translate("settingsTabWidget", "Settings"))
        self.downloadLocGroupBox.setTitle(_translate("settingsTabWidget", "Download Locations"))
        self.downloadLocPushButton.setText(_translate("settingsTabWidget", "Download"))
        settingsTabWidget.setTabText(settingsTabWidget.indexOf(self.locationTab), _translate("settingsTabWidget", "Location"))
        self.proxyUploadGroupBox.setTitle(_translate("settingsTabWidget", "Upload Proxy IP List"))
        self.proxyDeletePrevCheckBox.setText(_translate("settingsTabWidget", "Delete Previous List"))
        self.proxyUploadPushButton.setText(_translate("settingsTabWidget", "Upload"))
        settingsTabWidget.setTabText(settingsTabWidget.indexOf(self.proxyTab), _translate("settingsTabWidget", "Proxy"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    settingsTabWidget = QtWidgets.QTabWidget()
    ui = Ui_settingsTabWidget()
    ui.setupUi(settingsTabWidget)
    settingsTabWidget.show()
    sys.exit(app.exec_())

