#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""

UI handlers for tab "Visibility"

"""


import re


class UI(object):
    def __init__(self):
        pass

    def uiAddContent(self, sNewContent):
        sCurrentContent = unicode(self.visibilityField.toPlainText()).strip()

        if sCurrentContent:
            sCurrentContent += "\n"

        self.visibilityField.setText(sCurrentContent + sNewContent)

    def uiGetContentAsList(self):
        """
        Returns a list of all objects specifies in the text field.
        Any Python comment inside the text field will be removed.
        """

        return self.core.utils.objectsOnly(unicode(self.visibilityField.toPlainText()))

    def uiGetContentAsString(self):
        """
        Returns a list of all objects specifies in the text field.
        Any Python comment inside the text field will be removed.
        """

        return unicode(self.visibilityField.toPlainText())

    def uiLoadContent(self):
        self.visibilityField.setText(self.core.layer().visibility())

    def uiSaveTabContent(self):
        sNewContent = unicode(self.visibilityField.toPlainText())

        self.core.layer().setVisibility(sNewContent)

    def uiSetContent(self, sContent):
        self.visibilityField.setText(sContent)