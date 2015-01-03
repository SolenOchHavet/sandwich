#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""

Frame "Render Globals"

This frame will show all overrides user has done in the Render Globals.
The QGridLayout widget "scrollLayout" is used for adding all the Render Globals
that the user has overridden for the selected render layer.

"""

try:
    from PyQt4.QtCore import *
    from PyQt4.QtGui import *

except:
    from PySide.QtCore import *
    from PySide.QtGui import *

import sandwich.libs.uiRenderGlobals as ui
reload(ui)


class RenderGlobalsFrame(QFrame, ui.UI):
    def __init__(self, parent = None, core = None, text = None):
        QFrame.__init__(self)

        self.parent = parent
        self.core = core
        self.text = text

        # Layout Widgets
        self.mainLayout = QVBoxLayout()

        # Widgets
        self.bodyWidget = QWidget()
        self.scrollLayout = QGridLayout(self.bodyWidget)
        self.areaScroll = QScrollArea()

        # Widget Settings
        self.areaScroll.setWidgetResizable(True)
        self.areaScroll.setWidget(self.bodyWidget)

        # Layout
        self.mainLayout.addWidget(self.areaScroll, 1)

        # Layout Settings
        self.scrollLayout.setColumnStretch(0, 1)
        self.scrollLayout.setColumnStretch(1, 3)
        self.scrollLayout.setSpacing(1)
        self.setLayout(self.mainLayout)

        ui.UI.__init__(self)