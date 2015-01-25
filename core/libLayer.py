#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""

Library "Layer"

This object has the current layer in memory and lets you modify any aspect of
it.

"""

import re


class Layer(object):
    def __init__(self, parent, sLayerName, dLayerData = None):
        self.parent = parent
        self.utils = parent.utils
        self.node = parent.node
        self.sLayerName = sLayerName
        self.dLayerData = dLayerData or {
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

    def addAttribute(self, sAttributeName, sOverValue = "", 
        sRevertValue = "", sAssignment = ""):
        """
        Add new attribute to the current layer. Optionally, you may specify
        override value, revert value and assignment.

        NOTE: Attribute will not be executed unless all three values have been
        specified
        """

        self.dLayerData["dAttributes"][sAttributeName] = \
            {"sOverValue": sOverValue, "sRevertValue": sRevertValue, 
            "sObjects": sAssignment}

    def addShader(self, sShaderName, sAssignment = ""):
        """
        Add new shader with optional assigned objects to the current layer
        """
    
        self.dLayerData["dShaders"][sShaderName] = sAssignment

    def attributeAssignment(self, sAttributeName):
        """
        Return the objects that are affected by the attribute sAttributeName
        """

        return self.dLayerData["dAttributes"][sAttributeName]["sObjects"]

    def attributeOverrideValue(self, sAttributeName):
        """
        Returns the override value that is set for the attribute sAttributeName
        """

        return self.dLayerData["dAttributes"][sAttributeName]["sOverValue"]

    def attributeRevertValue(self, sAttributeName):
        """
        Returns the revert value that is set for the attribute sAttributeName
        """

        return self.dLayerData["dAttributes"][sAttributeName]["sRevertValue"]

    def attributes(self, bAsDictionary = False):
        """
        Returns a list of all created attributes for the layer
        """

        if not bAsDictionary:
            return sorted(self.dLayerData["dAttributes"].keys())

        return self.dLayerData["dAttributes"]

    def cameraName(self):
        """
        Returns the camera name that will be used for the layer
        """

        # Retrieve camera on the layer if it has been defined
        if self.dLayerData["dRenderSettings"]["lstCameraName"][0]:
            return self.dLayerData["dRenderSettings"]["lstCameraName"][1]

        else:
            return self.parent.dGlobals["sDefaultCamera"]

    def code(self):
        """

        """

        return {
            "sOverrideCode": self.dLayerData["sOverrideCode"], 
            "sOverrideMode": self.dLayerData["sOverrideMode"], 
            "sRevertCode": self.dLayerData["sRevertCode"],
            "sRevertMode": self.dLayerData["sRevertMode"],
            }

    def comments(self):
        """
        Returns the comments specified for the current layer
        """

        return self.dLayerData["sComments"]

    def endFrame(self):
        """
        Returns the end frame specified for the layer. It's either specified
        at layer level or at global level
        """

        lstData = self.dLayerData["dRenderSettings"]["lstRange"]

        if lstData[0]:
            if lstData[2] != None:
                return lstData[2]

        return self.parent.dGlobals["iEnd"]

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
        for oLayer in self.parent.layers():
            if oLayer.layerName() == self.sLayerName:
                continue

            # Reset the visibility to false for all objects in each layer
            lstObjects = self.utils.objectsOnly(oLayer.visibility())
            self.utils.applyAttribute("visibility", False, lstObjects)

            # Apply the revert section of the Attributes tab
            for sAttributeName in oLayer.attributes():
                self.utils.applyAttribute(sAttributeName,
                    oLayer.attributeRevertValue(sAttributeName),
                    oLayer.attributeAssignment(sAttributeName).split())

            # Apply the revert section of the MEL tab
            self.utils.applyCode(oLayer.revertMode(), oLayer.revertCode())

        # Reset the render globals into the defaults. The default render globals can only be resaved from Globals
        self.utils.applyRenderGlobals(self.parent.engines(), self.parent.dMasterRenderGlobals)

        # If this is masterLayer then abort now (we know that if
        # self.sLayerName is empty)
        if self.sLayerName == "masterLayer":
            return

        # Now apply our current layer
        lstObjects = self.utils.objectsOnly(self.visibility())
        self.utils.applyVisibility(lstObjects)

        for sShaderName in self.shaders():
            self.utils.applyShader(sShaderName,
                self.shaderAssignment(sShaderName, bAsList = True))

        for sAttributeName in self.attributes():
            self.utils.applyAttribute(sAttributeName,
                self.attributeOverrideValue(sAttributeName),
                self.attributeAssignment(sAttributeName).split())

        self.utils.applyRenderGlobals(self.parent.engines(), self.renderGlobals())

        self.utils.applyCode(self.overrideMode(), self.overrideCode())

        # Set the current render engine as the default in the Render View
        self.utils.setRenderViewEngine(self.renderEngine())

    def fileName(self):
        """
        Returns the file name for the render layer. It uses the scene name as
        the base and then adds the layer name seperated by an underscore
        """

        return self.utils.sceneName() + "_" + self.sLayerName

    def hasShader(self, sShaderName):
        """
        Check if layer has shader sShaderName
        """

        return sShaderName in self.dLayerData["dShaders"].keys()

    def incFrame(self):
        """
        Returns the incremental frame specified for the layer. It's either 
        specified at layer level or at global level
        """

        lstData = self.dLayerData["dRenderSettings"]["lstRange"]

        if lstData[0]:
            if lstData[3] != None:
                return lstData[3]

        return self.parent.dGlobals["iStep"]

    def layerName(self):
        return self.sLayerName

    def overrideCode(self):
        """
        Returns the custom override code specified for the current layer
        """

        return self.dLayerData["sOverrideCode"]

    def overrideMode(self):
        """
        Returns the override mode specified for the current layer. Can either
        be "mel" or "python"
        """

        return self.dLayerData["sOverrideMode"]

    def remove(self, sRenderLayer):
        self.node.deleteLayer(self.sLayerName)
        del self

    def removeAttribute(self, sAttributeName):
        if self.dLayerData["dAttributes"].has_key(sAttributeName):
            del self.dLayerData["dAttributes"][sAttributeName]

    def removeShader(self, sShaderName):
        """
        Remove the specified shader from the current layer if it exists
        """

        if self.dLayerData["dShaders"].has_key(sShaderName):
            del self.dLayerData["dShaders"][sShaderName]

    def rename(self, sOldLayerName, sNewLayerName):
        """
        Renames a layer from sOldLayerName to sNewLayerName

        NOTE: This method will rename it instantly, without any savings needed
        """

        # If we rename the current layer we will have to update the 
        # sLayerName variable as well.
        if self.sLayerName == sOldLayerName:
            self.sLayerName = sNewLayerName

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
        if self.dLayerData["dAttributes"].has_key(sNewAttributeName):
            return "Can't rename attribute into <b>%s</b> since it already " \
                "exists for the layer!" % (sNewAttributeName)
            
        self.dLayerData["dAttributes"][sNewAttributeName] = self.dLayerData["dAttributes"].pop(sOldAttributeName)

    def renameShader(self, sOldShaderName, sNewShaderName):
        """
        Renames the specified shader for the current layer.

        NOTE: Returns a string if the operation fails
        """

        # Skip if shader name has not been changed
        if sOldShaderName == sNewShaderName:
            return

        # If shader already exists, then raise an error
        if self.dLayerData["dShaders"].has_key(sNewShaderName):
            return "Can't rename attribute into <b>%s</b> since it already " \
                "exists for the layer!" % (sNewShaderName)

        self.dLayerData["dShaders"][sNewShaderName] = self.dLayerData["dShaders"].pop(sOldShaderName)

    def renderEngine(self):
        """
        Returns the specified render engine for the layer.
        """
        
        lstData = self.dLayerData["dRenderSettings"]["lstRenderEngine"]

        if lstData[0]:
            return self.parent.engine(lstData[1])

        else:
            return self.parent.engine(self.parent.dGlobals["sDefaultEngine"])

    def renderGlobals(self):
        return self.dLayerData["dRenderGlobals"]

    def renderSetting(self, sRenderSetting):
        return self.dLayerData["dRenderSettings"][sRenderSetting]

    def renderSettings(self):
        return self.dLayerData["dRenderSettings"].copy()

    def resolutionHeight(self):
        """
        Returns the resolution height. It's either specified at layer level or
        at global level
        """

        lstData = self.dLayerData["dRenderSettings"]

        if lstData[0]:
            if lstData[2] != None:
                return lstData[2]

        return self.parent.dGlobals["iHeight"]

    def resolutionWidth(self):
        """
        Returns the resolution width. It's either specified at layer level or
        at global level
        """

        lstData = self.dLayerData["dRenderSettings"]

        if lstData[0]:
            if lstData[1] != None:
                return lstData[1]

        return self.parent.dGlobals["iWidth"]

    def revertCode(self):
        """
        Returns the custom revert code specified for the current layer
        """

        return self.dLayerData["sRevertCode"]

    def revertMode(self):
        """
        Returns the revert mode specified for the current layer. Can either be
        "mel" or "python".
        """

        return self.dLayerData["sRevertMode"]

    def save(self):
        """
        Save the current state of the current layer into our sMayaNode within 
        our scene
        """

        # Make sure we have attributes on our save node that represents our
        # current layer
        self.node.save(self)

    def setAttributeAssignment(self, sAttributeName, sValue):
        """
        Set assignment for the specified attribute in the current layer
        """

        self.dLayerData["dAttributes"][sAttributeName]["sObjects"] = str(sValue)

    def setAttributeOverrideValue(self, sAttributeName, sValue):
        """
        Set override value for the specified attribute in the current layer
        """

        self.dLayerData["dAttributes"][sAttributeName]["sOverValue"] = str(sValue)

    def setAttributeRevertValue(self, sAttributeName, sValue):
        self.dLayerData["dAttributes"][sAttributeName]["sRevertValue"] = str(sValue)

    def setComments(self, sText):
        """
        Set the comments for the currently selected layer
        """

        self.dLayerData["sComments"] = sText

    def setOverrideCode(self, sText):
        """
        Set what override code should be run for the currently selected layer
        """

        self.dLayerData["sOverrideCode"] = sText

    def setRenderGlobals(self, dData = {}):
        """

        """

        self.dLayerData["dRenderGlobals"] = dData

    def setRenderGlobalsForCurrentEngine(self, dData = {}):
        self.dLayerData["dRenderGlobals"][self.renderEngine().engineName()] = dData

    def setRenderSetting(self, sRenderSetting, lstData):
        """
        Set what layer render settings should be used for the currently selected layer
        """

        self.dLayerData["dRenderSettings"][sRenderSetting] = lstData

    def setRevertCode(self, sText):
        """
        Set what revert code should be run for the currently selected layer
        """

        self.dLayerData["sRevertCode"] = sText

    def setShaderAssignment(self, sShaderName, sText):
        """
        Set the assignment for the specified shader in the current layer
        """

        self.dLayerData["dShaders"][sShaderName] = sText

    def setVisibility(self, sText):
        """
        Set what should be visible for the currently selected layer
        """

        self.dLayerData["sVisibility"] = sText

    def shaderAssignment(self, sShaderName, bAsList = False):
        """
        Return the objects that are affected by the shader sShaderName
        """

        if sShaderName in self.dLayerData["dShaders"].keys():
            if not bAsList:
                return self.dLayerData["dShaders"][sShaderName]

            else:
                return self.utils.objectsOnly(self.dLayerData["dShaders"][sShaderName])

        else:
            if not bAsList:
                return ""

            else:
                return []

    def shaders(self, bAsDictionary = False):
        """
        Returns a list of all shaders for the currently selected layer
        alphabetically
        """

        if not bAsDictionary:
            return sorted(self.dLayerData["dShaders"].keys())

        return self.dLayerData["dShaders"]

    def startFrame(self):
        """
        Returns the start frame specified for the layer. It's either specified
        at layer level or at global level
        """

        lstData = self.dLayerData["dRenderSettings"]["lstRange"]

        if lstData[0]:
            if lstData[1] != None:
                return lstData[1]

        return self.parent.dGlobals["iStart"]
        
    def visibility(self):
        """
        Returns what should be visibile for the currently selected layer
        """

        return self.dLayerData["sVisibility"]