#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""

Frame "Code"

This frame has two text fields for overriding and reverting MEL/Python code. User will usually use this section if
he/she needs special cases to take place that are easier to achieve using MEL/Python code.

"""

try:
    from PyQt4.QtGui import *

except:
    from PySide.QtGui import *

import sandwich.libs.uiCode as ui
reload(ui)


class CodeFrame(QFrame, ui.UI):
    def __init__(self, parent = None, core = None, text = None):
        QFrame.__init__(self)

        self.parent = parent
        self.core = core
        self.text = text

        # Layout Widgets
        self.mainLayout = QVBoxLayout()

        # Widgets
        self.overrideLabel = QLabel(self.text.code.overrideLabel)
        self.overrideField = QTextEdit()
        self.revertLabel = QLabel(self.text.code.revertLabel)
        self.revertField = QTextEdit()

        # Widget Settings
        self.overrideField.setStyleSheet("font-family:'Courier New', Courier, monospace;"\
            "font-size:12px")
        self.revertField.setStyleSheet("font-family:'Courier New', Courier, monospace;"\
            "font-size:12px")

        self.overrideLabel.setStatusTip(self.text.code.overrideTip)
        self.overrideField.setStatusTip(self.text.code.overrideTip)
        self.revertLabel.setStatusTip(self.text.code.revertTip)
        self.revertField.setStatusTip(self.text.code.revertTip)

        # Layout the Widgets
        self.mainLayout.addWidget(self.overrideLabel)
        self.mainLayout.addWidget(self.overrideField, 1)
        self.mainLayout.addWidget(self.revertLabel)
        self.mainLayout.addWidget(self.revertField, 1)

        # Layout Settings
        self.setLayout(self.mainLayout)

        ui.UI.__init__(self)