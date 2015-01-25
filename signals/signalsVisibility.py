#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""

Signals for "Visibility"

"""


class Signals(object):
    def __init__(self):
        self.addobjectsButton.released.connect(self.sgnAddObjects)
        self.orgobjectsButton.released.connect(self.sgnReorganizeObjects)

    def sgnAddObjects(self):
        """
        When user clicks the button "Add Objects" to add selected objects in
        the scene into this tab. Adds only objects that does not yet exists
        in the list. Supports object expressions.
        """

        lstCurrentContent = self.uiGetContentAsList()
        lstNewObjects = self.core.getSceneSelectedObjects()

        sNewContent = self.core.getOnlyNew(lstCurrentContent,
            lstNewObjects)

        if sNewContent:
            self.uiAddContent(sNewContent)
            self.uiSaveTabContent()

        else:
            print "Sandwich: No new objects were added because they have " \
                "already been added!"

    def sgnReorganizeObjects(self):
        """
        When user clicks the button "Reorganize Objects" to organize them
        alphabetically in the text fields
        """

        sNewContent = self.core.utils.reorganizeContent(
            self.uiGetContentAsString())

        self.uiSetContent(sNewContent)
        self.uiSaveTabContent()