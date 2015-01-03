#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""

Dialog "About"

"""

try:
    from PyQt4.QtCore import Qt
    from PyQt4.QtGui import *

except:
    from PySide.QtCore import Qt
    from PySide.QtGui import *


class AboutDialog(QDialog):
    def __init__(self, parent = None):
        QDialog.__init__(self)

        self.parent = parent

        # Layout Widgets
        self.mainLayout = QVBoxLayout()

        # Widgets
        self.aboutLabel = QLabel("<center><b style='font-size:16px'>Sandwich</b><br>" \
            "<br>A shy little render layer manager for Maya<br><br>Version 1.0<br><br>" \
            "In memory of<br>Niphon Ruangnoi 1983-2012</center>")

        # Layout Settings
        self.mainLayout.setContentsMargins(70, 25, 70, 25)

        # Layout
        self.mainLayout.addWidget(self.aboutLabel)

        # Dialog Settings
        self.setLayout(self.mainLayout)
        self.setWindowTitle("About Sandwich")