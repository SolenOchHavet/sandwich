#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""

UI handlers for "Overview"

"""

try:
    from PyQt4.QtCore import Qt
    from PyQt4.QtGui import *

except:
    from PySide.QtCore import Qt
    from PySide.QtGui import *


class UI(object):
    def __init__(self):
        pass

    def uiLoadOverview(self):
        if self.parent.sSelectedLayerName == "masterLayer":
            self.descriptionField.clear()

            return

        # Set the data for the Overview tab
        self.descriptionField.setText(self.core.layer().comments())

    def uiSaveTabContent(self):
        self.core.layer().setComments(unicode(self.descriptionField.toPlainText()))