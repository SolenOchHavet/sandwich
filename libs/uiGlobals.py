#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""

UI handlers for dialog "Globals"

"""

try:
    from PyQt4.QtCore import Qt
    from PyQt4.QtGui import *

except:
    from PySide.QtCore import Qt
    from PySide.QtGui import *

import maya.cmds as mc

import re
import os


class UI(object):
    def __init__(self):
        self.sSelectedCamera = ""
        self.sSelectedRendersFolder = ""
        self.sSelectedScenesFolder = ""
        self.bSelectedSettingImportRefs = False
        self.sSelectedWidth = 1024
        self.sSelectedHeight = 576
        self.sSelectedRenderEngine = ""

        self.sSelectedStart = 1
        self.sSelectedEnd = 10
        self.sSelectedStep = 1

        self.uiLoadGlobals()

    def uiCloseWindow(self):
        self.close()

    def uiGetCheckResults(self):
        sErr = ""

        if not os.path.exists(self.sSelectedRendersFolder):
            sErr += "Your \"Output Renders\" folder does not exists.<br>"

        if not os.path.exists(self.sSelectedScenesFolder):
            sErr += "Your \"Output Scenes\" folder does not exists.<br>"

        if not mc.objExists(self.sSelectedCamera):
            sErr += "Your \"Default Camera\" does not exists.<br>"

        if sErr:
            sTitle = "Warning!"
            sMsg = "The following setting(s) returned error(s):<br><br>" + \
                   sErr + "<br>Are you sure you still wish to save the new " \
                   "settings?"

            iIndex = QMessageBox.warning(self, sTitle, sMsg)

            if iIndex == 0:
                return True

            else:
                return False

        else:
            return True

    def uiGetNewCamera(self):
        lstCameras = self.core.getSceneCameras()
        lstResult = QInputDialog.getItem(self, "Select Camera",
                                         "Select what camera you wish to use " \
                                         "instead of the global one:",
                                         lstCameras, editable = False)

        return self._getResult(lstResult)

    def uiGetNewFolder(self, sTitle, sDefaultPath):
        if os.path.exists(sDefaultPath):
            return unicode(QFileDialog.getExistingDirectory(self, sTitle, sDefaultPath))

        else:
            return unicode(QFileDialog.getExistingDirectory(self, sTitle))

    def uiGetNewRendersFolder(self):
        sTitle = "Select Renders Folder"
        sCurrentFolderPath = unicode(self.rendersField.text())

        return self.uiGetNewFolder(sTitle, sCurrentFolderPath)

    def uiGetNewScenesFolder(self):
        sTitle = "Select Render Scenes Folder"
        sCurrentFolderPath = unicode(self.scenesField.text())

        return self.uiGetNewFolder(sTitle, sCurrentFolderPath)

    def uiLoadGlobals(self):
        for oEngine in self.core.engines():
            self.engineCombo.addItem(oEngine.displayName(), oEngine)

        sDefaultEngine = self.core.getGlobalsValue("sDefaultEngine")
        iIndex = self.engineCombo.findText(sDefaultEngine)
        
        if iIndex != -1:
            self.engineCombo.setCurrentIndex(iIndex)

        self.rendersField.setText(self.core.getGlobalsValue("sOutputRenders"))
        self.scenesField.setText(self.core.getGlobalsValue("sOutputScenes"))
        self.cameraField.setText(self.core.getGlobalsValue("sDefaultCamera"))

        self.widthField.setText(unicode(self.core.getGlobalsValue("iWidth")))
        self.heightField.setText(unicode(self.core.getGlobalsValue("iHeight")))

        self.startField.setText(unicode(self.core.getGlobalsValue("iStart")))
        self.endField.setText(unicode(self.core.getGlobalsValue("iEnd")))
        self.stepField.setText(unicode(self.core.getGlobalsValue("iStep")))

        self.terminalField.setText(self.core.getGlobalsValue("sTerminalApp"))

        self.uiSetCheckBox(self.mergeCheck, self.core.getGlobalsValue("bSettingImportRefs"))

    def uiSaveSelectedCamera(self):
        self.sSelectedCamera = unicode(self.cameraField.text()).strip()

    def uiSaveSelectedRenderEngine(self):
        self.sSelectedRenderEngine = unicode(self.engineCombo.currentText())

    def uiSaveSelectedRendersFolder(self):
        self.sSelectedRendersFolder = unicode(self.rendersField.text()).strip()

    def uiSaveSelectedScenesFolder(self):
        self.sSelectedScenesFolder = unicode(self.scenesField.text()).strip()

    def uiSaveSelectedSettings(self):
        self.sSelectedWidth = unicode(self.widthField.text())
        self.sSelectedHeight = unicode(self.heightField.text())

        self.sSelectedStart = unicode(self.startField.text())
        self.sSelectedEnd = unicode(self.endField.text())
        self.sSelectedStep = unicode(self.stepField.text())

        self.bSelectedSettingImportRefs = self.mergeCheck.isChecked()

    def uiSaveSelectedTerminalApp(self):
        self.sSelectedTerminalApp = unicode(self.terminalField.text())

    def uiSetCamera(self, sCameraName):
        self.cameraField.setText(sCameraName)

    def uiSetCheckBox(self, qtCheckBox, bValue):
        if bValue:
            qtCheckBox.setCheckState(Qt.Checked)

        else:
            qtCheckBox.setCheckState(Qt.Unchecked)

    def uiSetRendersFolder(self, sRendersFolder):
        self.rendersField.setText(sRendersFolder)

    def uiSetScenesFolder(self, sScenesFolder):
        self.scenesField.setText(sScenesFolder)

    def _getResult(self, lstResult):
        if lstResult[1]:
            return unicode(lstResult[0])

        else:
            return ""