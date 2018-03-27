import json
import sys

from PyQt5 import QtWidgets, QtGui, QtCore
from about import AboutProgram
from mainAppWindow import Ui_MainAppWindow
from clFormSubmitter import ClFormSubmitter
from modelsAlchemy import Profile, dbSession
from newProfile import NewProfileProgram
from settings import SettingsProgram


class MainAppProgram(Ui_MainAppWindow):
    countryStateDict = {}

    def __init__(self, window):
        Ui_MainAppWindow.__init__(self)
        self.setupUi(window)

        self.clFormSubmitter = ClFormSubmitter()

        self.clStartBtn.clicked.connect(self.clFormSubmitHandler)

        self.actionNewProfile.triggered.connect(self.openNewProfile)
        self.actionSettings.triggered.connect(self.openSettings)
        self.actionExit.triggered.connect(self.closeApp)
        self.actionAbout.triggered.connect(self.openAbout)
        self.getProfiles()



    def getProfiles(self):
        self.dbSession = dbSession()
        profiles = self.dbSession.query(Profile).filter(Profile.active==1).order_by(Profile.id.desc()).all()
        for profile in profiles:
            item = QtWidgets.QListWidgetItem(profile.name)
            item.setData(QtCore.Qt.UserRole, profile.id)
            self.clProfileListWidget.addItem(item)

        self.clProfileListWidget.itemClicked.connect(self.profileItemChangeEvent)



    def profileItemChangeEvent(self, item):
        print(item.data(QtCore.Qt.UserRole))



    def clFormSubmitHandler(self):
        clUsername = self.clUsernameLineEdit.text()
        clPassword = self.clPasswordLineEdit.text()

        # loginReturn = self.clFormSubmitter.clLoginSubmit(clUsername, clPassword)



    def openSettings(self):
        self.settingsTabWidget = QtWidgets.QTabWidget()
        self.settingsTabWidgetProgram = SettingsProgram(self.settingsTabWidget)
        self.settingsTabWidget.show()



    def openNewProfile(self):
        self.newProfileDialog = QtWidgets.QDialog()
        self.newProfileDialogProgram = NewProfileProgram(self.newProfileDialog)
        self.newProfileDialog.show()



    def openAbout(self):
        self.aboutDialog = QtWidgets.QDialog()
        self.aboutDialogProgram = AboutProgram(self.aboutDialog)
        self.aboutDialog.show()



    def closeApp(self):
        window.close()



if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    app.setWindowIcon(QtGui.QIcon("robobot-icon.png"))
    window = QtWidgets.QMainWindow()
    mainAppProg = MainAppProgram(window)
    window.show()
    sys.exit(app.exec_())