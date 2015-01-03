#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""

Frame "Visibility"

This section decides what should be visible for the selected render layer. It's just a single big text field where
user can enter the names of all objects that should be visible. User is also allowed to use Python-styled comments

"""

try:
    from PyQt4.QtGui import *

except:
    from PySide.QtGui import *

import sandwich.signals.signalsVisibility as signals
import sandwich.libs.uiVisibility as ui
reload(signals)
reload(ui)


class VisibilityFrame(QFrame, signals.Signals, ui.UI):
    def __init__(self, parent = None, core = None, text = None):
        QFrame.__init__(self)

        self.parent = parent
        self.core = core
        self.text = text

        # Layout Widgets
        self.mainLayout = QVBoxLayout()
        self.toolbarLayout = QHBoxLayout()

        # Widgets
        # - Toolbar buttons
        self.addobjectsButton = QPushButton(self.text.visibility.addobjectsLabel)
        self.orgobjectsButton = QPushButton(self.text.visibility.organizebjectsLabel)

        self.visibilityField = QTextEdit()

        # Widget settings
        self.addobjectsButton.setFixedWidth(115)
        self.orgobjectsButton.setFixedWidth(120)
        self.visibilityField.setStyleSheet("font-family:'Courier New', Courier, monospace;" \
            "font-size:12px")

        # Widget Status Tips
        self.addobjectsButton.setStatusTip(self.text.visibility.addobjectsTip)
        self.orgobjectsButton.setStatusTip(self.text.visibility.organizebjectsTip)
        self.visibilityField.setStatusTip(self.text.visibility.visibilityTip)

        # Layout the Widgets
        self.toolbarLayout.addWidget(self.addobjectsButton)
        self.toolbarLayout.addStretch(1)
        self.toolbarLayout.addWidget(self.orgobjectsButton)

        self.mainLayout.addLayout(self.toolbarLayout)
        self.mainLayout.addSpacing(5)
        self.mainLayout.addWidget(self.visibilityField, 1)

        # Layout Settings
        self.setLayout(self.mainLayout)

        ui.UI.__init__(self)
        signals.Signals.__init__(self)