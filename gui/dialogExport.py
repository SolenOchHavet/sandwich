#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""

Dialog "Export"

The interface for exporting out each render layer to Maya files. This is sometimes helpful when sending the renders
to the farm using another application.

"""

try:
    from PyQt4.QtCore import QRegExp
    from PyQt4.QtGui import *

except:
    from PySide.QtCore import QRegExp
    from PySide.QtGui import *

import sandwich.signals.signalsExport as signalsExport
import sandwich.libs.uiExport as uiExport
reload(signalsExport)
reload(uiExport)



class ExportDialog(QDialog, signalsExport.Signals, uiExport.UI):
    def __init__(self, parent = None, core = None):
        QDialog.__init__(self, parent)

        self.parent = parent
        self.core = core

        # Layout Widgets
        self.mainLayout = QVBoxLayout()
        self.buttonsLayout = QHBoxLayout()

        # Widgets
        self.layersLabel = QLabel("Select Render Layers to Export")
        self.layersTree = QTreeWidget()
        self.tipLabel = QLabel("TIP: Double click a line to change it's check status.")
        self.pathLabel = QLabel("Output Location: <font color='#bbc26e'><please set \"Output Scene\" in Globals to a directory></font>")

        self.exportMaButton = QPushButton("Export as .ma")
        self.exportMbButton = QPushButton("Export as .mb")
        self.cancelButton = QPushButton("Close")

        # Widget Settings
        self.setMinimumWidth(700)
        self.layersTree.setColumnCount(3)
        self.layersTree.setHeaderLabels(["Export", "Render Layer", "File Name"])
        self.layersTree.setColumnWidth(0, 50)
        self.layersTree.setColumnWidth(1, 250)

        # Widget Status Tips
        self.layersLabel.setStatusTip("Select which render layers should be exported.")
        self.layersTree.setStatusTip("Select which render layers should be exported.")
        self.pathLabel.setStatusTip("Your exported files will be written out here. You can change the location in Globals.")
        self.exportMaButton.setStatusTip("Export selected render layers as Maya Ascii files.")
        self.exportMbButton.setStatusTip("Export selected render layers as Maya Binary files.")
        self.cancelButton.setStatusTip("Close this dialog without doing anything.")

        # Layout the Widgets
        self.buttonsLayout.addStretch(1)
        self.buttonsLayout.addWidget(self.exportMaButton)
        self.buttonsLayout.addWidget(self.exportMbButton)
        self.buttonsLayout.addWidget(self.cancelButton)

        self.mainLayout.addWidget(self.layersLabel)
        self.mainLayout.addWidget(self.layersTree)
        self.mainLayout.addWidget(self.tipLabel)
        self.mainLayout.addSpacing(5)
        self.mainLayout.addWidget(self.pathLabel)
        self.mainLayout.addLayout(self.buttonsLayout)

        # Dialog Settings
        self.setLayout(self.mainLayout)
        self.setWindowTitle("Export")

        signalsExport.Signals.__init__(self)
        uiExport.UI.__init__(self)