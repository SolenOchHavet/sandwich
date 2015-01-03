#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""

Frame "Shaders"

This frame handles all the shaders that are being used for the selected render layer. You can:
 * Add, rename and remove shaders.
 * Set which objects should be affected by the different shaders.

"""

try:
    from PyQt4.QtGui import *

except:
    from PySide.QtGui import *

import sandwich.signals.signalsShaders as signals
import sandwich.libs.uiShaders as ui
reload(signals)
reload(ui)


class ShadersFrame(QFrame, signals.Signals, ui.UI):
    def __init__(self, parent = None, core = None, text = None):
        QFrame.__init__(self)

        self.parent = parent
        self.core = core
        self.text = text

        # Layout Widgets
        self.mainLayout = QVBoxLayout()
        self.bodyLayout = QHBoxLayout()
        self.toolbarLayout = QHBoxLayout()
        self.leftColumnLayout = QVBoxLayout()
        self.rightColumnLayout = QVBoxLayout()

        # Widgets
        # - Toolbar buttons
        self.addshaderButton = QPushButton(self.text.shaders.addshaderLabel)
        self.renameshaderButton = QPushButton(self.text.shaders.renameshaderLabel)
        self.addobjectsButton = QPushButton(self.text.shaders.addobjectsLabel)
        self.orgobjectsButton = QPushButton(self.text.shaders.organizebjectsLabel)

        # - Left and right column
        self.shaderLabel = QLabel(self.text.shaders.shaderlistLabel)
        self.shaderList = QListWidget()
        self.assignLabel = QLabel(self.text.shaders.assignLabel)
        self.assignField = QTextEdit()

        # Widget Settings
        self.shaderList.setFixedWidth(220)
        self.addshaderButton.setFixedWidth(115)
        self.renameshaderButton.setFixedWidth(115)
        self.addobjectsButton.setFixedWidth(115)
        self.orgobjectsButton.setFixedWidth(120)
        self.assignField.setStyleSheet("font-family:'Courier New', Courier, monospace;"\
            "font-size:12px")

        # Widget Status Tips
        self.addshaderButton.setStatusTip(self.text.shaders.addshaderTip)
        self.renameshaderButton.setStatusTip(self.text.shaders.renameshaderTip)
        self.addobjectsButton.setStatusTip(self.text.shaders.addobjectsTip)
        self.orgobjectsButton.setStatusTip(self.text.shaders.organizebjectsTip)
        self.shaderLabel.setStatusTip(self.text.shaders.shaderlistTip)
        self.shaderList.setStatusTip(self.text.shaders.shaderlistTip)
        self.assignLabel.setStatusTip(self.text.shaders.assignTip)
        self.assignField.setStatusTip(self.text.shaders.assignTip)

        # Layout the Widgets
        self.toolbarLayout.addWidget(self.addshaderButton)
        self.toolbarLayout.addWidget(self.renameshaderButton)
        self.toolbarLayout.addWidget(self.addobjectsButton)
        self.toolbarLayout.addStretch(1)
        self.toolbarLayout.addWidget(self.orgobjectsButton)

        self.leftColumnLayout.addWidget(self.shaderLabel)
        self.leftColumnLayout.addWidget(self.shaderList, 1)

        self.rightColumnLayout.addWidget(self.assignLabel)
        self.rightColumnLayout.addWidget(self.assignField, 1)

        self.bodyLayout.addLayout(self.leftColumnLayout)
        self.bodyLayout.addSpacing(5)
        self.bodyLayout.addLayout(self.rightColumnLayout)

        self.mainLayout.addLayout(self.toolbarLayout)
        self.mainLayout.addSpacing(5)
        self.mainLayout.addLayout(self.bodyLayout)

        # Layout Settings
        self.setLayout(self.mainLayout)

        ui.UI.__init__(self)
        signals.Signals.__init__(self)