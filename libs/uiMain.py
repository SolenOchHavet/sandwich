#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""

UI handlers for "Main"

This code also handles all panels (in the tabWidget).

"""

try:
    from PyQt4.QtCore import Qt
    from PyQt4.QtGui import *

except:
    from PySide.QtCore import Qt
    from PySide.QtGui import *

import re
from functools import partial


class UI(object):
    def __init__(self):
        self.sSelectedLayerName = self.core.layer().current()

        self.uiLoadRenderLayers(self.sSelectedLayerName)
        self.uiSaveSelectedRenderLayer()
        self.uiUpdateWindowTitle()
        self.uiValidate()

    def uiAsk(self, sTitle, sMessage):
        iIndex = QMessageBox.warning(self, sTitle, sMessage, "OK", "Cancel")

        return {0: True, 1: False}[iIndex]

    def uiGetNewRenderLayer(self):
        lstResult = QInputDialog.getText(self, "New Render Layer",
            "Enter the name of the new render layer:")

        return self._getResult(lstResult)

    def uiGetRenamedRenderLayer(self):
        # Adding extra space at the end to make the dialog extra wide :)
        lstResult = QInputDialog.getText(self, "Rename Render Layer",
            "Enter the new name of the render layer:         ",
            QLineEdit.Normal, self.sSelectedLayerName)

        return self._getResult(lstResult)

    def uiIsRenderLayerSelected(self):
        if self.dataTree.selectedItems():
            return True

        return False

    def uiLoadRenderLayers(self, sDefaultRenderLayer = None):
        self.list.renderlayersList.blockSignals(True)

        self.list.renderlayersList.clear()

        for oLayer in self.core.layers():
            self.list.renderlayersList.addItem(oLayer.layerName())

        # Set default
        if sDefaultRenderLayer:
            self.list.renderlayersList.setCurrentRow(lstRenderLayers.index(sDefaultRenderLayer))

        else:
            if self.list.renderlayersList.count() > 0:
                self.list.renderlayersList.setCurrentRow(self.list.renderlayersList.count() - 1)

            else:
                self.list.renderlayersList.setCurrentRow(0)

        self.list.renderlayersList.blockSignals(False)

    def uiLoadSelectedRenderLayer(self):
        if self.sSelectedLayerName == "masterLayer":
            self.overviewFrame.descriptionField.clear()
            self.visibilityFrame.visibilityField.clear()
            self.shadersFrame.shaderList.clear()
            self.shadersFrame.assignField.clear()
            self.attributesFrame.attributesList.clear()
            self.attributesFrame.overrideField.clear()
            self.attributesFrame.revertField.clear()
            self.attributesFrame.assignField.clear()

            self.uiSetCheckBox(self.overrideglobalsFrame.cameraCheck, False)
            self.overrideglobalsFrame.cameraField.clear()
            self.uiSetCheckBox(self.overrideglobalsFrame.resolutionCheck, False)
            self.overrideglobalsFrame.widthField.clear()
            self.overrideglobalsFrame.heightField.clear()
            self.uiSetCheckBox(self.overrideglobalsFrame.rangeCheck, False)
            self.overrideglobalsFrame.startField.clear()
            self.overrideglobalsFrame.endField.clear()
            self.overrideglobalsFrame.stepField.clear()

            self.codeFrame.overrideField.clear()
            self.codeFrame.revertField.clear()

            return

        # Set the data for the Overview tab
        self.overviewFrame.descriptionField.setText(self.core.layer().comments())

        # Load the data for the Visibility tab
        self.visibilityFrame.uiLoadContent()

        # Set the data for the Shaders tab
        self.shadersFrame.shaderList.blockSignals(True)
        self.shadersFrame.shaderList.clear()
        self.shadersFrame.assignField.clear()

        for sShaderName in self.core.layer().shaders():
            self.shadersFrame.shaderList.addItem(sShaderName)

        self.shadersFrame.shaderList.blockSignals(False)

        # Set the data for the Attributes tab
        self.attributesFrame.attributesList.blockSignals(True)
        self.attributesFrame.attributesList.clear()
        self.attributesFrame.overrideField.clear()
        self.attributesFrame.revertField.clear()
        self.attributesFrame.assignField.clear()

        for sAttributeName in self.core.layer().attributes():
            self.attributesFrame.attributesList.addItem(sAttributeName)

        self.attributesFrame.attributesList.blockSignals(False)

        # Set the data for the Render Settings tab
        self.overrideglobalsFrame.uiLoadOverrideGlobals()

        # Set the data for the Render Globals tab
        self.renderglobalsFrame.uiLoadRenderGlobals()

        # Set the data for the MEL tab
        self.codeFrame.overrideField.setText(self.core.layer().overrideCode())
        self.codeFrame.revertField.setText(self.core.layer().revertCode())

    def uiRemoveSelectedRenderLayer(self):
        iIndex = self.list.renderlayersList.currentRow()
        self.list.renderlayersList.blockSignals(True)
        self.list.renderlayersList.takeItem(iIndex)
        self.list.renderlayersList.setCurrentRow(iIndex)
        self.list.renderlayersList.blockSignals(False)

        self.core.layer(self.sSelectedLayerName).remove()

    def uiSaveSelectedRenderLayer(self):
        self.sSelectedLayerName = unicode(self.list.renderlayersList.currentItem().text())

    def uiSaveSelectedRenderLayerContent(self):
        self.overviewFrame.uiSaveTabContent()
        self.visibilityFrame.uiSaveTabContent()
        self.shadersFrame.uiSaveSelectedShaderContent()
        self.attributesFrame.uiSavePreviousSelectedAttribute()
        self.overrideglobalsFrame.uiSaveTabContent()
        self.renderglobalsFrame.uiSaveTabContent()
        self.codeFrame.uiSaveTabContent()

    def uiSaveTabOverview(self):
        self.core.layer().setComments(unicode(self.overviewFrame.descriptionField.toPlainText()))

    def uiSaveTabRenderGlobals(self):
        self.core.addLayerRenderGlobals()

    def uiSetCheckBox(self, qtCheckBox, bValue):
        if bValue:
            qtCheckBox.setCheckState(Qt.Checked)

        else:
            qtCheckBox.setCheckState(Qt.Unchecked)

    def uiSetRenderLayer(self, sLayerName):
        self.list.renderlayersList.blockSignals(True)
        
        lstResult =  self.list.renderlayersList.findItems(sLayerName, 
            Qt.MatchFixedString)
        
        if lstResult:
            self.list.renderlayersList.setCurrentItem(lstResult[0])
        
        self.list.renderlayersList.blockSignals(False)

    def uiSetRenderLayersVisible(self, bState):
        self.list.setHidden(not bState)

    def uiSetToolbarVisible(self, bState):
        self.toolbar.setHidden(not bState)

    def uiShowContextMenu(self, iContextMenuIndex, position, evtPostAction = None):
        """
        Shows a context menu depending on the variable iContextMenuIndex. These are the indexes:
         * 0. The "Render Layers" list in the main window.
         * 1. The "Shaders" list below the "Shaders" tab.
         * 2. The "Attributes" list below the "Attributes" tab.
        """

        menu = QMenu()

        if iContextMenuIndex == 0:
            # Context menu for the list "Render Layers"

            # Populate the context menu
            deleteAction = menu.addAction("Delete Layer...")

            # Execute the context menu and retrieve the result
            result = menu.exec_(self.list.renderlayersList.mapToGlobal(position))

            # Check the result and and return what we should do
            if result == deleteAction:
                # Checks if user tries to delete masterlayer. In that case return None
                if re.search("masterlayer", self.sSelectedLayerName, re.IGNORECASE):
                    return None

                else:
                    return 0

    def uiUpdateViewMenu(self, sSelectedLayerName = None):
        self.parent.layerMenu.clear()

        # Layer > Save layer
        action = self.parent.layerMenu.addAction("Save layer")
        action.triggered.connect(self.sgnSaveLayer)

        # Layer > New layer... 
        action = self.parent.layerMenu.addAction("New layer...")
        action.triggered.connect(self.sgnAddNewLayer)

        # Layer > Rename layer...
        action = self.parent.layerMenu.addAction("Rename layer...")
        action.triggered.connect(self.sgnRenameLayer)

        self.parent.layerMenu.addSeparator()

        actionGroup = QActionGroup(self.parent.layerMenu)

        for oLayer in self.core.layers():
            action = self.parent.layerMenu.addAction(oLayer.layerName())
            action.setCheckable(True)
            action.triggered.connect(partial(self.sgnSelectLayer, oLayer.layerName()))

            actionGroup.addAction(action)

            if oLayer.layerName() == sSelectedLayerName:
                action.setChecked(True)

    def uiUpdateWindowTitle(self):
        self.parent.setWindowTitle("Sandwich: " + self.sSelectedLayerName)

    def uiValidate(self):
        if self.sSelectedLayerName == "masterLayer":
            bIsMasterLayer = False

        else:
            bIsMasterLayer = True

        self.toolbar.renamelayerButton.setEnabled(bIsMasterLayer)
        self.toolbar.savelayerButton.setEnabled(bIsMasterLayer)
        self.settingsTab.setEnabled(bIsMasterLayer)

    def _getResult(self, lstResult):
        if lstResult[1]:
            return unicode(lstResult[0])

        else:
            return ""