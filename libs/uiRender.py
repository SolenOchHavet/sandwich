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
        self.layersList.clear()

        for oLayer in self.core.layers():
            item = QTreeWidgetItem()

            item.setText(1, oLayer.layerName())
            item.setText(2, oLayer.cameraName())
            item.setText(3, "%sx%s" % 
                (oLayer.resolutionWidth(), oLayer.resolutionHeight())
            item.setText(4, "%s-%s@%s" % (oLayer.startFrame(), 
                oLayer.endFrame(), oLayer.incFrame()))

            item.setCheckState(0, Qt.Checked)
            
            self.layersList.addTopLevelItem(item)

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