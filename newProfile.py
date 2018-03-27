import json
import sys
import threading

import time
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import QTimer, QThread
from PyQt5.QtWidgets import QMessageBox, QProgressBar, QProgressDialog
from clFormSubmitter import ClFormSubmitter
from modelsAlchemy import Location, dbSession, asc, Profile, Profilepicker
from newProfileDialog import Ui_newProfileDialog
from progress import ProgressProgramOperation
from clPageScrapper import ClPageScrapper


class NewProfileProgram(Ui_newProfileDialog):
    profileDataDict = {}
    profilePickerDataDict = []

    clPostPickerComboNumber = 0


    def __init__(self, dialog):
        Ui_newProfileDialog.__init__(self)
        self.setupUi(dialog)
        self.dialog = dialog

        self.progressProgramOperation = ProgressProgramOperation()
        self.clFormSubmitter = ClFormSubmitter()
        self.clPageScrapper = ClPageScrapper()


        self.clCreateProfileSaveBtn.setEnabled(False)

        self.addLocationItemsThread = threading.Thread(target=self.addLocationItems)
        self.addLocationItemsThread.daemon = True
        self.addLocationItemsThread.start()
        # self.addLocationItems()
        self.clLocationComboBox.activated.connect(self.addSubLocationItemsOnLocationChangeEvent)
        self.clSubLocationComboBox.activated.connect(self.addPostTypesOnSubLocationChangeEvent)
        # self.clPostTypeComboBox.activated.connect(self.addPostPickerFormDataOnPostTypeChangeEvent)
        self.clPostTypeComboBox.activated.connect(self.addPostPickerFormDataEvent)

        self.clPostAttrComboBox_1.activated.connect(self.addPostPickerFormDataEvent)
        self.clPostAttrComboBox_2.activated.connect(self.addPostPickerFormDataEvent)
        self.clPostAttrComboBox_3.activated.connect(self.addPostPickerFormDataEvent)
        self.clPostAttrComboBox_4.activated.connect(self.addPostPickerFormDataEvent)
        self.clPostAttrComboBox_5.activated.connect(self.addPostPickerFormDataEvent)

        self.clCreateProfileSaveBtn.clicked.connect(self.newProfileDataSaveEvent)
        self.clCreateProfileCloseBtn.clicked.connect(self.newProfileCloseEvent)


    def addLocationItems(self):
        self.dbSession = dbSession()
        locations = self.dbSession.query(Location).order_by(asc(Location.location)).all()

        self.clLocationComboBox.clear()
        # self.clLocationComboBox.addItem("Select", "")
        if len(locations) > 0:
            for location in locations:
                self.clLocationComboBox.addItem(location.location, location.location)

        self.dbSession.close()



    def addSubLocationItemsOnLocationChangeEvent(self):
        self.clLocationComboBox.setEnabled(False)
        self.addSubLocationItemsThread = threading.Thread(target=self.addSubLocationItems)
        self.addSubLocationItemsThread.daemon = True
        self.addSubLocationItemsThread.start()


    def addSubLocationItems(self):
        selectedLocation = self.clLocationComboBox.itemData(self.clLocationComboBox.currentIndex())
        # saving selected location in profileDataDict
        self.profileDataDict['selected_location'] = selectedLocation


        self.dbSession = dbSession()
        location = self.dbSession.query(Location) \
            .filter(Location.location == str(selectedLocation)) \
            .filter(Location.active == 1) \
            .order_by(asc(Location.location)).first()

        subLocationDict = json.loads(location.sub_location)

        self.clSubLocationComboBox.clear()
        # self.clSubLocationComboBox.addItem("Select", "")
        for subLocation in subLocationDict:
            self.clSubLocationComboBox.addItem(subLocation['location'], subLocation['link'])

        self.clSubLocationLbl.setVisible(True)
        self.clSubLocationComboBox.setVisible(True)



    def addPostTypesOnSubLocationChangeEvent(self):
        self.clSubLocationComboBox.setEnabled(False)
        self.addPostTypesThread = threading.Thread(target=self.addPostTypes)
        self.addPostTypesThread.daemon = True
        self.addPostTypesThread.start()



    def addPostTypes(self):
        selectedSubLocation = self.clSubLocationComboBox.currentText()
        selectedSubLocationLink = self.clSubLocationComboBox.itemData(self.clSubLocationComboBox.currentIndex())
        # saving selected sub location in profileDataDict
        self.profileDataDict['selected_sub_location'] = selectedSubLocation

        self.clCreateProfileSaveBtn.setText("Scrapping post type")

        self.postTypeDictJsonData = self.clPageScrapper.getClPostTypes(selectedSubLocationLink, self.clCreateProfileSaveBtn)
        self.postTypeDict = json.loads(self.postTypeDictJsonData)
        self.clPostTypePageLink = self.postTypeDict['postPageLink']
        self.clPostTypeFormActionLink = self.postTypeDict['formActionLink']

        # saving selected post url in profileDataDict
        self.profileDataDict['selected_post_url'] = self.clPostTypePageLink


        self.clPostTypeComboBox.clear()
        # self.clPostTypeComboBox.addItem("Select", "")
        for postType in self.postTypeDict['clPostTypeDict']:
            self.clPostTypeComboBox.addItem(self.postTypeDict['clPostTypeDict'][postType], postType)


        self.clCreateProfileSaveBtn.setText("Save")

        self.clPostTypeLbl.setVisible(True)
        self.clPostTypeComboBox.setVisible(True)



    def addPostPickerFormDataEvent(self):
        self.clPostTypeComboBox.setEnabled(False)
        self.addPostPickerThread = threading.Thread(target=self.addPostPicker)
        self.addPostPickerThread.daemon = True
        self.addPostPickerThread.start()



    def addPostPicker(self):
        # selectedPostPickerVal = ""
        # selectedPostPickerActionUrl = ""
        # selectedPostPickerCurrentUrl = ""

        profilePickerDataSingleDict = {}

        if self.clPostPickerComboNumber is 0:
            self.selectedPostPickerText = self.clPostTypeComboBox.itemText(self.clPostTypeComboBox.currentIndex())
            self.selectedPostPickerVal = self.clPostTypeComboBox.itemData(self.clPostTypeComboBox.currentIndex())
            self.selectedPostPickerActionUrl = self.clPostTypeFormActionLink
            self.selectedPostPickerCurrentUrl = self.clPostTypePageLink

            profilePickerDataSingleDict['text'] = self.selectedPostPickerText
            profilePickerDataSingleDict['value'] = self.selectedPostPickerVal
            profilePickerDataSingleDict['url'] = self.selectedPostPickerCurrentUrl
            self.profilePickerDataDict.append(profilePickerDataSingleDict)

            self.clPostPickerComboNumber = 1

        elif self.clPostPickerComboNumber is 1:
            self.selectedPostPickerText = self.clPostAttrComboBox_1.itemText(self.clPostAttrComboBox_1.currentIndex())
            self.selectedPostPickerVal = self.clPostAttrComboBox_1.itemData(self.clPostAttrComboBox_1.currentIndex())

            profilePickerDataSingleDict['text'] = self.selectedPostPickerText
            profilePickerDataSingleDict['value'] = self.selectedPostPickerVal
            profilePickerDataSingleDict['url'] = self.selectedPostPickerCurrentUrl
            self.profilePickerDataDict.append(profilePickerDataSingleDict)

            self.clPostAttrComboBox_1.setEnabled(False)
            self.clPostPickerComboNumber = 2

        elif self.clPostPickerComboNumber is 2:
            self.selectedPostPickerText = self.clPostAttrComboBox_2.itemText(self.clPostAttrComboBox_2.currentIndex())
            self.selectedPostPickerVal = self.clPostAttrComboBox_2.itemData(self.clPostAttrComboBox_2.currentIndex())

            profilePickerDataSingleDict['text'] = self.selectedPostPickerText
            profilePickerDataSingleDict['value'] = self.selectedPostPickerVal
            profilePickerDataSingleDict['url'] = self.selectedPostPickerCurrentUrl
            self.profilePickerDataDict.append(profilePickerDataSingleDict)

            self.clPostAttrComboBox_2.setEnabled(False)
            self.clPostPickerComboNumber = 3

        elif self.clPostPickerComboNumber is 3:
            self.selectedPostPickerText = self.clPostAttrComboBox_3.itemText(self.clPostAttrComboBox_3.currentIndex())
            self.selectedPostPickerVal = self.clPostAttrComboBox_3.itemData(self.clPostAttrComboBox_3.currentIndex())

            profilePickerDataSingleDict['text'] = self.selectedPostPickerText
            profilePickerDataSingleDict['value'] = self.selectedPostPickerVal
            profilePickerDataSingleDict['url'] = self.selectedPostPickerCurrentUrl
            self.profilePickerDataDict.append(profilePickerDataSingleDict)

            self.clPostAttrComboBox_3.setEnabled(False)
            self.clPostPickerComboNumber = 4

        elif self.clPostPickerComboNumber is 4:
            self.selectedPostPickerText = self.clPostAttrComboBox_4.itemText(self.clPostAttrComboBox_4.currentIndex())
            self.selectedPostPickerVal = self.clPostAttrComboBox_4.itemData(self.clPostAttrComboBox_4.currentIndex())

            profilePickerDataSingleDict['text'] = self.selectedPostPickerText
            profilePickerDataSingleDict['value'] = self.selectedPostPickerVal
            profilePickerDataSingleDict['url'] = self.selectedPostPickerCurrentUrl
            self.profilePickerDataDict.append(profilePickerDataSingleDict)

            self.clPostAttrComboBox_4.setEnabled(False)
            self.clPostPickerComboNumber = 5

        elif self.clPostPickerComboNumber is 5:
            print("no more combobox")


        if self.selectedPostPickerVal != "" and self.selectedPostPickerActionUrl != "" and self.selectedPostPickerCurrentUrl != "":
            self.clCreateProfileSaveBtn.setText("Scrapping post picker")
            clPostPickerFormData = self.clPageScrapper.getClPostPickerFormData(self.selectedPostPickerVal, self.selectedPostPickerCurrentUrl, self.clCreateProfileSaveBtn)
            if clPostPickerFormData is not False:
                clPostPickerFormJsonData = json.loads(clPostPickerFormData)
                self.selectedPostPickerActionUrl = clPostPickerFormJsonData['formActionLink']
                self.selectedPostPickerCurrentUrl = clPostPickerFormJsonData['postPageLink']
                clPostPickerFormDataDict = clPostPickerFormJsonData['clPostFormDataDict']


                if self.clPostPickerComboNumber is 1:
                    self.clPostAttrLbl_1.setVisible(True)
                    self.clPostAttrComboBox_1.setVisible(True)
                    self.addPostPickerDataToComboBox(clPostPickerFormDataDict, self.clPostAttrComboBox_1)

                if self.clPostPickerComboNumber is 2:
                    self.clPostAttrLbl_2.setVisible(True)
                    self.clPostAttrComboBox_2.setVisible(True)
                    self.addPostPickerDataToComboBox(clPostPickerFormDataDict, self.clPostAttrComboBox_2)

                if self.clPostPickerComboNumber is 3:
                    self.clPostAttrLbl_3.setVisible(True)
                    self.clPostAttrComboBox_3.setVisible(True)
                    self.addPostPickerDataToComboBox(clPostPickerFormDataDict, self.clPostAttrComboBox_3)

                if self.clPostPickerComboNumber is 4:
                    self.clPostAttrLbl_4.setVisible(True)
                    self.clPostAttrComboBox_4.setVisible(True)
                    self.addPostPickerDataToComboBox(clPostPickerFormDataDict, self.clPostAttrComboBox_4)

                if self.clPostPickerComboNumber is 5:
                    self.clPostAttrLbl_5.setVisible(True)
                    self.clPostAttrComboBox_5.setVisible(True)
                    self.addPostPickerDataToComboBox(clPostPickerFormDataDict, self.clPostAttrComboBox_5)


                self.clCreateProfileSaveBtn.setText("Save")

            else:
                self.clCreateProfileSaveBtn.setText("Save")
                self.clCreateProfileSaveBtn.setEnabled(True)



    def addPostPickerDataToComboBox(self, clPostPickerFormDataDict, comboBoxObj):
        for clPostPickerData in clPostPickerFormDataDict:
            comboBoxObj.addItem(clPostPickerFormDataDict[clPostPickerData], clPostPickerData)



    def newProfileDataSaveEvent(self):
        if self.clProfileNameLineEdit.text() != "":

            self.dbSession = dbSession()
            profiles = self.dbSession.query(Profile).filter(Profile.name == self.clProfileNameLineEdit.text()).all()
            self.dbSession.close()

            if len(profiles) < 1:
                self.newProfileDataSaveThread = threading.Thread(target=self.newProfileDataSave)
                self.newProfileDataSaveThread.daemon = True
                self.newProfileDataSaveThread.start()

            else:
                self.showMessageDialog("warning", "Profile name already exist!")
        else:
            self.showMessageDialog("warning", "Profile name cannot be empty!")



    def newProfileDataSave(self):
        self.clCreateProfileSaveBtn.setEnabled(False)
        self.clCreateProfileSaveBtn.setText("Saving profile")

        self.dbSession = dbSession()
        profile = Profile(
            name=self.clProfileNameLineEdit.text(),
            selected_location=self.profileDataDict['selected_location'],
            selected_sub_location=self.profileDataDict['selected_sub_location'],
            selected_post_url=self.profileDataDict['selected_post_url'],
            active=1
        )

        self.dbSession.add(profile)
        self.dbSession.flush()

        profilePickerList = []
        for count, profilePicker in enumerate(self.profilePickerDataDict):
            profilePickerList.append(
                Profilepicker(
                    profile_id=profile.id,
                    order=count + 1,
                    url=profilePicker['url'],
                    selected_value=profilePicker['value'],
                    selected_text=profilePicker['text']
                )
            )

        self.dbSession.add_all(profilePickerList)
        self.dbSession.commit()
        self.dbSession.close()

        self.clCreateProfileSaveBtn.setText("Saved Successfully!")
        time.sleep(2)
        dialog.close()



    def newProfileCloseEvent(self):
        dialog.close()



    def showMessageDialog(self, msgType, msg):
        self.msgBox = QMessageBox()
        if msgType == "error":
            self.msgBox.setIcon(QMessageBox.Critical)
            self.msgBox.setWindowTitle("RoboBot - Error")
        elif msgType == "warning":
            self.msgBox.setIcon(QMessageBox.Warning)
            self.msgBox.setWindowTitle("RoboBot - Warning")
        else:
            self.msgBox.setIcon(QMessageBox.Information)
            self.msgBox.setWindowTitle("RoboBot - Information")
        self.msgBox.setText(msg)
        self.msgBox.show()




if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    app.setWindowIcon(QtGui.QIcon("robobot-icon.png"))
    dialog = QtWidgets.QDialog()
    newProfileProg = NewProfileProgram(dialog)
    dialog.show()
    sys.exit(app.exec_())