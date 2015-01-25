#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""

Tool "Sandwich"
Author "Andreas Ekoutsidis"
Email "daiboushi@gmail.com"

A render layer manager for Maya2012 and forth. Requires either PyQt or PySide.

"""

try:
    from PyQt4.QtGui import *
    from PyQt4.QtCore import Qt

except:
    from PySide.QtGui import *
    from PySide.QtCore import Qt

import sys

import libs
import signals.signalsMain
import core.libMain as libMain
reload(libMain)
import core.libText as libText
reload(libText)
import gui.frameMain as frameMain
reload(frameMain)
import gui.dialogGlobals as dialogGlobals
reload(dialogGlobals)
import gui.dialogExport as dialogExport
reload(dialogExport)
import gui.dialogRender as dialogRender
reload(dialogRender)
import gui.dialogAbout as dialogAbout
reload(dialogAbout)


class Sandwich(QMainWindow):
    def __init__(self, parent = None):
        QMainWindow.__init__(self, parent)

        self.setWindowTitle("Sandwich")

        self.core = libMain.MainCore()
        self.text = libText.Text()

        # Setup Sandwich's menus
        menuBar = self.menuBar()

        self.frame = frameMain.MainFrame(self, core = self.core,
            text = self.text)
        self.setCentralWidget(self.frame)
        self.setGeometry(90, 90, 840, 430)
        self.statusBar()

        # File menu
        fileMenu = QMenu("&File", menuBar)

        # File > New Layer... 
        action = fileMenu.addAction("New Layer...")
        action.setShortcut("Ctrl+Shift+N")
        action.triggered.connect(self.frame.sgnNewLayer)

        # File > Save Layer 
        action = fileMenu.addAction("Save Layer")
        action.setShortcut("Ctrl+Shift+S")
        action.triggered.connect(self.frame.sgnSaveLayer)

        fileMenu.addSeparator()

        # File > Render... 
        action = fileMenu.addAction("Render...")
        action.triggered.connect(self.frame.sgnLaunchRender)

        # File > Export... 
        action = fileMenu.addAction("Export...")
        action.triggered.connect(self.frame.sgnLaunchExport)

        # File menu
        editMenu = QMenu("&Edit", menuBar)

        # Edit > Rename Layer...
        action = editMenu.addAction("Rename Layer...")
        action.triggered.connect(self.frame.sgnNewLayer)

        editMenu.addSeparator()

        # Edit > Globals... 
        action = editMenu.addAction("Globals...")
        action.triggered.connect(self.frame.sgnLaunchGlobals)        

        # Layer menu - Containing all layer controls and layers
        self.layerMenu = QMenu("&Layer", menuBar)

        # View menu - Containing controls over what should be visible
        # in Sandwich's interface
        self.viewMenu = QMenu("&View", menuBar)

        # View - Toolbar
        action = self.viewMenu.addAction("Toolbar")
        action.setCheckable(True)
        action.setChecked(True)
        action.setStatusTip("Show/Hide the toolbar")
        action.triggered.connect(self.frame.sgnSwitchVisibilityForToolbar)

        # View - Render Layers
        action = self.viewMenu.addAction("Render Layers")
        action.setCheckable(True)
        action.setChecked(True)
        action.setStatusTip("Show/Hide the render layer list")
        action.triggered.connect(self.frame.sgnSwitchRenderLayersForToolbar)

        # Help menu - Sandwich Help and About Sandwich
        helpMenu = QMenu("&Help", menuBar)
        action = helpMenu.addAction("Sandwich Help")
        action.triggered.connect(self.core.help)

        helpMenu.addSeparator()

        action = helpMenu.addAction("About Sandwich")
        action.triggered.connect(self.showAbout)
        
        # Assemble the menues
        menuBar.addMenu(fileMenu)
        menuBar.addMenu(editMenu)
        menuBar.addMenu(self.layerMenu)
        menuBar.addMenu(self.viewMenu)
        menuBar.addMenu(helpMenu)

        self.frame.uiUpdateViewMenu()

        # If we are on OSX, set the always on top flag
        if sys.platform == "darwin":
            self.setWindowFlags(Qt.WindowStaysOnTopHint)

        # If first run, force Sandwich to show Globals where user has
        # to confirm the settings
        if self.core.node.isFirstRun():
            self.showGlobals(True)

    def showAbout(self):
        """
        Shows the About dialog
        """

        dlg = dialogAbout.AboutDialog(self)
        dlg.show()

    def showExport(self):
        """
        Shows the Export dialog for exporting the layers as scenes
        """

        dlg = dialogExport.ExportDialog(self, core = self.core)
        dlg.show()

    def showGlobals(self, bAsModal = False):
        """
        Shows Sandwich's Globals dialog
        """

        dlg = dialogGlobals.GlobalsDialog(self, core = self.core)

        if bAsModal:
            dlg.setModal(True)

        dlg.show()

    def showRender(self):
        """
        Shows the Render dialog for rendering out the layers
        """

        dlg = dialogRender.RenderDialog(self, core = self.core)
        dlg.show()