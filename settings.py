import json
import sys
import threading

import asyncio
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QMessageBox, QTableWidgetItem

# from modelsPeewee import Proxy, Location
from fetchOnlineProxies import FetchOnlineProxies
from modelsAlchemy import Proxy, Location, dbSession
from clPageScrapper import ClPageScrapper
from settingsTabWidget import Ui_settingsTabWidget
from fileBrowserDialog import FileBrowserDialogProgram



class SettingsProgram(Ui_settingsTabWidget):

    def __init__(self, tabWidget):
        Ui_settingsTabWidget.__init__(self)
        self.setupUi(tabWidget)
        self.dialog = tabWidget

        self.loop = asyncio.get_event_loop()

        self.getProxyIPsFromDBThread = threading.Thread(target=self.getProxyIPsFromDB)
        self.getProxyIPsFromDBThread.daemon = True
        self.getProxyIPsFromDBThread.start()
        self.proxyUploadPushButton.clicked.connect(self.uploadedProxyFile)
        self.proxyFetchPushButton.clicked.connect(self.fetchOnlineProxyDataEvent)
        self.downloadLocPushButton.clicked.connect(self.downloadSaveLocData)



    def getProxyIPsFromDB(self):
        self.dbSession = dbSession()
        proxies = self.dbSession.query(Proxy).all()
        if len(proxies) > 0:
            self.proxyTableWidget.setRowCount(len(proxies))
            self.proxyTableWidget.setEnabled(False)
            for currentRowCount, proxy in enumerate(proxies):
                self.proxyTableWidget.setItem(currentRowCount, 0, QTableWidgetItem(proxy.ip))
                self.proxyTableWidget.setItem(currentRowCount, 1, QTableWidgetItem(proxy.port))
                self.proxyTableWidget.setItem(currentRowCount, 2, QTableWidgetItem(proxy.type))
                if proxy.active is 1:
                    self.proxyTableWidget.setItem(currentRowCount, 3, QTableWidgetItem('Active'))
                    self.proxyTableWidget.item(currentRowCount, 3).setBackground(QColor(43, 228, 55))
                else:
                    self.proxyTableWidget.setItem(currentRowCount, 3, QTableWidgetItem('Inactive'))
                    self.proxyTableWidget.item(currentRowCount, 3).setBackground(QColor(229, 70, 70))

            self.proxyTableWidget.setEnabled(True)

        self.dbSession.close()


    def fetchOnlineProxyDataEvent(self):
        prevProxyDelStatus = self.proxyDeletePrevCheckBox.isChecked()
        if prevProxyDelStatus is True:
            self.dbSession = dbSession()
            self.dbSession.execute('''DELETE FROM proxies''')
            self.dbSession.commit()
            self.dbSession.close()

        self.fetchOnlineProxyDataThread = threading.Thread(target=self.fetchOnlineProxyData)
        self.fetchOnlineProxyDataThread.daemon = True
        self.fetchOnlineProxyDataThread.start()
        # self.fetchOnlineProxyDataThread.join()



    def fetchOnlineProxyData(self):
        self.proxyUploadPushButton.setEnabled(False)
        self.proxyFetchPushButton.setEnabled(False)
        self.proxyIPVersionComboBox.setEnabled(False)
        self.proxyDeletePrevCheckBox.setEnabled(False)
        self.proxyFetchPushButton.setText("Fetching...")


        fetchOnlineProxies = FetchOnlineProxies()
        fetchOnlineProxies.proxyCount = 100
        fetchOnlineProxies.countries = ['US']
        fetchOnlineProxies.types = ['SOCKS4', 'SOCKS5']
        fetchedProxyList = fetchOnlineProxies.getProxies(self.loop, self.proxyFetchPushButton)

        self.dbSession = dbSession()
        proxyList = []
        for count, ipPortList in enumerate(fetchedProxyList):
            self.proxyFetchPushButton.setText("Saving ("+str(count)+"/"+str(len(fetchedProxyList))+")")
            proxy = self.dbSession.query(Proxy).filter(Proxy.ip == ipPortList['host'], Proxy.port == ipPortList['port'], Proxy.type == ipPortList['type']).all()
            if len(proxy) < 1:
                proxyList.append(Proxy(ip=ipPortList['host'], port=ipPortList['port'], type=ipPortList['type'], active=1))

        self.dbSession.add_all(proxyList)
        self.dbSession.commit()
        self.dbSession.close()

        self.proxyFetchPushButton.setText("Fetch Online")
        self.proxyUploadPushButton.setEnabled(True)
        self.proxyFetchPushButton.setEnabled(True)
        self.proxyIPVersionComboBox.setEnabled(True)
        self.proxyDeletePrevCheckBox.setEnabled(True)

        self.getProxyIPsFromDB()



    def uploadedProxyFile(self):
        selectedIPVersion = self.proxyIPVersionComboBox.itemData(self.proxyIPVersionComboBox.currentIndex())
        if selectedIPVersion != "":
            self.fileBrowserDialogProgram = FileBrowserDialogProgram()
            file = self.fileBrowserDialogProgram.openFileNameDialog("Text File (*.txt)")
            if file != "":
                prevProxyDelStatus = self.proxyDeletePrevCheckBox.isChecked()
                if prevProxyDelStatus is True:
                    self.dbSession = dbSession()
                    self.dbSession.execute('''DELETE FROM proxies''')
                    self.dbSession.commit()
                    self.dbSession.close()

                self.saveProxyIPsToDBThread = threading.Thread(target=self.saveProxyDataToDB, args=(file, selectedIPVersion))
                self.saveProxyIPsToDBThread.daemon = True
                self.saveProxyIPsToDBThread.start()

            else:
                self.showMessageDialog("error", "No file found!")
        else:
            self.showMessageDialog("warning", "No IP Version selected!")



    def saveProxyDataToDB(self, file, selectedIPVersion):
        self.proxyUploadPushButton.setEnabled(False)
        self.proxyFetchPushButton.setEnabled(False)
        self.proxyIPVersionComboBox.setEnabled(False)
        self.proxyDeletePrevCheckBox.setEnabled(False)
        self.proxyUploadPushButton.setText("Uploading...")
        ipPortMultiList = [line.strip('\n').split(':') for line in open(file, 'r')]


        self.dbSession = dbSession()
        proxyList = []
        for count, ipPortList in enumerate(ipPortMultiList):
            self.proxyUploadPushButton.setText("Saving ("+str(count)+"/"+str(len(ipPortMultiList))+")")
            proxy = self.dbSession.query(Proxy).filter(Proxy.ip == ipPortList[0], Proxy.port == ipPortList[1], Proxy.type == selectedIPVersion).all()
            if len(proxy) < 1:
                proxyList.append(Proxy(ip=ipPortList[0], port=ipPortList[1], type=selectedIPVersion, active=1))

        self.dbSession.add_all(proxyList)
        self.dbSession.commit()
        self.dbSession.close()

        self.proxyUploadPushButton.setText("Upload")
        self.proxyUploadPushButton.setEnabled(True)
        self.proxyFetchPushButton.setEnabled(True)
        self.proxyIPVersionComboBox.setEnabled(True)
        self.proxyDeletePrevCheckBox.setEnabled(True)

        self.getProxyIPsFromDB()



    def downloadSaveLocData(self):
        self.downloadSaveLocDataThread = threading.Thread(target=self.downloadLocData)
        self.downloadSaveLocDataThread.daemon = True
        self.downloadSaveLocDataThread.start()



    def downloadLocData(self):
        self.downloadLocPushButton.setEnabled(False)
        self.downloadLocPushButton.setText("Scrapping...")
        clPageScrapper = ClPageScrapper()
        locationUrlDictJsonData = clPageScrapper.getClLocationData()
        self.saveLocData(locationUrlDictJsonData)
        self.downloadLocPushButton.setText("Download")
        self.downloadLocPushButton.setEnabled(True)



    def saveLocData(self, locationUrlDictJsonData):
        locationUrlDict = json.loads(locationUrlDictJsonData)
        if len(locationUrlDict) > 0:
            self.downloadLocPushButton.setText("Deleting Previous all")

            self.dbSession = dbSession()
            self.dbSession.execute('''DELETE FROM locations''')
            self.dbSession.commit()

            locationObjList = []
            for count, location in enumerate(locationUrlDict):
                self.downloadLocPushButton.setText("Saving ("+str(count)+"/"+str(len(locationUrlDict))+")")
                locationObjList.append(Location(location=location, sub_location=json.dumps(locationUrlDict[location]), active=1))

            self.dbSession.add_all(locationObjList)
            self.dbSession.commit()
            self.dbSession.close()



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
    tabWidget = QtWidgets.QTabWidget()
    settingsProg = SettingsProgram(tabWidget)
    tabWidget.show()
    sys.exit(app.exec_())