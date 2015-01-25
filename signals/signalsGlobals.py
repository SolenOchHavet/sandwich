#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""

Signals for "Globals"

"""


class Signals(object):
    def __init__(self):
        self.rendersButton.released.connect(self.sgnBrowseRenders)
        self.scenesButton.released.connect(self.sgnBrowseScenes)
        self.cameraButton.released.connect(self.sgnBrowseCamera)
        self.cancelButton.released.connect(self.sgnCancel)
        self.saveButton.released.connect(self.sgnSave)

    def sgnBrowseCamera(self):
        """
        When user clicks the button "Browse" at the "Default Camera" line to
        select the default camera that will be used to render a render layer.
        Can later be overridden at layer level
        """

        sCamera = self.uiGetNewCamera()

        if sCamera:
            self.uiSetCamera(sCamera)

    def sgnBrowseRenders(self):
        """
        When user clicks the button "Browse" at the "Output Renders" line to
        select a directory for where the renders will be outputed
        """

        sNewRendersFolder = self.uiGetNewRendersFolder()

        if sNewRendersFolder:
            self.uiSetRendersFolder(sNewRendersFolder)

    def sgnBrowseScenes(self):
        """
        When user clicks the button "Browse" at the "Output Scenes" line to
        select a directory for where the scenes will be outputed
        """

        sNewScenesFolder = self.uiGetNewScenesFolder()

        if sNewScenesFolder:
            self.uiSetScenesFolder(sNewScenesFolder)

    def sgnCancel(self):
        """
        When user clicks the button "Cancel" to abort the dialog
        """

        self.uiCloseWindow()

    def sgnSave(self):
        """
        When user clicks the button "Save" to save the new settings that are
        inside the Globals dialog
        """

        self.uiSaveSelectedCamera()
        self.uiSaveSelectedRendersFolder()
        self.uiSaveSelectedScenesFolder()
        self.uiSaveSelectedTerminalApp()
        self.uiSaveSelectedSettings()
        self.uiSaveSelectedRenderEngine()

        bResult = self.uiGetCheckResults()

        if bResult:
            self.core.setGlobalsValue("sDefaultEngine", self.sSelectedRenderEngine)

            self.core.setGlobalsValue("sOutputRenders", self.sSelectedRendersFolder)
            self.core.setGlobalsValue("sOutputScenes", self.sSelectedScenesFolder)
            self.core.setGlobalsValue("sDefaultCamera", self.sSelectedCamera)

            self.core.setGlobalsValue("iWidth", int(self.sSelectedWidth))
            self.core.setGlobalsValue("iHeight", int(self.sSelectedHeight))

            self.core.setGlobalsValue("iStart", int(self.sSelectedStart))
            self.core.setGlobalsValue("iEnd", int(self.sSelectedEnd))
            self.core.setGlobalsValue("iStep", int(self.sSelectedStep))

            self.core.setGlobalsValue("sTerminalApp", self.sSelectedTerminalApp)

            self.core.setGlobalsValue("bSettingImportRefs", self.bSelectedSettingImportRefs)

            self.core.saveGlobals()

            self.uiCloseWindow()