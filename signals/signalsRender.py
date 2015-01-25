#!/usr/bin/env python
# -*- coding: utf-8 -*-



class Signals(object):
    def __init__(self):
        self.layersList.itemDoubleClicked.connect(self.sgnDoubleClickInList)
        self.renderCurrentButton.released.connect(self.sgnRenderCurrentFrame)
        self.renderAllButton.released.connect(self.sgnRenderAllFrames)
        self.cancelButton.released.connect(self.sgnCancel)

    def sgnCancel(self):
        """
        When user clicks the button "Cancel" to abort the dialog
        """

        self.uiCloseWindow()

    def sgnDoubleClickInList(self):
        """
        When user double clicks an item in the render list to change the check
        box state rather than clicking the check box
        """

        self.uiSwitchSelectedCheckStateInList()

    def sgnRenderAllFrames(self):
        """
        When user clicks the button "Render All Frames" to render all frames
        for all selected render layers
        """

        self.uiSaveSelectedRenders()

        self.core.render(self.lstSelectedRenders, bEverything = True)

    def sgnRenderCurrentFrame(self):
        """
        When user clicks the button "Render Current Frame" to render the 
        current frame for all selected render layers
        """

        self.uiSaveSelectedRenders()

        self.core.render(self.lstSelectedRenders, bCurrentFrame = True)