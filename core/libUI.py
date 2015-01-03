#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""

Library "UI"

This sub library handles the UI settings in Sandwich

"""


class UICore(object):
    def __init__(self, parent):
        self.parent = parent
        
        self.bToolbarVisible = True
        self.bRenderLayersVisible = True

    def isRenderLayersVisible(self):
        return self.bRenderLayersVisible

    def isToolbarVisible(self):
        return self.bToolbarVisible

    def setRenderLayersVisible(self, bState):
        self.bRenderLayersVisible = bState

    def setToolbarVisible(self, bState):
        self.bToolbarVisible = bState