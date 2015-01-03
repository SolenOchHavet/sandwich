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

except:
    from PySide.QtGui import *

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

        # File menu - Containing Render, Export and Globals
        fileMenu = QMenu("File", menuBar)

        # File > Render... 
        action = fileMenu.addAction("Render...")
        action.triggered.connect(self.frame.sgnLaunchRender)

        # File > Export... 
        action = fileMenu.addAction("Export...")
        action.triggered.connect(self.frame.sgnLaunchExport)

        # File > Globals... 
        action = fileMenu.addAction("Globals...")
        action.triggered.connect(self.frame.sgnLaunchGlobals)        

        # Layer menu - Containing all layer controls and layers
        self.layerMenu = QMenu("Layer", menuBar)

        # View menu - Containing controls over what should be visible
        # in Sandwich's interface
        self.viewMenu = QMenu("View", menuBar)

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
        helpMenu = QMenu("Help", menuBar)
        action = helpMenu.addAction("Sandwich Help")
        action.triggered.connect(self.core.help)

        helpMenu.addSeparator()

        action = helpMenu.addAction("About Sandwich")
        action.triggered.connect(self.showAbout)
        
        # Assemble the menues
        menuBar.addMenu(fileMenu)
        menuBar.addMenu(self.layerMenu)
        menuBar.addMenu(self.viewMenu)
        menuBar.addMenu(helpMenu)

        self.frame.uiUpdateViewMenu(self.frame.sSelectedLayerName)

        # If first run, force Sandwich to show Globals where user has
        # to confirm the settings
        if self.core.isFirstRun():
            self.showGlobals(True)

    def showAbout(self):
        """
        Shows the About dialog
        """

        self.aboutDlg = dialogAbout.AboutDialog(self.frame)
        self.aboutDlg.show()

    def showExport(self):
        """
        Shows the Export dialog for exporting the layers as scenes
        """

        self.exportDlg = dialogExport.ExportDialog(self.frame, core = self.core)
        self.exportDlg.show()

    def showGlobals(self, bAsModal = False):
        """
        Shows Sandwich's Globals dialog
        """

        self.globalsDlg = dialogGlobals.GlobalsDialog(self.frame, core = self.core)

        if bAsModal:
            self.globalsDlg.setModal(True)

        self.globalsDlg.show()

    def showRender(self):
        """
        Shows the Render dialog for rendering out the layers
        """

        self.renderDlg = dialogRender.RenderDialog(self.frame, core = self.core)
        self.renderDlg.show()