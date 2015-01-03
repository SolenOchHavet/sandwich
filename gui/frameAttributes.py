#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""

Frame "Attributes"

This panel handles all the attributes that are being used for the selected render layer. You can:
 * Add, rename and remove attributes.
 * Set which objects should be affected by the different attributes.

"""

try:
    from PyQt4.QtGui import *

except:
    from PySide.QtGui import *

import sandwich.signals.signalsAttributes as signals
import sandwich.libs.uiAttributes as ui
reload(signals)
reload(ui)


class AttributesFrame(QFrame, signals.Signals, ui.UI):
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
        self.addattrButton = QPushButton("Add Attribute...")
        self.renameattrButton = QPushButton("Rename Attribute...")
        self.addobjectsButton = QPushButton("Add Objects")
        self.orgobjectsButton = QPushButton("Reorganize Objects")

        # - Left column
        self.attributesLabel = QLabel("Attribute List")
        self.attributesList = QListWidget()

        # - Right column
        self.overrideLabel = QLabel("Override Value")
        self.overrideField = QLineEdit()
        self.revertLabel = QLabel("Revert Value")
        self.revertField = QLineEdit()
        self.assignLabel = QLabel("Assign to These Objects")
        self.assignField = QTextEdit()

        # Settings
        self.attributesList.setFixedWidth(220)
        self.addattrButton.setFixedWidth(115)
        self.renameattrButton.setFixedWidth(115)
        self.addobjectsButton.setFixedWidth(115)
        self.orgobjectsButton.setFixedWidth(120)
        self.assignField.setStyleSheet("font-family:'Courier New', Courier, monospace;"\
            "font-size:12px")

        # Widget Status Tips
        self.addattrButton.setStatusTip("Add new attribute.")
        self.renameattrButton.setStatusTip("Rename selected attribute. Name must be unique.")
        self.addobjectsButton.setStatusTip("Add selected objects from the scene.")
        self.orgobjectsButton.setStatusTip("Reorganizes the assigned object's " \
            "names in alphabetic order.")
        self.attributesLabel.setStatusTip("All current attributes. Select one " \
            "to set it's override/revert value and assign objects to it.")
        self.attributesList.setStatusTip("All current attributes. Select one to " \
            "set it's override/revert value and assign objects to it.")
        self.overrideLabel.setStatusTip("Set the revert attribute value it " \
            "should have when this render layer is no longer active.")
        self.overrideField.setStatusTip("Set the attribute value it should have " \
            "when this render layer is active.")
        self.revertLabel.setStatusTip("Set the revert attribute value it should " \
            "have when this render layer is no longer active.")
        self.revertField.setStatusTip("Set the revert attribute value it should " \
            "have when this render layer is no longer active.")
        self.assignLabel.setStatusTip("Set which objects should be affected by " \
            "the currently selected attribute.")
        self.assignField.setStatusTip("Set which objects should be affected by " \
            "the currently selected attribute.")

        # Layout the Widgets
        self.toolbarLayout.addWidget(self.addattrButton)
        self.toolbarLayout.addWidget(self.renameattrButton)
        self.toolbarLayout.addWidget(self.addobjectsButton)
        self.toolbarLayout.addStretch(1)
        self.toolbarLayout.addWidget(self.orgobjectsButton)

        self.leftColumnLayout.addWidget(self.attributesLabel)
        self.leftColumnLayout.addWidget(self.attributesList, 1)

        self.rightColumnLayout.addWidget(self.overrideLabel)
        self.rightColumnLayout.addWidget(self.overrideField)
        self.rightColumnLayout.addWidget(self.revertLabel)
        self.rightColumnLayout.addWidget(self.revertField)
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