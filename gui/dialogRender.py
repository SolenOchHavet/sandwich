#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""

Dialog "Render"

The interface for rendering out each render layer.

"""

try:
    from PyQt4.QtCore import QRegExp
    from PyQt4.QtGui import *

except:
    from PySide.QtCore import QRegExp
    from PySide.QtGui import *

import sandwich.signals.signalsRender as signalsRender
import sandwich.libs.uiRender as uiRender
reload(signalsRender)
reload(uiRender)



class RenderDialog(QDialog, signalsRender.Signals, uiRender.UI):
    def __init__(self, parent = None, core = None):
        QDialog.__init__(self, parent)

        self.core = core

        # Layout Widgets
        self.mainLayout = QVBoxLayout()
        self.buttonsLayout = QHBoxLayout()

        # Widgets
        self.layersLabel = QLabel("Select Render Layers to Render")
        self.layersList = QTreeWidget()
        self.tipLabel = QLabel("TIP: Double click a line to change it's check status.")
        self.pathLabel = QLabel("Output Location: <font color='#bbc26e'>/haha/hhu/hmh../..</font>")

        self.renderCurrentButton = QPushButton("Render Current Frame")
        self.renderAllButton = QPushButton("Render All Frames")
        self.cancelButton = QPushButton("Close")

        # Widget Settings
        self.setMinimumWidth(700)
        self.layersList.setColumnCount(5)
        self.layersList.setHeaderLabels(["Render", "Render Layer", "Camera", "Resolution", "Range"])
        self.layersList.setColumnWidth(0, 60)
        self.layersList.setColumnWidth(2, 150)
        self.layersList.header().setStretchLastSection(False)
        self.layersList.header().setResizeMode(1, QHeaderView.Stretch)

        # Widget Status Tips
        self.layersLabel.setStatusTip("Select which render layers should be rendered.")
        self.layersList.setStatusTip("Select which render layers should be rendered.")
        self.pathLabel.setStatusTip("Your rendered files will be located here. You can change the location in Globals.")
        self.renderCurrentButton.setStatusTip("Render the current frame for selected render layers to disk.")
        self.renderAllButton.setStatusTip("Render the full frame range for each selected render layers to disk.")
        self.cancelButton.setStatusTip("Close this dialog without doing anything.")

        # Layout the Widgets
        self.buttonsLayout.addStretch(1)
        self.buttonsLayout.addWidget(self.renderCurrentButton)
        self.buttonsLayout.addWidget(self.renderAllButton)
        self.buttonsLayout.addWidget(self.cancelButton)

        self.mainLayout.addWidget(self.layersLabel)
        self.mainLayout.addWidget(self.layersList)
        self.mainLayout.addWidget(self.tipLabel)
        self.mainLayout.addSpacing(5)
        self.mainLayout.addWidget(self.pathLabel)
        self.mainLayout.addLayout(self.buttonsLayout)

        # Dialog Settings
        self.setLayout(self.mainLayout)
        self.setWindowTitle("Render")

        signalsRender.Signals.__init__(self)
        uiRender.UI.__init__(self)