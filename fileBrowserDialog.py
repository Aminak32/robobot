from PyQt5.QtWidgets import QWidget, QFileDialog


class FileBrowserDialogProgram(QWidget):

    def openFileNameDialog(self, fileType):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file, _ = QFileDialog.getOpenFileName(self, "Open File", "", fileType, options=options)
        if file:
            return file
        else:
            return ""

    def openFileNamesDialog(self, fileType):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        files, _ = QFileDialog.getOpenFileNames(self, "Open Files", "", fileType, options=options)
        if files:
            return files
        else:
            return ""

    def saveFileDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getSaveFileName(self, "Save File", "",
                                                  "All Files (*);;Text Files (*.txt)", options=options)
        if fileName:
            return fileName
        else:
            return ""
