import sys
from PyQt5 import QtWidgets, QtGui
from aboutDialog import Ui_aboutDialog


class AboutProgram(Ui_aboutDialog):

    def __init__(self, dialog):
        Ui_aboutDialog.__init__(self)
        self.setupUi(dialog)
        self.dialog = dialog

        self.aboutOkButton.clicked.connect(self.closeAboutProgram)

    def closeAboutProgram(self):
        self.dialog.close()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    app.setWindowIcon(QtGui.QIcon("robobot-icon.png"))
    dialog = QtWidgets.QDialog()
    aboutProg = AboutProgram(dialog)
    dialog.show()
    sys.exit(app.exec_())