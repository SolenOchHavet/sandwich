#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""

Signals for "Attributes"

"""

try:
    from PyQt4.QtCore import Qt

except:
    from PySide.QtCore import Qt


class Signals(object):
    def __init__(self):
        self.addattrButton.released.connect(self.evtAddNewAttribute)
        self.renameattrButton.released.connect(self.evtRenameAttribute)
        self.addobjectsButton.released.connect(self.evtAddObjects)
        self.orgobjectsButton.released.connect(self.evtReorganizeObjects)
        self.attributesList.itemSelectionChanged.connect(self.evtSelectAttribute)
        self.attributesList.setContextMenuPolicy(Qt.CustomContextMenu)
        self.attributesList.customContextMenuRequested.connect(self.evtContextMenu)

    def evtAddNewAttribute(self):
        """
        When user clicks the button "Add Attribute" below the Attribute tab.
        Let's user add a new attribute
        """

        sNewAttribute = self.uiGetNewAttribute()

        if sNewAttribute:
            self.uiSavePreviousSelectedAttribute()

            self.core.layer().addAttribute(sNewAttribute)

            self.uiLoadAttributes(sNewAttribute)
            self.uiSaveSelectedAttribute()
            self.uiLoadSelectedAttribute()

            self.uiValidate()

    def evtAddObjects(self):
        """
        When user clicks the button "Add Objects" to add selected objects from
        the scene. Adds only objects that does not yet exists in the list.
        Supports object expressions.
        """

        # Get what we currently have in the interface and what's selected
        # within the scene
        lstCurrentContent = self.uiGetAttributeContentAsList()
        lstNewObjects = self.core.getSceneSelectedObjects()

        # Compare the two lists and only add objects that are not already in
        # there
        sNewContent = self.core.getOnlyNew(lstCurrentContent, lstNewObjects)

        if sNewContent:
            self.uiAddAttributeContent(sNewContent)
            self.uiSaveSelectedAttributeContent()

        else:
            print "Sandwich: No new objects were added because they have already been added!"

    def evtContextMenu(self, position):
        """
        When user right clicks the list "Attributes" to get the context menu. The context menu contains the items:
         * Delete Attribute... (code 0). Will remove the attribute after the user confirms the action. However it wont
           be removed for real until user saves the render layer.
        """

        iCode = self.uiShowContextMenu(2, position)

        # Abort if no attribute is selected!
        if not self.uiIsAttributeSelected():
            return

        if iCode == 0:
            self.evtRenameAttribute()

        elif iCode == 1:
            self.evtRemoveAttribute()

    def evtRemoveAttribute(self):
        """
        When user clicks the item "Remove Attribute" from the context menu to
        remove selected attribute from the current render layer.

        Note: The changes are not saved until "Save Layer" has been clicked.
        """

        sTitle = "Remove Attribute?"
        sMessage = "Are you sure you wish to remove attribute \"%s\"?" % \
            (self.sSelectedAttribute)

        if self.uiAsk(sTitle, sMessage):
            self.uiRemoveSelectedAttribute()

            self.uiSaveSelectedAttribute()
            self.uiLoadSelectedAttribute()
            self.uiValidateAttributeTab()

    def evtRenameAttribute(self):
        """
        When user clicks the item "Rename Attribute" from the context menu to
        rename selected attribute.

        Note: The changes are not saved until "Save Layer" has been clicked.
        """

        sRenamedAttribute = self.uiGetRenamedAttribute()

        if sRenamedAttribute:
            self.core.layer().renameAttribute(self.sSelectedAttribute,
                sRenamedAttribute)

            self.uiLoadAttributes(sRenamedAttribute)
            self.uiSaveSelectedAttribute()
            self.uiLoadSelectedAttribute()

    def evtReorganizeObjects(self):
        """
        When user clicks the button "Reorganize Objects" to organize them
        alphabetically in the text fields
        """

        sNewContent = self.core.getReorganizedContent(
            self.uiGetAttributeContentAsString())

        self.uiSetContent(sNewContent)
        self.uiSaveSelectedAttributeContent()

    def evtSelectAttribute(self):
        """
        When user selected an attribute in the Attribute List. Will make the textfields
        "Override Value", "Revert Value" and "Assign to These Objects" to show all data
        related to the attribute
        """

        # When user change selected shader we have to make sure to save his/her
        # changes by running this special command
        self.uiSavePreviousSelectedAttribute()

        self.uiSaveSelectedAttribute()
        self.uiLoadSelectedAttribute()

        self.uiValidate()