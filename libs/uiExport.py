#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""

UI handlers for dialog "Export"

"""

try:
    from PyQt4.QtCore import Qt
    from PyQt4.QtGui import *

except:
    from PySide.QtCore import Qt
    from PySide.QtGui import *

import maya.cmds as mc

import re
import os



class UI(object):
    def __init__(self):
        self.lstSelectedExports = []
        self.sSelectedFileType = ""

        self.uiLoadExportList()
        self.uiLoadOutputLocation()

    def uiCloseWindow(self):
        self.close()

    def uiLoadExportList(self):
        dData = self.core.getAllExports()

        lstRenderLayers = dData.keys()
        lstRenderLayers.sort()

        self.layersList.clear()

        for sRenderLayer in lstRenderLayers:
            treeItem = QTreeWidgetItem(["", sRenderLayer, dData[sRenderLayer]["sFileName"] + ".mb"])
            treeItem.setCheckState(0, Qt.Checked)
            self.layersList.addTopLevelItem(treeItem)

    def uiLoadOutputLocation(self):
        sOutputLocation = self.core.getGlobalsValue("sOutputScenes")
        print sOutputLocation, len(sOutputLocation), type(sOutputLocation), "!!!"
        print self.core.dGlobals
        if sOutputLocation:
            sLabel = "Output Location: <font color='#bbc26e'>%s</font>" % (sOutputLocation)

        else:
            sLabel = "Output Location: <font color='#bbc26e'><please set \"Output Scene\" in Globals to a directory></font>"

        self.pathLabel.setText(sLabel)

    def uiSaveSelectedExports(self):
        self.lstSelectedExports = []

        for iIndex in range(self.layersList.topLevelItemCount()):
            treeItem = self.layersList.topLevelItem(iIndex)
            if treeItem.checkState(0) == Qt.Checked:
                self.lstSelectedExports.append(unicode(treeItem.text(1)))

    def uiShowResults(self):
        sTitle = "Export results"
        sMsg = "The following render layers were exported:<br>"

        for sRenderLayer in self.lstSelectedExports:
            sMsg += " * " + sRenderLayer + "<br>"

        sMsg += "<br>Export settings:"

        # Show what file type was used in the export
        sMsg += "<br> * File Type: <font color='#bbc26e'>%s</font>" % (self.sSelectedFileType)

        # Show if Import References was used
        sMsg += "<br> * Import references: "

        if self.core.getGlobalsValue("bSettingImportRefs"):
            sMsg += "<font color='#bbc26e'>Yes</font>"

        else:
            sMsg += "<font color='#bbc26e'>No</font>"

        QMessageBox.information(self, sTitle, sMsg)

    def uiSwitchSelectedCheckStateInList(self):
        lstSelected = self.layersList.selectedItems()

        if lstSelected[0].checkState(0) == Qt.Checked:
            lstSelected[0].setCheckState(0, Qt.Unchecked)

        else:
            lstSelected[0].setCheckState(0, Qt.Checked)