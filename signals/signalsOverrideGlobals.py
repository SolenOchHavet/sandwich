#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""

Signals for "Override Globals"

"""

try:
    from PyQt4.QtCore import Qt

except:
    from PySide.QtCore import Qt


class Signals(object):
    def __init__(self):
        self.cameraCheck.stateChanged.connect(self.evtChangeRenderSettings)
        self.cameraButton.released.connect(self.evtSelectCamera)
        self.resolutionCheck.stateChanged.connect(self.evtChangeRenderSettings)
        self.rangeCheck.stateChanged.connect(self.evtChangeRenderSettings)
        self.engineCheck.stateChanged.connect(self.evtChangeRenderSettings)

    def evtChangeRenderSettings(self):
        """
        When user clicks any of the check boxes next to the settings to activate or
        inactivate any of them.
        """

        self.uiValidate()

    def evtSelectCamera(self):
        """
        When user clicks the button "Browse..." to browse for a camera. If done
        on this level, it will override the camera that was set in Global Settings
        for this render layer.
        """

        sCamera = self.uiGetCamera()

        if sCamera:
            self.uiSetOverrideCamera(sCamera)