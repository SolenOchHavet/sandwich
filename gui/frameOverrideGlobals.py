#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""

Frame "Override Globals"

This frame holds different rendering settings that can be overridden at render layer level. They are:
 * "Override Camera Name". Overrides the camera that's used for rendering the layer.
 * "Override Resolution". Overrides the resolution for the layer.
 * "Override Range". Overrides the frame range will be used for the layer.
 * "Override Engine". Overrides which render engine should be used for rendering the layer.

All overrides above have a default value that's specified in the Globals dialog.

"""

try:
    from PyQt4.QtCore import QRegExp
    from PyQt4.QtGui import *

except:
    from PySide.QtCore import QRegExp
    from PySide.QtGui import *

import sandwich.signals.signalsOverrideGlobals as signals
import sandwich.libs.uiOverrideGlobals as ui
reload(signals)
reload(ui)


class OverrideGlobalsFrame(QFrame, signals.Signals, ui.UI):
    def __init__(self, parent = None, core = None, text = None):
        QFrame.__init__(self)

        self.parent = parent
        self.core = core
        self.text = text

        # Layout Widgets
        self.mainLayout = QGridLayout()
        self.resolutionLayout = QHBoxLayout()
        self.rangeLayout = QHBoxLayout()

        # Widgets
        self.cameraCheck = QCheckBox()
        self.cameraLabel = QLabel(self.text.override.cameraLabel)
        self.cameraField = QLineEdit()
        self.cameraButton = QPushButton(self.text.override.cameraBrowseLabel)
        self.resolutionCheck = QCheckBox()
        self.resolutionLabel = QLabel(self.text.override.resolutionLabel)
        self.widthField = QLineEdit()
        self.heightField = QLineEdit()
        self.rangeCheck = QCheckBox()
        self.rangeLabel = QLabel(self.text.override.rangeLabel)
        self.startField = QLineEdit()
        self.endField = QLineEdit()
        self.stepField = QLineEdit()
        self.engineCheck = QCheckBox()
        self.engineLabel = QLabel(self.text.override.engineLabel)
        self.engineCombo = QComboBox()

        # Settings
        rangeValidator = QRegExpValidator(QRegExp("-?[0-9]+"), self)
        resValidator = QRegExpValidator(QRegExp("[0-9]+"), self)
        nameValidator = QRegExpValidator(QRegExp("[a-z,A-Z,_][a-z,A-Z,_,0-9]*"), self)

        self.widthField.setFixedWidth(60)
        self.heightField.setFixedWidth(60)
        self.startField.setFixedWidth(60)
        self.endField.setFixedWidth(60)
        self.stepField.setFixedWidth(60)

        self.cameraField.setValidator(nameValidator)
        self.widthField.setValidator(resValidator)
        self.heightField.setValidator(resValidator)
        self.startField.setValidator(rangeValidator)
        self.endField.setValidator(rangeValidator)
        self.stepField.setValidator(rangeValidator)

        # Widget Status Tips
        self.cameraCheck.setStatusTip(self.text.override.cameraactivateTip)
        self.cameraLabel.setStatusTip(self.text.override.cameraTip)
        self.cameraField.setStatusTip(self.text.override.camerafieldTip)
        self.cameraButton.setStatusTip(self.text.override.camerabrowseTip)
        self.resolutionCheck.setStatusTip(self.text.override.resolutionactivateTip)
        self.resolutionLabel.setStatusTip(self.text.override.resolutionTip)
        self.widthField.setStatusTip(self.text.override.widthTip)
        self.heightField.setStatusTip(self.text.override.heightTip)
        self.rangeCheck.setStatusTip(self.text.override.rangeactivateTip)
        self.rangeLabel.setStatusTip(self.text.override.rangeTip)
        self.startField.setStatusTip(self.text.override.startTip)
        self.endField.setStatusTip(self.text.override.endTip)
        self.stepField.setStatusTip(self.text.override.stepTip)
        self.engineCheck.setStatusTip(self.text.override.engineactivateTip)
        self.engineLabel.setStatusTip(self.text.override.engineLabel)
        self.engineCombo.setStatusTip(self.text.override.engineLabel)

        # Layout the Widgets
        self.resolutionLayout.addWidget(self.widthField)
        self.resolutionLayout.addWidget(self.heightField)
        self.resolutionLayout.addStretch(1)

        self.rangeLayout.addWidget(self.startField)
        self.rangeLayout.addWidget(self.endField)
        self.rangeLayout.addWidget(self.stepField)
        self.rangeLayout.addStretch(1)

        self.mainLayout.addWidget(self.cameraCheck, 0, 0)
        self.mainLayout.addWidget(self.cameraLabel, 0, 1)
        self.mainLayout.addWidget(self.cameraField, 0, 2)
        self.mainLayout.addWidget(self.cameraButton, 0, 3)
        self.mainLayout.addWidget(self.resolutionCheck, 1, 0)
        self.mainLayout.addWidget(self.resolutionLabel, 1, 1)
        self.mainLayout.addLayout(self.resolutionLayout, 1, 2)
        self.mainLayout.addWidget(self.rangeCheck, 2, 0)
        self.mainLayout.addWidget(self.rangeLabel, 2, 1)
        self.mainLayout.addLayout(self.rangeLayout, 2, 2)
        self.mainLayout.addWidget(self.engineCheck, 3, 0)
        self.mainLayout.addWidget(self.engineLabel, 3, 1)
        self.mainLayout.addWidget(self.engineCombo, 3, 2)

        self.mainLayout.setRowStretch(4, 1)

        # Layout Settings
        self.setLayout(self.mainLayout)

        ui.UI.__init__(self)
        signals.Signals.__init__(self)