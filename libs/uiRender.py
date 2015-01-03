#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""

UI handlers for dialog "Render"

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
        self.lstSelectedRenders = []

        self.uiLoadRenderList()
        self.uiLoadOutputLocation()

    def uiCloseWindow(self):
        self.close()

    def uiLoadOutputLocation(self):
        sOutputLocation = self.core.getGlobalsValue("sOutputRenders")
        if sOutputLocation:
            sOutputLocation += "/$FILE_$LAYER_$CAMERA/$RES/"
            sLabel = "Output Location: <font color='#bbc26e'>%s</font>" % (sOutputLocation)

        else:
            sLabel = "Output Location: <font color='#bbc26e'>(please set \"Output Renders\" in Globals to a directory)</font>"

        self.pathLabel.setText(sLabel)

    def uiLoadRenderList(self):
        dData = self.core.getAllRenders()

        lstRenderLayers = dData.keys()
        lstRenderLayers.sort()

        self.layersList.clear()

        for sRenderLayer in lstRenderLayers:
            lstRow = ["", sRenderLayer, dData[sRenderLayer]["sCameraName"]]
            lstRow.append("%sx%s" % (dData[sRenderLayer]["lstResolution"][0],
                                     dData[sRenderLayer]["lstResolution"][1]))
            lstRow.append("%s-%s@%s" % (dData[sRenderLayer]["lstRange"][0],
                                        dData[sRenderLayer]["lstRange"][1],
                                        dData[sRenderLayer]["lstRange"][2]))

            treeItem = QTreeWidgetItem(lstRow)
            treeItem.setCheckState(0, Qt.Checked)
            self.layersList.addTopLevelItem(treeItem)

    def uiSaveSelectedRenders(self):
        self.lstSelectedRenders = []

        for iIndex in range(self.layersList.topLevelItemCount()):
            treeItem = self.layersList.topLevelItem(iIndex)
            if treeItem.checkState(0) == Qt.Checked:
                self.lstSelectedRenders.append(unicode(treeItem.text(1)))

    def uiSwitchSelectedCheckStateInList(self):
        lstSelected = self.layersList.selectedItems()

        if lstSelected[0].checkState(0) == Qt.Checked:
            lstSelected[0].setCheckState(0, Qt.Unchecked)

        else:
            lstSelected[0].setCheckState(0, Qt.Checked)