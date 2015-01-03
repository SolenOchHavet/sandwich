#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""

UI handlers for tab "Override Globals"

"""

try:
    from PyQt4.QtCore import Qt
    from PyQt4.QtGui import *

except:
    from PySide.QtCore import Qt
    from PySide.QtGui import *

import re


class UI(object):
    def __init__(self):
        self.uiLoadEngines()
        self.uiValidate()

    def uiGetCamera(self):
        lstCameras = self.core.getSceneCameras()
        lstResult = QInputDialog.getItem(self, "Select Camera",
            "Select what camera you wish to use instead of the global one:",
            lstCameras, editable = False)

        return self._getResult(lstResult)

    def uiLoadEngines(self):
        """
        Loads all supported render engines in combo box "Override Engine"
        """
        
        self.engineCombo.addItems(self.core.getSupportedEngines())

    # RENAMED FROM: uiLoadRenderSettings
    def uiLoadOverrideGlobals(self):
        """
        Loads the tab "Override Globals" with the settings for the current selected render layer.

        Executes: As sub method to uiLoadSelectedRenderLayer()
        """

        lstCamera = self.core.layer().renderSetting("lstCameraName")
        lstResolution = self.core.layer().renderSetting("lstResolution")
        lstRange = self.core.layer().renderSetting("lstRange")
        lstRenderEngine = self.core.layer().renderSetting("lstRenderEngine")

        self.uiSetCheckBox(self.cameraCheck, lstCamera[0])
        self.uiSetCheckBox(self.resolutionCheck, lstResolution[0])
        self.uiSetCheckBox(self.rangeCheck, lstRange[0])
        self.uiSetCheckBox(self.engineCheck, lstRenderEngine[0])

        self.cameraField.setText(lstCamera[1])
        self.widthField.setText(lstResolution[1])
        self.heightField.setText(lstResolution[2])
        self.startField.setText(lstRange[1])
        self.endField.setText(lstRange[2])
        self.stepField.setText(lstRange[3])

        if lstRenderEngine[1]:
            self.engineCombo.setCurrentIndex(self.core.getSupportedEngines().index(lstRenderEngine[1]))

        else:
            self.engineCombo.setCurrentIndex(0)

    def uiSaveTabContent(self):
        """
        Saves everything in the tab into the core
        """

        lstCamera = [False, ""]
        lstResolution = [False, "", ""]
        lstRange = [False, "", "", ""]
        lstRenderEngine = [False, ""]

        lstCamera[0] = self.cameraCheck.isChecked()
        lstResolution[0] = self.resolutionCheck.isChecked()
        lstRange[0] = self.rangeCheck.isChecked()
        lstRenderEngine[0] = self.engineCheck.isChecked()

        lstCamera[1] = unicode(self.cameraField.text())
        lstResolution[1] = unicode(self.widthField.text())
        lstResolution[2] = unicode(self.heightField.text())
        lstRange[1] = unicode(self.startField.text())
        lstRange[2] = unicode(self.endField.text())
        lstRange[3] = unicode(self.stepField.text())
        lstRenderEngine[1] = unicode(self.engineCombo.currentText())

        self.core.setLayerRenderSetting("lstCameraName", lstCamera)
        self.core.setLayerRenderSetting("lstResolution", lstResolution)
        self.core.setLayerRenderSetting("lstRange", lstRange)
        self.core.setLayerRenderSetting("lstRenderEngine", lstRenderEngine)

    def uiSetCheckBox(self, qtCheckBox, bValue):
        if bValue:
            qtCheckBox.setCheckState(Qt.Checked)

        else:
            qtCheckBox.setCheckState(Qt.Unchecked)

    def uiSetOverrideCamera(self, sCamera):
        self.cameraField.setText(sCamera)

    def uiValidate(self):
        bOverrideCamera = self.cameraCheck.isChecked()
        bOverrideResolution = self.resolutionCheck.isChecked()
        bOverrideRange = self.rangeCheck.isChecked()
        bOverrideEngine = self.engineCheck.isChecked()

        self.cameraLabel.setEnabled(bOverrideCamera)
        self.cameraField.setEnabled(bOverrideCamera)
        self.cameraButton.setEnabled(bOverrideCamera)
        self.resolutionLabel.setEnabled(bOverrideResolution)
        self.widthField.setEnabled(bOverrideResolution)
        self.heightField.setEnabled(bOverrideResolution)
        self.rangeLabel.setEnabled(bOverrideRange)
        self.startField.setEnabled(bOverrideRange)
        self.endField.setEnabled(bOverrideRange)
        self.stepField.setEnabled(bOverrideRange)
        self.engineLabel.setEnabled(bOverrideEngine)
        self.engineCombo.setEnabled(bOverrideEngine)

    def _getResult(self, lstResult):
        if lstResult[1]:
            return unicode(lstResult[0])

        else:
            return ""