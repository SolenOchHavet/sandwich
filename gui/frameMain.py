#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""

Frame "Main"

This frame is the main window for Sandwich. It includes a tabWidget that's made up of several panels. The frame also
have a toolbar, a list for all render layers and a status line. The status line will help the user by informing him/her
what he/she is pointing at with the mouse.

"""

try:
    from PyQt4.QtGui import *
    from PyQt4.QtCore import Qt

except:
    from PySide.QtGui import *
    from PySide.QtCore import Qt

import sandwich.signals.signalsMain as signalsMain
import sandwich.libs.uiMain as uiMain
reload(signalsMain)
reload(uiMain)

import frameToolbar
import frameOverview
import frameVisibility
import frameShaders
import frameAttributes
import frameOverrideGlobals
import frameRenderGlobals
import frameCode
reload(frameToolbar)
reload(frameOverview)
reload(frameVisibility)
reload(frameShaders)
reload(frameAttributes)
reload(frameOverrideGlobals)
reload(frameRenderGlobals)
reload(frameCode)


class MainFrame(QFrame, signalsMain.Signals, uiMain.UI):
    def __init__(self, parent = None, core = None, text = None):
        QFrame.__init__(self)

        self.parent = parent
        self.core = core
        self.text = text
        
        # Layout Widgets
        self.mainLayout = QVBoxLayout()
        
        # Frames
        self.overviewFrame = frameOverview.OverviewFrame(
            self, core = self.core, text = self.text)
        self.visibilityFrame = frameVisibility.VisibilityFrame(
            self, core = self.core, text = self.text)
        self.shadersFrame = frameShaders.ShadersFrame(
            self, core = self.core, text = self.text)
        self.attributesFrame = frameAttributes.AttributesFrame(
            self, core = self.core, text = self.text)
        self.overrideglobalsFrame = frameOverrideGlobals.OverrideGlobalsFrame(
            self, core = self.core, text = self.text)
        self.renderglobalsFrame = frameRenderGlobals.RenderGlobalsFrame(
            self, core = self.core, text = self.text)
        self.codeFrame = frameCode.CodeFrame(
            self, core = self.core, text = self.text)

        # Widgets
        # - Toolbar, created separately
        self.toolbar = frameToolbar.ToolbarFrame(self)

        # - Render Layers, created separately
        self.dataTree = QTreeWidget()
        self.mainSplitter = QSplitter(Qt.Horizontal)

        # - The tab widget on the right side
        self.settingsTab = QTabWidget()

        # Widget Settings
        self.dataTree.setHeaderLabels(["Render Layers"])
        self.dataTree.setRootIsDecorated(False)
        self.mainSplitter.addWidget(self.dataTree)
        self.mainSplitter.addWidget(self.settingsTab)
        self.mainSplitter.setStretchFactor(0, 1)
        self.mainSplitter.setStretchFactor(1, 2)

        # TabWidget setup
        self.settingsTab.addTab(self.overviewFrame, "Overview")
        self.settingsTab.addTab(self.visibilityFrame, "Visibility")
        self.settingsTab.addTab(self.shadersFrame, "Shaders")
        self.settingsTab.addTab(self.attributesFrame, "Attributes")
        self.settingsTab.addTab(self.overrideglobalsFrame, "Override Globals")
        self.settingsTab.addTab(self.renderglobalsFrame, "Render Globals")
        self.settingsTab.addTab(self.codeFrame, "Code")

        # Layout the Widgets
        self.mainLayout.addSpacing(5)
        self.mainLayout.addWidget(self.toolbar)
        self.mainLayout.addWidget(self.mainSplitter)
        self.mainLayout.addSpacing(5)

        # Layout Settings
        self.setLayout(self.mainLayout)

        uiMain.UI.__init__(self)
        signalsMain.Signals.__init__(self)