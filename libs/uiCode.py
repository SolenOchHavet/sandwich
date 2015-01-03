#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""

UI handlers for "Code"

This code also handles all panels (in the tabWidget).

"""

try:
    from PyQt4.QtCore import Qt
    from PyQt4.QtGui import *

except:
    from PySide.QtCore import Qt
    from PySide.QtGui import *

import re


class UI(object):
    def __init__(self):
        pass

    def uiSaveTabContent(self):
        self.core.layer().setOverrideCode(unicode(self.overrideField.toPlainText()))
        self.core.layer().setRevertCode(unicode(self.revertField.toPlainText()))