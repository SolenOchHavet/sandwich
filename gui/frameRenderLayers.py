#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""

Frame "Render Layers"

This frame contains the render layer list. By having this as a separate frame, we
can easily switch the visibility on it in order to save space in the main window.

"""

try:
    from PyQt4.QtGui import *

except:
    from PySide.QtGui import *


class RenderLayersFrame(QFrame):
    def __init__(self, parent = None):
        QFrame.__init__(self)

        self.parent = parent

        # Layout Widgets
        self.mainLayout = QVBoxLayout()

        # Widgets
        self.dataLabel = QLabel("Render Layers")
        self.dataTree = QTreeWidget()

        # Widget Settings
        self.dataTree.setFixedWidth(200)

        # Widget Status Tips
        self.dataTree.setStatusTip("Shows all render layers in this scene. Select one to trigger it.")

        # Layout the Widgets
        self.mainLayout.addWidget(self.dataLabel)
        self.mainLayout.addWidget(self.dataTree)

        # Layout Settings
        self.mainLayout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.mainLayout)