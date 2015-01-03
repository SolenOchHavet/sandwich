#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""

UI handlers for tab "Shaders"

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
        self.sSelectedShader = ""

    def uiAddShaderContent(self, sNewObjects):
        sText = unicode(self.assignField.toPlainText()).strip()

        if sText:
            sText += "\n"

        sText += sNewObjects

        self.assignField.setText(sText)

    def uiAsk(self, sTitle, sMessage):
        iIndex = QMessageBox.warning(self, sTitle, sMessage, "OK", "Cancel")

        return {0: True, 1: False}[iIndex]

    def uiGetDestinationLayer(self):
        # Retrieve all render layers and remove the current render layer
        lstLayers = self.core.getLayers(bIncludeMasterLayer = False)
        lstLayers.remove(self.core.layer().current())

        if not lstLayers:
            return

        lstResult = QInputDialog.getItem(self, "Transfer Shader to Render Layer",
            "Select which render layer you wish to transfer shader <b>%s</b> to:" %
            (self.sSelectedShader), lstLayers, editable = False)

        return self._getResult(lstResult)

    def uiGetNewShader(self):
        lstShaders = self.core.getSceneShaders()
        lstResult = QInputDialog.getItem(self, "Add Shader to Render Layer",
            "Select what shader you wish to add to the current render layer:",
            lstShaders, editable = False)

        return self._getResult(lstResult)

    def uiGetRenamedShaders(self):
        # Adding extra space at the end to make the dialog extra wide :)
        lstResult = QInputDialog.getText(self, "Rename Shader",
            "Enter the new name of the shader:          ",
            QLineEdit.Normal, self.sSelectedShader)

        return self._getResult(lstResult)

    def uiGetShaderContentAsList(self):
        """
        Returns a list of all objects specifies in the text field.
        Any Python comment inside the text field will be removed.
        """

        return self.core.getOnlyObjects(unicode(self.assignField.toPlainText()))

    def uiGetShaderContentAsString(self):
        """
        Returns a list of all objects specifies in the text field.
        Any Python comment inside the text field will be removed.
        """

        return unicode(self.assignField.toPlainText())

    def uiIsShaderSelected(self):
        return self.shaderList.currentRow() != -1

    def uiLoadSelectedShader(self):
        if self.sSelectedShader:
            sShaderContent = self.core.layer().shaderAssignment(self.sSelectedShader)

        else:
            sShaderContent = ""

        self.assignField.setText(sShaderContent)

    def uiLoadShaders(self, sDefaultShader = None):
        self.shaderList.blockSignals(True)

        self.shaderList.clear()
        self.assignField.clear()

        lstShaders = self.core.layer().shaders()

        for sShader in lstShaders:
            self.shaderList.addItem(sShader)

        # Set default
        if sDefaultShader:
            self.shaderList.setCurrentRow(lstShaders.index(sDefaultShader))

        self.shaderList.blockSignals(False)

    def uiRemoveSelectedShader(self):
        self.shaderList.blockSignals(True)

        iIndex = self.shaderList.currentRow()
        self.shaderList.takeItem(iIndex)

        self.core.layer().removeShader(self.sSelectedShader)

        self.shaderList.blockSignals(False)

    def uiSavePreviousSelectedShader(self):
        if self.sSelectedShader:
            sShaderContent = unicode(self.assignField.toPlainText())

            self.core.layer().setShaderAssignment(self.sSelectedShader, sShaderContent)

    def uiSaveSelectedShader(self):
        item = self.shaderList.currentItem()

        if item:
            self.sSelectedShader = unicode(item.text())

        else:
            self.sSelectedShader = ""

    def uiSaveSelectedShaderContent(self):
        if self.sSelectedShader:
            sValue = unicode(self.assignField.toPlainText())
            self.core.layer().setShaderAssignment(self.sSelectedShader, sValue)

    def uiSetShaderContent(self, sContent):
        self.assignField.setText(sContent)

    def uiShowContextMenu(self, position, evtPostAction = None):
        """
        Shows a context menu with the items:
         * Rename Shader: Lets user rename selected shader
         * Delete Shader: Deletes selected shader
         * Transfer Shader: Transfer a copy of the shader with it's content to another layer
        """

        menu = QMenu()

        # Populate the context menu
        renameAction = menu.addAction("Rename Shader...")
        menu.addSeparator()
        transferAction = menu.addAction("Transfer Shader...")
        menu.addSeparator()
        deleteAction = menu.addAction("Delete Shader...")

        # Execute the context menu and retrieve the result
        result = menu.exec_(self.shaderList.mapToGlobal(position))

        # Check the result and return what we should do
        if result == renameAction:
            return 0

        elif result == transferAction:
            return 1

        elif result == deleteAction:
            return 2

    def uiValidate(self):
        item = self.shaderList.currentItem()

        if item:
            bEnable = True

        else:
            bEnable = False

        self.assignLabel.setEnabled(bEnable)
        self.assignField.setEnabled(bEnable)
        self.renameshaderButton.setEnabled(bEnable)
        self.addobjectsButton.setEnabled(bEnable)
        self.orgobjectsButton.setEnabled(bEnable)

    def _getResult(self, lstResult):
        if lstResult[1]:
            return unicode(lstResult[0])

        else:
            return ""