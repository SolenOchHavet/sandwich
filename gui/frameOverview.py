#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""

Frame "Overview"

This frame is just a big text field for the user to input any comments, reminders or ideas for the current selected
render layer.

"""

try:
    from PyQt4.QtGui import *

except:
    from PySide.QtGui import *

import sandwich.libs.uiOverview as ui
reload(ui)


class OverviewFrame(QFrame, ui.UI):
    def __init__(self, parent = None, core = None, text = None):
        QFrame.__init__(self)

        self.parent = parent
        self.core = core
        self.text = text

        # Layout Widgets
        self.mainLayout = QVBoxLayout()

        # Widgets
        self.descriptionLabel = QLabel(self.text.overview.descriptionLabel)
        self.descriptionField = QTextEdit()

        # Widget settings
        self.descriptionField.setStyleSheet("font-family:'Courier New', Courier, monospace;" \
            "font-size:12px")

        # Widget Status Tips
        self.descriptionLabel.setStatusTip(self.text.overview.descriptionTip)
        self.descriptionField.setStatusTip(self.text.overview.descriptionTip)

        # Layout the Widgets
        self.mainLayout.addWidget(self.descriptionLabel)
        self.mainLayout.addWidget(self.descriptionField)

        # Layout Settings
        self.setLayout(self.mainLayout)

        ui.UI.__init__(self)