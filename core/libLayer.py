#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""

Library "Layer"

This object has the current layer in memory and lets you modify any aspect of
it.

"""

import re


class Layer(object):
    def __init__(self, parent):
        self.parent = parent
        self.utils = parent.utils
        self.node = parent.node
        self.dLayers = {}
        # TODO: vart ska det här ligga??
        self.dLayers["masterLayer"] = {
            "sComments": "",
            "sVisibility": "",
            "dShaders": {},
            "dAttributes": {},
            "sOverrideCode": "",
            "sOverrideMode": "python",
            "sRevertCode": "",
            "sRevertMode": "python",
            "dRenderSettings": {
                "lstCameraName": [False, ""],
                "lstResolution": [False, "", ""],
                "lstRange": [False, "", "", ""],
                "lstRenderEngine": [False, ""],
            },
            "dRenderGlobals": {},
        }
        self.sOverrideLayer = None
        self.dRenderGlobals = {}

    def addAttribute(self, sAttributeName, sOverValue = "", 
        sRevertValue = "", sAssignment = ""):
        """
        Add new attribute to the current layer. Optionally, you may specify
        override value, revert value and assignment.

        NOTE: Attribute will not be executed unless all three values have been
        specified.
        """

        self.dLayers[self.layerName()]["dAttributes"][sAttributeName] = \
            {"sOverValue": sOverValue, "sRevertValue": sRevertValue, 
            "sObjects": sAssignment}

    def addShader(self, sShaderName, sAssignment = ""):
        """
        Add new shader with optional assigned objects to the current layer
        """
    
        self.dLayers[self.layerName()]["dShaders"][sShaderName] = sAssignment

    def attributeAssignment(self, sAttributeName):
        """
        Return the objects that are affected by the attribute sAttributeName
        """

        return self.dLayers[self.layerName()]["dAttributes"][sAttributeName]["sObjects"]

    def attributeOverrideValue(self, sAttributeName):
        """
        Returns the override value that is set for the attribute sAttributeName
        """

        return self.dLayers[self.layerName()]["dAttributes"][sAttributeName]["sOverValue"]

    def attributeRevertValue(self, sAttributeName):
        """
        Returns the revert value that is set for the attribute sAttributeName
        """

        return self.dLayers[self.layerName()]["dAttributes"][sAttributeName]["sRevertValue"]

    def attributes(self, bAsDictionary = False):
        """
        Returns a list of all created attributes for the layer
        """

        if not bAsDictionary:
            lstAttributes = self.dLayers[self.layerName()]["dAttributes"].keys()
            lstAttributes.sort()

            return lstAttributes

        else:
            return self.dLayers[self.layerName()]["dAttributes"]

    def code(self):
        """

        """

        dLayer = self.dLayers[self.layerName()]

        return {dLayer["sOverrideCode"], dLayer["sOverrideMode"],
            dLayer["sRevertCode"], dLayer["sRevertMode"]}

    def comments(self):
        """
        Returns the comments specified for the current layer
        """

        return self.dLayers[self.layerName()]["sComments"]

    def current(self):
        return self.sCurrentLayer

    def execute(self):
        """
        Applys the current layer to the scene
        """

        # Quickly reset the visibility and shading.
        # NOTE: The proper visibility resetting is done inside the loop below
        self.utils.resetVisiblity()
        self.utils.resetShading()

        # Now loop through all layers except the selected and run the revert
        # section for attributes and MEL code
        for sRenderLayer in self.dLayers.keys():
            if sRenderLayer == self.sCurrentLayer:
                continue

            # Reset the visibility to false for all objects in each layer
            lstObjects = self.parent.getOnlyObjects(self.dLayers[sRenderLayer]["sVisibility"])
            self.utils.applyAttribute("visibility", False, lstObjects)

            # Apply the revert section of the Attributes tab
            for sAttributeName in self.dLayers[sRenderLayer]["dAttributes"].keys():
                self.utils.applyAttribute(sAttributeName,
                    self.dLayers[sRenderLayer]["dAttributes"][sAttributeName]["sRevertValue"],
                    self.dLayers[sRenderLayer]["dAttributes"][sAttributeName]["sObjects"].split())

            # Apply the revert section of the MEL tab
            self.utils.applyCode(self.dLayers[sRenderLayer]["sRevertMode"], 
                self.dLayers[sRenderLayer]["sRevertCode"])

        # Reset the render globals into the defaults. The default render globals can only be resaved from Globals
        self.utils.applyRenderGlobals(self.dRenderGlobals)

        # If this is masterLayer then abort now (we know that if
        # self.sCurrentLayer is empty)
        if not self.sCurrentLayer:
            return

        # Now apply our current layer
        lstObjects = self.parent.getOnlyObjects(self.visibility())
        self.utils.applyVisibility(lstObjects)

        for sShaderName in self.shaders():
            self.utils.applyShader(sShaderName,
                self.shaderAssignment(sShaderName, bAsList = True))

        for sAttributeName in self.attributes():
            self.utils.applyAttribute(sAttributeName,
                self.attributeOverrideValue(sAttributeName),
                self.attributeAssignment(sAttributeName).split())

        self.utils.applyRenderGlobals(self.renderGlobals())

        self.utils.applyCode(self.overrideMode(), self.overrideCode())

        # Set the current render engine as the default in the Render View
        sRenderEngine = self.parent.getLayerRenderEngine()
        self.parent.setRenderViewEngine(sRenderEngine)

    def layerName(self):
        return self.sOverrideLayer or self.sCurrentLayer

    def overrideCode(self):
        """
        Returns the custom override code specified for the current layer
        """

        return self.dLayers[self.layerName()]["sOverrideCode"]

    def overrideMode(self):
        """
        Returns the override mode specified for the current layer. Can either
        be "mel" or "python".
        """

        return self.dLayers[self.layerName()]["sOverrideMode"]

    def remove(self, sRenderLayer):
        del self.dLayers[self.layerName()]
        self.node.deleteLayer(self.layerName())

    def removeAttribute(self, sAttributeName):
        if self.dLayers[self.layerName()]["dAttributes"].has_key(sAttributeName):
            del self.dLayers[self.layerName()]["dAttributes"][sAttributeName]

    def removeShader(self, sShaderName):
        """
        Remove the specified shader from the current layer if it exists
        """

        if self.dLayers[self.layerName()]["dShaders"].has_key(sShaderName):
            del self.dLayers[self.layerName()]["dShaders"][sShaderName]

    def rename(self, sOldLayerName, sNewLayerName):
        """
        Renames a layer from sOldLayerName to sNewLayerName

        NOTE: This method will rename it instantly, without any savings needed.
        """

        # If we rename the current layer we will have to update the 
        # sCurrentLayer variable as well.
        if self.sCurrentLayer == sOldLayerName:
            self.sCurrentLayer = sNewLayerName

        self.dLayers[sNewLayerName] = self.dLayers.pop(sOldLayerName)
        self.node.renameLayer(sOldLayerName, sNewLayerName)

    def renameAttribute(self, sOldAttributeName, sNewAttributeName):
        """
        Renames the specified attribute for the current layer.

        NOTE: Returns a string if the operation fails
        """

        # Skip if attribute name has not been changed
        if sOldAttributeName == sNewAttributeName:
            return

        # If attribute already exists, then raise an error
        if self.dLayers[self.layerName()]["dAttributes"].has_key(sNewAttributeName):
            return "Can't rename attribute into <b>%s</b> since it already " \
                "exists for the layer!" % (sNewAttributeName)
            
        self.dLayers[self.layerName()]["dAttributes"][sNewAttributeName] = self.dLayers[self.layerName()]["dAttributes"].pop(sOldAttributeName)

    def renameShader(self, sOldShaderName, sNewShaderName):
        """
        Renames the specified shader for the current layer.

        NOTE: Returns a string if the operation fails
        """

        # Skip if shader name has not been changed
        if sOldShaderName == sNewShaderName:
            return

        # If shader already exists, then raise an error
        if self.dLayers[self.layerName()]["dShaders"].has_key(sNewShaderName):
            return "Can't rename attribute into <b>%s</b> since it already " \
                "exists for the layer!" % (sNewShaderName)

        self.dLayers[self.layerName()]["dShaders"][sNewShaderName] = self.dLayers[self.layerName()]["dShaders"].pop(sOldShaderName)

    def renderGlobals(self, sRenderLayer = None):
        return self.dLayers[self.layerName()]["dRenderGlobals"]

    def renderSetting(self, sRenderSetting):
        return self.dLayers[self.layerName()]["dRenderSettings"][sRenderSetting]

    def renderSettings(self, sRenderLayer = None):
        return self.dLayers[self.layerName()]["dRenderSettings"].copy()

    def revertCode(self):
        """
        Returns the custom revert code specified for the current layer
        """

        return self.dLayers[self.layerName()]["sRevertCode"]

    def revertMode(self):
        """
        Returns the revert mode specified for the current layer. Can either be
        "mel" or "python".
        """

        return self.dLayers[self.layerName()]["sRevertMode"]

    def save(self):
        """
        Save the current state of the current layer into our sMayaNode within 
        our scene
        """

        # Make sure we have attributes on our save node that represents our
        # current layer
        self.node.save(self)

    def select(self, sLayerName = None):
        self.sCurrentLayer = sLayerName or self.sOverrideLayer

    def set(self, sLayerName = None):
        """
        Specify the currently selected layer.

        NOTE: This method does not execute the layer change. Use execute() 
        after calling this method.
        """

        self.sOverrideLayer = sLayerName

        # if sLayerName in self.dLayers.keys():
        #     self.sCurrentLayer = sLayerName

        #     self.node.saveSelected(sLayerName)

        # elif re.search("^" + self.sMasterLayer + "$", sLayerName, re.IGNORECASE):
        #     self.sCurrentLayer = ""

        #     self.node.saveSelected("masterLayer")

        # else:
        #     return "Can't select layer \"%s\" since it does not exists!" % (sLayerName)

    def setAttributeAssignment(self, sAttributeName, sValue):
        """
        Set assignment for the specified attribute in the current layer
        """

        self.dLayers[self.layerName()]["dAttributes"][sAttributeName]["sObjects"] = str(sValue)

    def setAttributeOverrideValue(self, sAttributeName, sValue):
        """
        Set override value for the specified attribute in the current layer
        """

        self.dLayers[self.layerName()]["dAttributes"][sAttributeName]["sOverValue"] = str(sValue)

    def setAttributeRevertValue(self, sAttributeName, sValue):
        self.dLayers[self.layerName()]["dAttributes"][sAttributeName]["sRevertValue"] = str(sValue)

    def setComments(self, sText):
        """
        Set the comments for the currently selected layer
        """

        self.dLayers[self.layerName()]["sComments"] = sText

    def setOverrideCode(self, sText):
        """
        Set what override code should be run for the currently selected layer
        """

        self.dLayers[self.layerName()]["sOverrideCode"] = sText

    def setRevertCode(self, sText):
        """
        Set what revert code should be run for the currently selected layer
        """

        self.dLayers[self.layerName()]["sRevertCode"] = sText

    def setShaderAssignment(self, sShaderName, sText):
        """
        Set the assignment for the specified shader in the current layer
        """

        self.dLayers[self.layerName()]["dShaders"][sShaderName] = sText

    def setVisibility(self, sText):
        """
        Set what should be visible for the currently selected layer
        """

        self.dLayers[self.layerName()]["sVisibility"] = sText

    def shaderAssignment(self, sShaderName, bAsList = False):
        """
        Return the objects that are affected by the shader sShaderName
        """

        if sShaderName in self.dLayers[self.layerName()]["dShaders"].keys():
            if not bAsList:
                return self.dLayers[self.layerName()]["dShaders"][sShaderName]

            else:
                return self.getOnlyObjects(self.dLayers[self.layerName()]["dShaders"][sShaderName])

        else:
            if not bAsList:
                return ""

            else:
                return []

    def shaders(self):
        """
        Returns a list of all shaders for the currently selected layer
        alphabetically
        """

        return sorted(self.dLayers[self.layerName()]["dShaders"].keys())
        
    def visibility(self):
        """
        Returns what should be visibile for the currently selected layer
        """

        return self.dLayers[self.layerName()]["sVisibility"]