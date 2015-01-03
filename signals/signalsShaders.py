#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""

Signals for "Shaders"

"""

try:
    from PyQt4.QtCore import Qt

except:
    from PySide.QtCore import Qt


class Signals(object):
    def __init__(self):
        self.addshaderButton.released.connect(self.evtAddNewShader)
        self.renameshaderButton.released.connect(self.evtRenameShader)
        self.addobjectsButton.released.connect(self.evtAddObjects)
        self.orgobjectsButton.released.connect(self.evtReorganizeObjects)
        self.shaderList.itemActivated.connect(self.evtRenameShader)
        self.shaderList.itemSelectionChanged.connect(self.evtSelectShader)
        self.shaderList.setContextMenuPolicy(Qt.CustomContextMenu)
        self.shaderList.customContextMenuRequested.connect(self.evtContextMenu)

    def evtAddNewShader(self):
        """
        When user clicks the button "Add Shader..." to add a new shader to
        the current render layer
        """

        sNewShader = self.uiGetNewShader()

        if sNewShader:
            self.uiSavePreviousSelectedShader()

            self.core.layer().addShader(sNewShader)

            self.uiLoadShaders(sNewShader)
            self.uiSaveSelectedShader()
            self.uiLoadSelectedShader()

            self.uiValidate()

    def evtAddObjects(self):
        """
        When user clicks the button "Add Objects..." to add selected objects from the
        Maya scene into the selected shader's "Assign to these Objects" textfield.
        Adds only objects that does not yet exists in the list. Supports object
        expressions.
        """

        # Get what we currently have in the interface and what's selected
        # within the scene
        lstCurrentContent = self.uiGetShaderContentAsList()
        lstNewObjects = self.core.getSceneSelectedObjects()

        # Compare the two lists and only add objects that are not already in
        # there
        sNewContent = self.core.getOnlyNew(lstCurrentContent,
            lstNewObjects)

        if sNewContent:
            self.uiAddShaderContent(sNewContent)
            self.uiSaveSelectedShaderContent()

        else:
            print "Sandwich: No new objects were added because they have already been added!"

    def evtContextMenu(self, position):
        """
        When user right clicks the list "Shaders" to get the context menu. The
        context menu contains the items:
         * 0: Rename Shader
         * 1: Transfer Shader
         * 2: Delete Shader
        """

        iCode = self.uiShowContextMenu(position)

        if iCode == 0:
            self.evtRenameShader()

        if iCode == 1:
            self.evtTransferShader()

        if iCode == 2:
            self.evtRemoveShader()

    def evtRemoveShader(self):
        """
        When user clicks the item "Rename Shader..." from the context menu to remove
        selected shader from the current render layer.
        """

        # Abort if no shader is selected!
        if not self.uiIsShaderSelected():
            return

        sTitle = "Remove Shader?"
        sMessage = "Are you sure you wish to remove shader \"%s\"?" % \
            (self.sSelectedShader)

        if self.uiAsk(sTitle, sMessage):
            self.uiRemoveSelectedShader()
            self.uiSaveSelectedShader()
            self.uiLoadSelectedShader()
            self.uiValidate()

    def evtRenameShader(self):
        """
        When user clicks the item "Rename Shader..." from the context menu to rename
        selected shader.
        """

        sRenamedShader = self.uiGetRenamedShaders()

        if sRenamedShader:
            self.core.layer().renameShader(self.sSelectedShader, sRenamedShader)

            self.uiLoadShaders(sRenamedShader)
            self.uiSaveSelectedShader()
            self.uiLoadSelectedShader()

    def evtReorganizeObjects(self):
        """
        When user clicks the button "Reorganize Objects" to organize the objects field.
        Takes Python comments into consideration when the sorting is done.
        """

        sNewContent = self.core.getReorganizedContent(self.uiGetShaderContentAsString())

        self.uiSetShaderContent(sNewContent)
        self.uiSaveSelectedShaderContent()

    def evtSelectShader(self):
        """
        When user selected a shader in the Shader List below the Shaders tab. Will make
        the textfield "Assign to These Objects" to show which objects the selected
        shader should be applied to.
        """

        # When user change selected shader we have to make sure to save his/her
        # changes by running this special command
        self.uiSavePreviousSelectedShader()

        self.uiSaveSelectedShader()
        self.uiLoadSelectedShader()

        self.uiValidate()

    def evtTransferShader(self):
        """
        When user clicks the item "Transfer Shader..." in the context menu of a selected
        shader in order to copy it into another layer. If it already exists there, user
        will be asked before it gets transfered.
        """

        sDestinationLayer = self.uiGetDestinationLayer()

        if not sDestinationLayer:
            return

        # Check if selected shader already exists for the destination layer
        if self.core.existsShaderInLayer(self.sSelectedShader, sDestinationLayer):
            # If the shader exists, ask the user if we can proceed. Otherwise abort
            bResult = self.uiAsk("Continue transfer?", "The shader \"%s\" does " \
                "already exists for render layer \"%s\". Do you wish to " \
                "overwrite it?\n\nThe transfer will be saved without " \
                "affecting the current layer." %
                (self.sSelectedShader, sDestinationLayer))

            if bResult:
                self.core.transferShader(self.sSelectedShader, sDestinationLayer)

        else:
            # Selected shader does not yet exists for destination layer. We are
            # free to transfer it without asking
            self.core.transferShader(self.sSelectedShader, sDestinationLayer)