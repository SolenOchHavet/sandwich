#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""

UI handlers for tab "Render Globals"

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

    def uiClearLayout(self, qtLayout):
        while qtLayout.count():
            widgetItem = qtLayout.takeAt(0)
            if not widgetItem:
                continue

            widget = widgetItem.widget()
            if widget:
                widget.deleteLater()

    def uiLoadRenderGlobals(self):
        print "uiLoadRenderGlobals!!!"
        oRenderEngine = self.core.layer().renderEngine()
        dRenderGlobals = self.core.layer().renderGlobals()

        self.dataTree.clear()

        for sRenderEngine in dRenderGlobals.keys():
            if not sRenderEngine == oRenderEngine.engineName():
                continue

            for lstAttr in dRenderGlobals[sRenderEngine]:
                print lstAttr, # sAttrName...? 
                sNodeWithAttr = lstAttr[0]
                # Check if attribute is a part of the overridden attributes
                # bFound = False
                

                # for lstAttr in lstOverrideAttrs:
                #     if sAttrName == lstAttr[0]:
                #         bFound = True
                #         break

                #     iIndex += 1

                # if not bFound:
                #     continue

                # # If this attribute is the first hit in this section then make a label
                # if self.iCurrentId != iId:
                #     sSection = funcGetSection(iId)
                #     qSectionLabel = QLabel(sLabelCss % ("%", sSection))
                #     self.scrollLayout.addWidget(qSectionLabel, self.iCurrentRow, 0, 1, 3, Qt.AlignBottom)

                #     # Do this check to skip first section to have this height
                #     if self.iCurrentId != None:
                #         self.scrollLayout.setRowMinimumHeight(self.iCurrentRow, 25)

                #     self.iCurrentRow += 1
                #     self.iCurrentId = iId

                # Translate the node path
                for lstRow in oRenderEngine.nodes():
                    sNodeWithAttr = sNodeWithAttr.replace(lstRow[1], lstRow[0])

                # Get type of attribute as an ID
                iTypeId = self.core.getAttributeType(sNodeWithAttr)

                sAttrLabel = self.core.getAttributeName(sNodeWithAttr)

                xDefaultValue = self.core.getDefaultRenderGlobalsItem(sRenderEngine, lstAttr[0])

                # Try to get the value of the attribute. If this function fails we are dealing with a message
                # attribute
                try:
                    xValue = self.core.getAttributeValue(sNodeWithAttr)

                except:
                    continue

                # Handle the label different depending on type
                if iTypeId == 1:
                    # Bool
                    sValueText = {0: "off", 1: "on"}[int(xValue)]
                    if xDefaultValue != None:
                        xDefaultValue = {0: "off", 1: "on"}[int(xDefaultValue)]

