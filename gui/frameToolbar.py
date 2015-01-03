#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""

Frame "Toolbar"

This frame contains the toolbar buttons of Sandwich. By having this as a separate
frame, we can switch the visibility on it in order to save space in the main window.

"""

try:
    from PyQt4.QtGui import *

except:
    from PySide.QtGui import *


class ToolbarFrame(QFrame):
    def __init__(self, parent = None, text = None):
        QFrame.__init__(self)

        self.parent = parent
        self.text = text
        
        # Layout Widgets
        self.mainLayout = QVBoxLayout()
        self.buttonsLayout = QHBoxLayout()

        # Widgets
        self.newlayerButton = QPushButton("New Layer...")
        self.renamelayerButton = QPushButton("Rename Layer...")
        self.savelayerButton = QPushButton("Save Layer")

        self.renderButton = QPushButton("Render...")
        self.exportButton = QPushButton("Export...")
        self.globalsButton = QPushButton("Globals...")

        # Widget Settings
        self.newlayerButton.setFixedSize(100, 32)
        self.renamelayerButton.setFixedSize(100, 32)
        self.savelayerButton.setFixedSize(100, 32)
        self.renderButton.setFixedSize(100, 32)
        self.exportButton.setFixedSize(100, 32)
        self.globalsButton.setFixedSize(100, 32)

        # Widget Status Tips
        self.newlayerButton.setStatusTip("Create a new render layer. If created, it will become the active one.")
        self.renamelayerButton.setStatusTip("Rename the selected render layer. Name must be unique and never \"masterLayer\".")
        self.savelayerButton.setStatusTip("Save and apply the latest changes to the selected render layer.")
        self.renderButton.setStatusTip("Shows the render dialog. Used to render out the render layers.")
        self.exportButton.setStatusTip("Shows the export dialog. Used to export the render layers to new Maya files.")
        self.globalsButton.setStatusTip("Shows the global settings dialog.")

        # Layout the Widgets
        self.buttonsLayout.addWidget(self.newlayerButton)
        self.buttonsLayout.addWidget(self.renamelayerButton)
        self.buttonsLayout.addWidget(self.savelayerButton)
        self.buttonsLayout.addStretch(1)
        self.buttonsLayout.addWidget(self.renderButton)
        self.buttonsLayout.addWidget(self.exportButton)
        self.buttonsLayout.addSpacing(10)
        self.buttonsLayout.addWidget(self.globalsButton)

        self.mainLayout.addLayout(self.buttonsLayout)
        self.mainLayout.addSpacing(10)

        # Layout Settings
        self.mainLayout.setContentsMargins(0, 0, 0, 0)
        self.buttonsLayout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.mainLayout)