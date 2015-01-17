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
        self.uiLoadRenderLayers()
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
            QLineEdit.Normal, self.core.layer().layerName())

        return self._getResult(lstResult)

    def uiIsRenderLayerSelected(self):
        if self.dataTree.selectedItems():
            return True

        return False

    def uiLoadRenderLayers(self):
        self.dataTree.blockSignals(True)
        self.dataTree.clear()

        for oLayer in self.core.layers():
            item = QTreeWidgetItem()

            item.setText(0, oLayer.layerName())

            self.dataTree.addTopLevelItem(item)

            if self.core.layer() == oLayer:
                item.setSelected(True)

        self.dataTree.blockSignals(False)

    def uiLoadSelectedRenderLayer(self):
        if self.core.layer().layerName() == "masterLayer":
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
        iIndex = self.dataTree.currentRow()
        self.dataTree.blockSignals(True)
        self.dataTree.takeItem(iIndex)
        self.dataTree.setCurrentRow(iIndex)
        self.dataTree.blockSignals(False)

        self.core.layer(self.core.layer().layerName()).remove()

    def uiSaveSelectedRenderLayer(self):
        lstSelection = self.dataTree.selectedItems()

        if lstSelection:
            self.core.selectLayer(lstSelection[0].text(0))

        else:
            self.core.selectLayer(None)

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

    def uiSetCheckBox(self, qtCheckBox, bValue):
        if bValue:
            qtCheckBox.setCheckState(Qt.Checked)

        else:
            qtCheckBox.setCheckState(Qt.Unchecked)

    def uiSetRenderLayer(self, sLayerName):
        self.dataTree.blockSignals(True)
        
        lstResult =  self.dataTree.findItems(sLayerName, 
            Qt.MatchFixedString)
        
        if lstResult:
            self.dataTree.setCurrentItem(lstResult[0])
        
        self.dataTree.blockSignals(False)

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
            result = menu.exec_(self.dataTree.mapToGlobal(position))

            # Check the result and and return what we should do
            if result == deleteAction:
                # Checks if user tries to delete masterlayer. In that case return None
                if re.search("masterlayer", self.core.layer().layerName(), re.IGNORECASE):
                    return None

                else:
                    return 0

    def uiUpdateViewMenu(self, sSelectedLayerName = None):
        self.parent.layerMenu.clear()
        actionGroup = QActionGroup(self.parent.layerMenu)

        for oLayer in self.core.layers():
            action = self.parent.layerMenu.addAction(oLayer.layerName())
            action.setCheckable(True)
            action.triggered.connect(partial(self.sgnSelectLayer, oLayer.layerName()))

            actionGroup.addAction(action)

            if oLayer.layerName() == sSelectedLayerName:
                action.setChecked(True)

    def uiUpdateWindowTitle(self):
        self.parent.setWindowTitle("Sandwich: " + self.core.layer().layerName())

    def uiValidate(self):
        if self.core.layer().layerName() == "masterLayer":
            bIsMasterLayer = False

        else:
            bIsMasterLayer = True

        self.toolbar.renameLayerButton.setEnabled(bIsMasterLayer)
        self.toolbar.savelayerButton.setEnabled(bIsMasterLayer)
        self.settingsTab.setEnabled(bIsMasterLayer)

    def _getResult(self, lstResult):
        if lstResult[1]:
            return unicode(lstResult[0])

        else:
            return ""