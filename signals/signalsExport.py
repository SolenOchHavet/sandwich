#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""

Signals for "Export"

"""


class Signals(object):
    def __init__(self):
        self.layersTree.itemDoubleClicked.connect(self.sgnDoubleClickInList)
        self.exportMaButton.released.connect(self.sgnExportAsMa)
        self.exportMbButton.released.connect(self.sgnExportAsMb)
        self.cancelButton.released.connect(self.sgnCancel)

    def sgnCancel(self):
        """
        When user clicks the button "Cancel" to abort the dialog
        """

        self.uiCloseWindow()

    def sgnDoubleClickInList(self):
        """
        When user double clicks an item in the export list to change the check
        box state rather than clicking the check box
        """

        self.uiSwitchSelectedCheckStateInList()

    def sgnExportAsMa(self):
        """
        When user clicks the button "Export as .ma" to export selected render
        layers as Maya Ascii files
        """

        self.uiSaveSelectedExports()
        self.sSelectedFileType = "Maya Ascii"

        if not self.lstSelectedExports:
            return

        self.core.export(self.lstSelectedExports, bAsAscii = True)
        self.core.layer().select(self.parent.sSelectedLayerName)
        self.core.layer().execute()

        self.uiShowResults()

    def sgnExportAsMb(self):
        """
        When user clicks the button "Export as .mb" to export selected render
        layers as Maya Binary files
        """

        self.uiSaveSelectedExports()
        self.sSelectedFileType = "Maya Binary"

        if not self.lstSelectedExports:
            return

        self.core.export(self.lstSelectedExports, bAsBinary = True)
        self.core.layer().select(self.parent.sSelectedLayerName)
        self.core.layer().execute()

        self.uiShowResults()