#                elif iTypeId == 4:
#                    # Enum
#                    lstTemp = sNodeWithAttr.split(".")
#                    lstEnums = self.core.getAttributeEnum(lstTemp[0], lstTemp[1])
#                    qControl = QComboBox(parent = self.renderglobalsFrame)
#                    qControl.addItems(lstEnums)
#
#                elif iTypeId == 7:
#                    # TdataCompound?
#                    qControl = QLineEdit(parent = self.renderglobalsFrame)
#
                elif iTypeId == 8:
                    # Color Attribute
                    sValueText = unicode(xValue[0])
                    xDefaultValue = xDefaultValue[0]

                else:
                    sValueText = unicode(xValue)

                item = QTreeWidgetItem()

                item.setText(0, sAttrLabel)
                item.setText(1, "%s (default: %s)" % (sValueText, xDefaultValue))
                
                editButton = QPushButton("Edit...", self.dataTree)

                self.dataTree.addTopLevelItem(item)
                self.dataTree.setItemWidget(item, 2, editButton)

        # # Clear the interface that holds all previous Render Globals settings
        # self.uiClearLayout(self.scrollLayout)

        # self.iCurrentId = None
        # self.iCurrentRow = 0

        # # Get the render globals data from the core
        
        # print "Loading render globals!!", oRenderEngine
        # print "overrides!", dRenderGlobals
        # # Draw the render globals overrides that have been done for the current
        # # render layer
        # self.uiLoadScrollArea(oRenderEngine, dRenderGlobals)

        # self.scrollLayout.setRowStretch(self.iCurrentRow, 1)

    def uiLoadScrollArea(self, oRenderEngine, dRenderGlobals):
        # Loop through all sections on render globals for selected render engine
        sLabelCss = "<div style=\"width:100%s;background-color:#4e4e4e;margin-left:45px;font-size:13px;" \
                    "font-weight:bold;border-bottom:solid 1 #616161;\">%s</span>"
        sRenderEngine = oRenderEngine.engineName()
        print dRenderGlobals
        iIndex = 0
        for iId in sorted(dRenderGlobals.keys()):
            print "ID", iId
            # Loop through all attributes within a section
            for lstAttr in dRenderGlobals[iId]:
                print lstAttr, # sAttrName...? 
                sNodeWithAttr = lstAttr[0]
                # Check if attribute is a part of the overridden attributes
                # bFound = False
                

                # for lstAttr in lstOverrideAttrs:
                #     if sAttrName == lstAttr[0]:
                #         bFound = True
                #         break

                #     iIndex += 1

                # if not bFound:
                #     continue

                # # If this attribute is the first hit in this section then make a label
                # if self.iCurrentId != iId:
                #     sSection = funcGetSection(iId)
                #     qSectionLabel = QLabel(sLabelCss % ("%", sSection))
                #     self.scrollLayout.addWidget(qSectionLabel, self.iCurrentRow, 0, 1, 3, Qt.AlignBottom)

                #     # Do this check to skip first section to have this height
                #     if self.iCurrentId != None:
                #         self.scrollLayout.setRowMinimumHeight(self.iCurrentRow, 25)

                #     self.iCurrentRow += 1
                #     self.iCurrentId = iId

                # Translate the node path
                for lstRow in oRenderEngine.nodes():
                    sNodeWithAttr = sNodeWithAttr.replace(lstRow[1], lstRow[0])

                # Get type of attribute as an ID
                iTypeId = self.core.getAttributeType(sNodeWithAttr)

                sAttrLabel = self.core.getAttributeName(sNodeWithAttr)

                xDefaultValue = self.core.getDefaultRenderGlobalsItem(sRenderEngine, lstAttr[0])

                # Try to get the value of the attribute. If this function fails we are dealing with a message
                # attribute
                try:
                    xValue = self.core.getAttributeValue(sNodeWithAttr)

                except:
                    continue

                # Draw the controls
                qAttrLabel = QLabel("<span style='font-weight:none'>" + sAttrLabel + ":</span>&nbsp;")

                # Handle the label different depending on type
                if iTypeId == 1:
                    # Bool
                    sValueText = {0: "off", 1: "on"}[int(xValue)]
                    xDefaultValue = {0: "off", 1: "on"}[int(xDefaultValue)]

#                elif iTypeId == 4:
#                    # Enum
#                    lstTemp = sNodeWithAttr.split(".")
#                    lstEnums = self.core.getAttributeEnum(lstTemp[0], lstTemp[1])
#                    qControl = QComboBox(parent = self.renderglobalsFrame)
#                    qControl.addItems(lstEnums)
#
#                elif iTypeId == 7:
#                    # TdataCompound?
#                    qControl = QLineEdit(parent = self.renderglobalsFrame)
#
                elif iTypeId == 8:
                    # Color Attribute
                    sValueText = unicode(xValue[0])
                    xDefaultValue = xDefaultValue[0]

                else:
                    sValueText = unicode(xValue)

                qValueLabel = QLabel("<font color='#bbc26e'>%s</font>   (default: %s)" %
                    (sValueText, xDefaultValue))
                removeButton = QPushButton("Remove")

                # Layout widgets
                self.scrollLayout.addWidget(qAttrLabel, self.iCurrentRow, 0, 1, 1, Qt.AlignRight)
                self.scrollLayout.addWidget(qValueLabel, self.iCurrentRow, 1, 1, 1)
                self.scrollLayout.addWidget(removeButton, self.iCurrentRow, 2, 1, 1)

                self.iCurrentRow += 1

                #lstOverrideAttrs.pop(iIndex)

        # Add stretching to the end of the layout
        self.scrollLayout.setRowStretch(self.iCurrentRow, 1)

    def uiSaveTabContent(self):
        self.core.addLayerRenderGlobals()

    def uiSetCheckBox(self, qtCheckBox, bValue):
        if bValue:
            qtCheckBox.setCheckState(Qt.Checked)

        else:
            qtCheckBox.setCheckState(Qt.Unchecked)