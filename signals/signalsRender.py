#!/usr/bin/env python
# -*- coding: utf-8 -*-



class Signals(object):
    def __init__(self):
        self.layersList.itemDoubleClicked.connect(self.evtDoubleClickInList)
        self.renderCurrentButton.released.connect(self.evtRenderCurrentFrame)
        self.renderAllButton.released.connect(self.evtRenderAllFrames)
        self.cancelButton.released.connect(self.evtCancel)

    def evtCancel(self):
        """
        When user clicks the button "Cancel" to abort the dialog
        """

        self.uiCloseWindow()

    def evtDoubleClickInList(self):
        """
        When user double clicks an item in the render list to change the check
        box state rather than clicking the check box
        """

        self.uiSwitchSelectedCheckStateInList()

    def evtRenderAllFrames(self):
        """
        When user clicks the button "Render All Frames" to render all frames
        for all selected render layers
        """

        self.uiSaveSelectedRenders()

        self.core.render(self.lstSelectedRenders, bEverything = True)

    def evtRenderCurrentFrame(self):
        """
        When user clicks the button "Render Current Frame" to render the current
        frame for all selected render layers
        """

        self.uiSaveSelectedRenders()

        self.core.render(self.lstSelectedRenders, bCurrentFrame = True)