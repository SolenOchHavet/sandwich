#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""

Library "Node"

Handles all storing and retrieving of data from the Sandwich node in the scene.

"""

import maya.cmds as mc


class Node(object):
    def __init__(self):
        self.sSwNode = "sandwichNode"
        self.bIsFirstRun = False

        self.lstLayerAttrs = ("overview", "visibility", "shaders", 
            "attributes", "globals", "settings", "code", "renderGlobals")

        # We create the Maya node at the initialization of the core if it is not
        # yet created
        self.create()
        self.createGlobalsAttributes()

    def create(self):
        """
        Creates our Maya node if we do not have it yet
        """

        if not mc.objExists(self.sSwNode):
            mc.createNode("transform", name = self.sSwNode)

            # Also, mark this as first startup
            self.bIsFirstRun = True

    def createGlobalsAttributes(self):
        """
        Creates attribute to store all globals settings and an additional
        attribute for saving the latest selected layer
        """

        if not mc.objExists(self.sSwNode + ".globals"):
            mc.addAttr(self.sSwNode, ln = "globals", dt = "string")

        if not mc.objExists(self.sSwNode + ".current"):
            mc.addAttr(self.sSwNode, ln = "current", dt = "string")

        if not mc.objExists(self.sSwNode + ".renderGlobals"):
            mc.addAttr(self.sSwNode, ln = "renderGlobals", dt = "string")

    def createLayer(self, sLayerName):
        """
        Creates all attributes needed to store all information about the render
        layer on the sandwichNode
        """

        # Iterate over all layer attributes that must exists. Only create them
        # if they do not exists
        for sSuffix in self.lstLayerAttrs:
            sAttr = sLayerName + "_" + sSuffix

            if not mc.objExists(self.sSwNode + "." + sAttr):
                mc.addAttr(self.sSwNode, ln = sAttr, dt = "string")

    def deleteLayer(self, sLayerName):
        """
        Delete render layer sLayerName from the node by removing all of 
        it's attributes
        """

        for sSuffix in self.lstLayerAttrs:
            if mc.objExists(self.sSwNode + "." + sLayerName + "_" + sSuffix):
                mc.deleteAttr(self.sSwNode, at = sLayerName + "_" + sSuffix)

    def globals(self):
        """
        Returns the default Sandwich globals
        """

        sOutput = mc.getAttr(self.sSwNode + ".globals")

        if sOutput:
            return eval(sOutput)

        return {}

    def isFirstRun(self):
        return self.bIsFirstRun

    def layerAttributes(self, sRenderLayerName):
        """
        Special method to retrieve the current state for the attributes
        section as a dictionary
        """

        return eval(mc.getAttr(self.sSwNode + "." + sRenderLayerName + "_attributes"))

    def layers(self):
        """
        Returns a dictionary of all layers that are currently stored on the 
        Sandwich node
        """

        dOutput = {}

        lstAttrs = mc.listAttr(self.sSwNode, string = "*_overview") or []

        for sAttr in lstAttrs:
            sRenderLayer = sAttr.rsplit("_", 1)[0]

            # Add the render layer. This will make it currently selected so we
            # can use the core's different function to load data
            dOutput[sRenderLayer] = {}

            # Load the overview data
            sData = mc.getAttr(self.sSwNode + "." + sRenderLayer + 
                "_overview")

            dOutput[sRenderLayer]["sComments"] = sData

            # Load the visibility data
            sData = mc.getAttr(self.sSwNode + "." + sRenderLayer + 
                "_visibility")

            dOutput[sRenderLayer]["sVisibility"] = sData

            # Load the shaders data
            dData = eval(mc.getAttr(self.sSwNode + "." + sRenderLayer + 
                "_shaders"))

            dOutput[sRenderLayer]["dShaders"] = dData

            # Load the attributes data
            dData = eval(mc.getAttr(self.sSwNode + "." + sRenderLayer + 
                "_attributes"))

            dOutput[sRenderLayer]["dAttributes"] = dData

            # Load the render settings
            dData = eval(mc.getAttr(self.sSwNode + "." + sRenderLayer + 
                "_settings"))

            dOutput[sRenderLayer]["dRenderSettings"] = dData

            # Load the render globals
            dData = eval(mc.getAttr(self.sSwNode + "." + sRenderLayer + 
                "_renderGlobals"))

            dOutput[sRenderLayer]["dRenderGlobals"] = dData

            # Load the code data
            dData = eval(mc.getAttr(self.sSwNode + "." + sRenderLayer + 
                "_code"))
            print dData
            dOutput[sRenderLayer]["sOverrideCode"] = dData["sOverrideCode"]
            dOutput[sRenderLayer]["sOverrideMode"] = dData["sOverrideMode"]
            dOutput[sRenderLayer]["sRevertCode"] = dData["sRevertCode"]
            dOutput[sRenderLayer]["sRevertMode"] = dData["sRevertMode"]

        return dOutput

    def renameLayer(self, sOldLayerName, sNewLayerName):
        """
        Renames the layer on node level, which means rename the attributes
        that are used for storing all parts of the render layer.
        """

        for sSuffix in self.lstLayerAttrs:
            # Make sure each attribute still exists before renaming them
            if mc.objExists(self.sSwNode + "." + sOldLayerName + "_" + sSuffix):
                mc.renameAttr(self.sSwNode + "." + sOldLayerName + "_" + sSuffix,
                    sNewLayerName + "_" + sSuffix)

    def renderGlobals(self):
        """
        Returns the default render globals for the master layer
        """

        sOutput = mc.getAttr(self.sSwNode + ".renderGlobals")

        if sOutput:
            return eval(sOutput)

        return {}

    def save(self, oLayer):
        """
        Saves the specified render layer object to the node
        """

        sBasePath = self.sSwNode + "." + oLayer.layerName()

        # Make sure all attributes exists before saving anything
        self.createLayer(oLayer.layerName())

        # Save the overview data to the node
        mc.setAttr(sBasePath + "_overview", oLayer.comments(), type = "string")

        # Save the visibility data to the node
        mc.setAttr(sBasePath + "_visibility", oLayer.visibility(),
            type = "string")

        # Save the shaders data to the node
        mc.setAttr(sBasePath + "_shaders", unicode(oLayer.shaders(True)), 
            type = "string")

        # Save the attributes data to the node
        mc.setAttr(sBasePath + "_attributes", unicode(oLayer.attributes(True)),
            type = "string")

        # Save the output settings data to the node
        mc.setAttr(sBasePath + "_settings", unicode(oLayer.renderSettings()),
            type = "string")

        # Save the render globals data to the node
        mc.setAttr(sBasePath + "_renderGlobals", unicode(oLayer.renderGlobals()),
            type = "string")

        # Save the code data to the node
        mc.setAttr(sBasePath + "_code", unicode(oLayer.code()), type = "string")

    def saveSelected(self, sLayerName):
        """
        Saves the specified layer as the selected on to Sandwich's node. This 
        is only useful during the next launch of Sandwich, which will remember
        which was the latest selected layer
        """

        mc.setAttr(self.sSwNode + ".current", sLayerName, type = "string")

    def saveDefaultRenderGlobals(self, dData = {}):
        """
        Save the default Render Globals
        """

        mc.setAttr(self.sSwNode + ".renderGlobals", unicode(dData), 
            type = "string")

    def saveGlobals(self, dData = {}):
        """
        Saves Sandwich's settings (called Globals) to the node
        """

        # Save the globals data to the node
        mc.setAttr(self.sSwNode + ".globals", unicode(dData), type = "string")

    def selected(self):
        """
        Returns the last selected render layer, which has been stored in the
        sandwichNode. If no render layer has been specified, then return the
        name of the master layer
        """

        return mc.getAttr(self.sSwNode + ".current") or "masterLayer"