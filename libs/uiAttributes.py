#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""

UI handlers for tab "Attributes"

"""

try:
    from PyQt4.QtGui import *

except:
    from PySide.QtGui import *

import re


class UI(object):
    def __init__(self):
        self.sSelectedAttribute = ""

    def uiAddAttributeContent(self, sNewObjects):
        sText = unicode(self.assignField.toPlainText()).strip()

        if sText:
            sText += "\n"

        sText += sNewObjects

        self.assignField.setText(sText)

    def uiAsk(self, sTitle, sMessage):
        iIndex = QMessageBox.warning(self, sTitle, sMessage, "OK", "Cancel")

        return {0: True, 1: False}[iIndex]

    def uiClearLayout(self, qtLayout):
        while qtLayout.count():
            widgetItem = qtLayout.takeAt(0)
            if not widgetItem:
                continue

            widget = widgetItem.widget()
            if widget:
                widget.deleteLater()

    def uiGetAttributeContentAsList(self):
        return self.core.utils.objectsOnly(unicode(self.assignField.toPlainText()).strip())

    def uiGetAttributeContentAsString(self):
        return unicode(self.assignField.toPlainText())

    def uiGetNewAttribute(self):
        lstResult = QInputDialog.getText(self, "New Attribute",
            "Enter the name of the new attribute:")

        sResult = self._getResult(lstResult)

        if sResult:
            # Check if attribute name is valid, otherwise inform user
            if not re.search("^[a-z,_][a-z,_,\\d]*$", sResult, re.IGNORECASE):
                sTitle = "Invalid attribute name"
                sMsg = "Your attribute name \"%s\" is not a valid Maya attribute " \
                    "name. It must start with an alphabetic character or " \
                    "underscore followed with only characters, underscores and digits.\n\n" \
                    "Please try again." % \
                    (sResult)

                QMessageBox.critical(self, sTitle, sMsg)

                return ""

            # Check if attribute name is unique for this rendr layer
            if sResult in self.core.layer().attributes():
                sTitle = "Attribute name not unique"
                sMsg = "Your attribute name \"%s\" does already exists for this render layer. You can't have two " \
                       "attributes with the same name." % \
                       (sResult)

                QMessageBox.critical(self, sTitle, sMsg)

                return ""

            # If it passed above tests then this attribute name is valid and unique
            return sResult

        else:
            return ""

    def uiGetRenamedAttribute(self):
        # Adding extra space at the end to make the dialog extra wide :)
        lstResult = QInputDialog.getText(self, "Rename Attribute",
            "Enter the new name of the attribute:         ", QLineEdit.Normal,
            self.sSelectedAttribute)

        return self._getResult(lstResult)

    def uiIsAttributeSelected(self):
        return self.attributesList.currentRow() != -1

    def uiLoadAttributes(self, sDefaultAttribute = None):
        self.attributesList.blockSignals(True)

        self.attributesList.clear()
        self.overrideField.clear()
        self.revertField.clear()
        self.assignField.clear()

        lstAttributes = self.core.layer().attributes()

        for sAttribute in lstAttributes:
            self.attributesList.addItem(sAttribute)

        # Set default
        if sDefaultAttribute:
            self.attributesList.setCurrentRow(lstAttributes.index(sDefaultAttribute))

        self.attributesList.blockSignals(False)

    def uiLoadSelectedAttribute(self):
        if self.sSelectedAttribute:
            sAttributeOverride = self.core.layer().attributeOverrideValue(self.sSelectedAttribute)
            sAttributeRevert = self.core.layer().attributeRevertValue(self.sSelectedAttribute)
            sAttributeContent = self.core.layer().attributeAssignment(self.sSelectedAttribute)

        else:
            sAttributeOverride = ""
            sAttributeRevert = ""
            sAttributeContent = ""

        self.overrideField.setText(sAttributeOverride)
        self.revertField.setText(sAttributeRevert)
        self.assignField.setText(sAttributeContent)

    def uiRemoveSelectedAttribute(self):
        iIndex = self.attributesList.currentRow()
        self.attributesList.takeItem(iIndex)

        self.core.layer().removeAttribute(self.sSelectedAttribute)

    def uiSavePreviousSelectedAttribute(self):
        if self.sSelectedAttribute:
            sAttributeOverride = unicode(self.overrideField.text())
            sAttributeRevert = unicode(self.revertField.text())
            sAttributeContent = unicode(self.assignField.toPlainText())

            self.core.layer().setAttributeOverrideValue(self.sSelectedAttribute, sAttributeOverride)
            self.core.layer().setAttributeRevertValue(self.sSelectedAttribute, sAttributeRevert)
            self.core.layer().setAttributeAssignment(self.sSelectedAttribute, sAttributeContent)

    def uiSaveSelectedAttribute(self):
        item = self.attributesList.currentItem()

        if item:
            self.sSelectedAttribute = unicode(item.text())

        else:
            self.sSelectedAttribute = ""

    def uiSaveSelectedAttributeContent(self):
        if self.sSelectedAttribute:
            sValue = unicode(self.assignField.toPlainText())
            self.core.layer().setAttributeAssignment(self.sSelectedAttribute, sValue)

    def uiSetContent(self, sContent):
        self.assignField.setText(sContent)

    def uiShowContextMenu(self, iContextMenuIndex, position, evtPostAction = None):
        """
        Shows a context menu when right clicking self.attributesList
        """

        menu = QMenu()

        # Context menu for the list "Attributes"

        # Populate the context menu
        renameAction = menu.addAction("Rename Attribute...")
        menu.addSeparator()
        deleteAction = menu.addAction("Delete Attribute...")

        # Execute the context menu and retrieve the result
        result = menu.exec_(self.attributesList.mapToGlobal(position))

        # Check the result and return what we should do
        if result == renameAction:
            return 0

        elif result == deleteAction:
            return 1

    def uiValidate(self):
        item = self.attributesList.currentItem()

        if item:
            bEnable = True

        else:
            bEnable = False

        self.renameattrButton.setEnabled(bEnable)
        self.addobjectsButton.setEnabled(bEnable)
        self.orgobjectsButton.setEnabled(bEnable)
        self.overrideLabel.setEnabled(bEnable)
        self.overrideField.setEnabled(bEnable)
        self.revertLabel.setEnabled(bEnable)
        self.revertField.setEnabled(bEnable)
        self.assignLabel.setEnabled(bEnable)
        self.assignField.setEnabled(bEnable)

    def _getResult(self, lstResult):
        if lstResult[1]:
            return unicode(lstResult[0])

        else:
            return ""