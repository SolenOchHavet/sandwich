#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""

Library "Node"

Handles all storing and retrieving of data from the Sandwich node in the scene.

"""

import maya.cmds as mc


class Node(object):
    def __init__(self, parent):
        self.parent = parent
        self.sMayaNode = "sandwichNode"

        self.lstLayerAttrs = ("overview", "visibility", "shaders", 
            "attributes", "globals", "settings", "code", "renderGlobals")

        # We create the Maya node at the initialization of the core if it is not
        # yet created
        self.create()

        self.createGlobalsAttributes()

        # If the Maya node already exists it might contain render layers data.
        # Load it in that case
        self.load()

    def create(self):
        """
        Creates our Maya node if we do not have it yet
        """

        if not mc.objExists(self.sMayaNode):
            mc.createNode("transform", name = self.sMayaNode)

            # Also, mark this as first startup
            self.parent.bIsFirstRun = True

    def createGlobalsAttributes(self):
        """
        Creates attribute to store all globals settings and an additional
        attribute for saving the latest selected layer
        """

        if not mc.objExists(self.sMayaNode + ".globals"):
            mc.addAttr(self.sMayaNode, ln = "globals", dt = "string")

        if not mc.objExists(self.sMayaNode + ".current"):
            mc.addAttr(self.sMayaNode, ln = "current", dt = "string")

        if not mc.objExists(self.sMayaNode + ".renderGlobals"):
            mc.addAttr(self.sMayaNode, ln = "renderGlobals", dt = "string")

    def createLayer(self, sLayerName):
        """
        Creates all attributes needed to store all information about the render
        layer on the sandwichNode
        """

        # Iterate over all layer attributes that must exists. Only create them
        # if they do not exists
        for sSuffix in self.lstLayerAttrs:
            sAttr = sLayerName + "_" + sSuffix

            if not mc.objExists(self.sMayaNode + "." + sAttr):
                mc.addAttr(self.sMayaNode, ln = sAttr, dt = "string")

    def createLayerAttributes(self):
        """
        Creates all necessary attributes in order to store our current
        layer's data

        TODO: DEPRICATED!
        """

        lstData = ("_overview", "_visibility", "_shaders", "_attributes",
                   "_globals", "_settings", "_code", "_renderGlobals")

        # Create the attributes that does not exist already. Although this
        # approach should not be necessary, lets just be safe
        for sAttrSuffix in lstData:
            if not mc.objExists(self.sMayaNode + "." + self.parent.sCurrentLayer + sAttrSuffix):
                mc.addAttr(self.sMayaNode, ln = self.parent.sCurrentLayer + sAttrSuffix,
                    dt = "string")

    def current(self):
        """
        Returns the last selected render layer, which has been stored in the
        sandwichNode. If no render layer has been specified, then return the
        name of the master layer
        """

        return mc.getAttr(self.sMayaNode + ".current") or "masterLayer"

    def deleteLayer(self, sRenderLayerName):
        """
        Delete render layer sRenderLayerName from the node by removing
        all of it's attributes
        """

        lstData = ("overview", "visibility", "shaders", "attributes", "code",
            "globals", "settings", "renderGlobals")

        for sAttr in lstData:
            if mc.objExists(self.sMayaNode + "." + sRenderLayerName + "_" + sAttr):
                mc.deleteAttr(self.sMayaNode, at = sRenderLayerName + "_" + sAttr)

    def getLayerAttributesData(self, sRenderLayerName):
        """
        Special method to retrieve the current state for the attributes
        section as a dictionary
        """

        return eval(mc.getAttr(self.sMayaNode + "." + sRenderLayerName + "_attributes"))

    def load(self):
        """
        Loads all data from the Sandwich node to create all layers and settings.
        """

        dOutput = {}

        lstAttrs = mc.listAttr(self.sMayaNode, string = "*_overview") or []

        for sAttr in lstAttrs:
            iLastUnderScore = sAttr.rfind("_")
            sRenderLayer = sAttr[:iLastUnderScore]

            # Add the render layer. This will make it currently selected so we
            # can use the core's different function to load data
            dOutput[sRenderLayer] = {}

            # Load the overview data
            sData = mc.getAttr(self.sMayaNode + "." +
                self.parent.sCurrentLayer + "_overview")

            dOutput[sRenderLayer]["sComments"] = sData

            # Load the visibility data
            sData = mc.getAttr(self.sMayaNode + "." +
                self.parent.sCurrentLayer + "_visibility")

            dOutput[sRenderLayer]["sVisibility"] = sData

            # Load the shaders data
            dData = eval(mc.getAttr(self.sMayaNode + "." +
                self.parent.sCurrentLayer + "_shaders"))

            dOutput[sRenderLayer]["dShaders"] = dData

            # Load the attributes data
            dData = eval(mc.getAttr(self.sMayaNode + "." +
                self.parent.sCurrentLayer + "_attributes"))

            dOutput[sRenderLayer]["dAttributes"] = dData

            # Load the render settings
            dData = eval(mc.getAttr(self.sMayaNode + "." +
                self.parent.sCurrentLayer + "_settings"))

            dOutput[sRenderLayer]["dRenderSettings"] = dData

            # Load the render globals
            dData = eval(mc.getAttr(self.sMayaNode + "." +
                self.parent.sCurrentLayer + "_renderGlobals"))

            dOutput[sRenderLayer]["dRenderGlobals"] = dData

            # Load the code data
            dData = eval(mc.getAttr(self.sMayaNode + "." +
                self.parent.sCurrentLayer + "_code"))

            #self.parent.layer().setOverrideCode(dData["sOverride"])
            #self.parent.layer().setRevertCode(dData["sRevert"])

        # Load globals if any is saved or create defaults
        sData = mc.getAttr(self.sMayaNode + ".globals")

        if sData:
            self.parent.setGlobals(eval(sData))

        else:
            self.parent.addGlobals()

        # Load default render globals
        # sData = mc.getAttr(self.sMayaNode + ".renderGlobals")

        # if sData:
        #     self.parent.setRenderGlobals(eval(sData))
        #     self.parent.setDefaultRenderGlobals(eval(sData))

        # else:
        #     self.parent.addDefaultRenderGlobals()

        #     # Save the new default render globals back to the Sandwich node
        #     mc.setAttr(self.sMayaNode + ".renderGlobals", unicode(self.parent.dDefaultRenderGlobals),
        #         type = "string")

    def loadCurrentLayer(self):
        """
        Loads the last selected layer from Sandwich's node. This method is only
        executed once on each Sandwich startup to select the last selected layer
        """

        sCurrentLayer = mc.getAttr(self.sMayaNode + ".current")

        if sCurrentLayer in self.parent.getLayers():
            self.parent.layer().select(sCurrentLayer)

        else:
            self.parent.layer().select(self.parent.sMasterLayer)

    def renameLayer(self, sOldRenderLayerName, sNewRenderLayerName):
        """
        Renames the layer on node level, which means rename the attributes
        that are used for storing all parts of the render layer.
        """

        lstData = ("overview", "visibility", "shaders", "attributes",
            "code", "globals", "settings", "renderGlobals")

        for sAttr in lstData:
            # Make sure each attribute still exists before renaming them
            if mc.objExists(self.sMayaNode + "." + sOldRenderLayerName + "_" + sAttr):
                mc.renameAttr(self.sMayaNode + "." + sOldRenderLayerName + "_" + sAttr,
                    sNewRenderLayerName + "_" + sAttr)

    def saveCurrentLayer(self):
        """
        Saves the currently selected layer to Sandwich's node. This value will
        only be retrieved when Sandwich launches to select the last active layer.
        """

        mc.setAttr(self.sMayaNode + ".current", self.parent.sCurrentLayer, type = "string")

    def saveDefaultRenderGlobals(self):
        """
        Save the default Render Globals.
        """

        mc.setAttr(self.sMayaNode + ".renderGlobals", unicode(self.parent.dRenderGlobals),
            type = "string")

    def saveGlobals(self):
        """
        Saves Sandwich's settings (called Globals) to the node
        """

        dData = self.parent.getGlobals()

        # Save the globals data to the node
        mc.setAttr(self.sMayaNode + ".globals", unicode(dData), type = "string")

    def saveLayer(self, sRenderLayer = None):
        """
        Saves the specified render layer sRenderLayer. If sRenderLayer is None, then
        the currently active layer will be saved.

        TODO: DEPRICATED
        """

        sRenderLayer = sRenderLayer or self.parent.sCurrentLayer

        # Save the overview data to the node
        mc.setAttr(self.sMayaNode + "." + sRenderLayer + "_overview",
            self.parent.layer(sRenderLayer).comments(), type = "string")

        # Save the visibility data to the node
        mc.setAttr(self.sMayaNode + "." + sRenderLayer + "_visibility",
            self.parent.layer(sRenderLayer).visibility(), type = "string")

        # Save the shaders data to the node
        mc.setAttr(self.sMayaNode + "." + sRenderLayer + "_shaders",
            unicode(self.parent.layer(sRenderLayer).shaders()), type = "string")

        # Save the attributes data to the node
        mc.setAttr(self.sMayaNode + "." + sRenderLayer + "_attributes",
            unicode(self.parent.layer(sRenderLayer).attributes(True)), type = "string")

        # Save the output settings data to the node
        mc.setAttr(self.sMayaNode + "." + sRenderLayer + "_settings",
            unicode(self.parent.layer(sRenderLayer).renderSettings()), type = "string")

        # Save the render globals data to the node
        mc.setAttr(self.sMayaNode + "." + sRenderLayer + "_renderGlobals",
            unicode(self.parent.layer(sRenderLayer).renderGlobals()), type = "string")

        # Save the code data to the node
        dData = {"sOverride": self.parent.layer(sRenderLayer).overrideCode(),
            "sRevert": self.parent.layer(sRenderLayer).revertCode()}
        mc.setAttr(self.sMayaNode + "." + sRenderLayer + "_code",
            unicode(dData), type = "string")