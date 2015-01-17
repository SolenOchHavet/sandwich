#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""

Dialog "Globals"

The interface for the global settings for Sandwich.

"""

try:
    from PyQt4.QtCore import QRegExp
    from PyQt4.QtGui import *

except:
    from PySide.QtCore import QRegExp
    from PySide.QtGui import *

import sandwich.signals.signalsGlobals as signalsGlobals
import sandwich.libs.uiGlobals as uiGlobals
reload(signalsGlobals)
reload(uiGlobals)



class GlobalsDialog(QDialog, signalsGlobals.Signals, uiGlobals.UI):
    def __init__(self, parent = None, core = None):
        QDialog.__init__(self)

        self.core = core

        # Layout Widgets
        self.mainLayout = QVBoxLayout()
        self.gridLayout = QGridLayout()
        self.row1Layout = QHBoxLayout()
        self.row2Layout = QHBoxLayout()
        self.row3Layout = QHBoxLayout()
        self.buttonsLayout = QHBoxLayout()

        # Widgets
        self.engineLabel = QLabel("Default Engine")
        self.engineCombo = QComboBox()
        self.rendersLabel = QLabel("Output Renders")
        self.rendersField = QLineEdit()
        self.rendersButton = QPushButton("Browse")
        self.scenesLabel = QLabel("Output Scenes")
        self.scenesField = QLineEdit()
        self.scenesButton = QPushButton("Browse")
        self.cameraLabel = QLabel("Default Camera")
        self.cameraField = QLineEdit()
        self.cameraButton = QPushButton("Browse")
        self.resolutionLabel = QLabel("Default Resolution")
        self.widthField = QLineEdit("1024")
        self.heightField = QLineEdit("576")
        self.rangeLabel = QLabel("Default Range")
        self.startField = QLineEdit("1")
        self.endField = QLineEdit("10")
        self.stepField = QLineEdit("1")
        self.terminalLabel = QLabel("Terminal App")
        self.terminalField = QLineEdit("")
        self.settingsLabel = QLabel("Settings")
        self.mergeCheck = QCheckBox("Import references into the scene on export")
        self.spaceLabel = QLabel(" ")

        self.cancelButton = QPushButton("Cancel")
        self.saveButton = QPushButton("Save")

        # Widget Settings
        rangeValidator = QRegExpValidator(QRegExp("-?[0-9]+"), self)
        resValidator = QRegExpValidator(QRegExp("[0-9]+"), self)
        nameValidator = QRegExpValidator(QRegExp("[a-z,A-Z,_,\|][a-z,A-Z,_,\|,0-9]*"), self)

        self.widthField.setMinimumWidth(10)
        self.heightField.setMinimumWidth(10)
        self.startField.setMinimumWidth(10)
        self.endField.setMinimumWidth(10)
        self.stepField.setMinimumWidth(10)

        self.cameraField.setValidator(nameValidator)
        self.widthField.setValidator(resValidator)
        self.heightField.setValidator(resValidator)
        self.startField.setValidator(rangeValidator)
        self.endField.setValidator(rangeValidator)
        self.stepField.setValidator(rangeValidator)

        # Widget Status Tips
        self.engineLabel.setStatusTip("Select the default render engine for all render layers.")
        self.engineCombo.setStatusTip("Select the default render engine for all render layers.")
        self.rendersLabel.setStatusTip("Set the default output path for renders.")
        self.rendersField.setStatusTip("Set the default output path for renders.")
        self.rendersButton.setStatusTip("Set the default output path for renders by browsing to the folder.")
        self.scenesLabel.setStatusTip("Set the default output path for exported files.")
        self.scenesField.setStatusTip("Set the default output path for exported files.")
        self.scenesButton.setStatusTip("Set the default output path for exported files by browsing to the folder.")
        self.cameraLabel.setStatusTip("Set the default render camera.")
        self.cameraField.setStatusTip("Set the default render camera.")
        self.cameraButton.setStatusTip("Select the default render camera from a list.")
        self.resolutionLabel.setStatusTip("Set the default resolution.")
        self.widthField.setStatusTip("Set the width of the default resolution.")
        self.heightField.setStatusTip("Set the height of the default resolution.")
        self.rangeLabel.setStatusTip("Set the default frame range for all render layers.")
        self.startField.setStatusTip("Set the default start frame for all render layers.")
        self.endField.setStatusTip("Set the default end frame for all render layers.")
        self.stepField.setStatusTip("Set the default frame step for all render layers.")
        self.terminalLabel.setStatusTip("Set the command to let Sandwich start a terminal. $BATCHFILE is the path to the batch render file Sandwich creates.")
        self.terminalField.setStatusTip("Set the command to let Sandwich start a terminal. $BATCHFILE is the path to the batch render file Sandwich creates.")
        self.settingsLabel.setStatusTip("Additional settings")
        self.mergeCheck.setStatusTip("Imports the references into the scene before exporting the files. Default: off")
        self.cancelButton.setStatusTip("Close dialog without saving anything.")
        self.saveButton.setStatusTip("Saves the new settings and closes this dialog.")

        # Layout the Widgets
        self.row1Layout.addWidget(self.rendersField, 1)
        self.row1Layout.addWidget(self.rendersButton)
        self.row2Layout.addWidget(self.scenesField, 1)
        self.row2Layout.addWidget(self.scenesButton)
        self.row3Layout.addWidget(self.cameraField, 1)
        self.row3Layout.addWidget(self.cameraButton)

        self.gridLayout.addWidget(self.engineLabel, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.engineCombo, 0, 1, 1, 3)
        self.gridLayout.addWidget(self.rendersLabel, 1, 0, 1, 1)
        self.gridLayout.addLayout(self.row1Layout, 1, 1, 1, 3)
        self.gridLayout.addWidget(self.scenesLabel, 2, 0, 1, 1)
        self.gridLayout.addLayout(self.row2Layout, 2, 1, 1, 3)
        self.gridLayout.addWidget(self.cameraLabel, 3, 0, 1, 1)
        self.gridLayout.addLayout(self.row3Layout, 3, 1, 1, 3)
        self.gridLayout.addWidget(self.resolutionLabel, 4, 0, 1, 1)
        self.gridLayout.addWidget(self.widthField, 4, 1, 1, 1)
        self.gridLayout.addWidget(self.heightField, 4, 2, 1, 1)
        self.gridLayout.addWidget(self.rangeLabel, 5, 0, 1, 1)
        self.gridLayout.addWidget(self.startField, 5, 1, 1, 1)
        self.gridLayout.addWidget(self.endField, 5, 2, 1, 1)
        self.gridLayout.addWidget(self.stepField, 5, 3, 1, 1)
        self.gridLayout.addWidget(self.spaceLabel, 6, 0, 1, 1)
        self.gridLayout.addWidget(self.settingsLabel, 7, 0, 1, 1)
        self.gridLayout.addWidget(self.mergeCheck, 7, 1, 1, 3)
        self.gridLayout.addWidget(self.terminalLabel, 8, 0, 1, 1)
        self.gridLayout.addWidget(self.terminalField, 8, 1, 1, 3)

        self.buttonsLayout.addStretch(1)
        self.buttonsLayout.addWidget(self.cancelButton)
        self.buttonsLayout.addWidget(self.saveButton)

        self.mainLayout.addLayout(self.gridLayout)
        self.mainLayout.addStretch(1)
        self.mainLayout.addLayout(self.buttonsLayout)

        # Layout Settings
        self.gridLayout.setColumnStretch(1, 1)
        self.gridLayout.setColumnStretch(2, 1)
        self.gridLayout.setColumnStretch(3, 1)

        # Dialog Settings
        self.setLayout(self.mainLayout)
        self.setWindowTitle("Globals")

        signalsGlobals.Signals.__init__(self)
        uiGlobals.UI.__init__(self)