#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""

Core "Main"

The main file of Sandwich's core. You can use this from the commandline instead of Sandwich's
interface if you are hardcore =)

"""

import maya.cmds as mc
import maya.mel as mel

import string
import re
import os
import sys
import subprocess as sub

import libLayer
import libOutput
import libUtils
import libNode
import libUI
reload(libLayer)
reload(libOutput)
reload(libUtils)
reload(libNode)
reload(libUI)


class MainCore(object):
    def __init__(self):
        self.dGlobals = {}
        self.dRenderGlobals = {}
        self.dDefaultRenderGlobals = {}
        self.dLayers = {} # TODO: REMOVE!
        self.lstLayers = []
        self.sCurrentLayer = ""
        self.sMasterLayer = "masterLayer"
        self.bIsFirstRun = False
        self.lstSelection = []

        # Get the Maya version as a integer
        self.iMayaVersion = int(re.search("\d+", mc.about(v=True)).group())

        self.reloadEngines()

        self.out = libOutput.Output(self)
        self.utils = libUtils.Utils()
        self.node = libNode.Node()
        self.ui = libUI.UICore(self)
        self.__layer = libLayer.Layer(self)

        self.reIsLight = re.compile("Light$")

        # Post actions that have to take place after the initialization of above classes
        self.layer(self.node.selected()).select()

    def addDefaultRenderGlobals(self):
        """
        Sets the default render globals for all render engines available in Sandwich. When a render layer later saves
        it's settings it will only store what has been edited. Like git.
        """

        self.dDefaultRenderGlobals = self.utils.renderGlobals(self.engines())

    def addGlobals(self):
        """
        Adds default globals if they do not exists. Override them if appropriate environment variable exists.
        """

        if self.dGlobals:
            return

        self.dGlobals = {
            "sOutputRenders": "",
            "sOutputScenes": "",
            "sDefaultCamera": "",
            "iWidth": "1024",
            "iHeight": "576",
            "iStart": "1",
            "iEnd": "10",
            "iStep": "1",
            "bSettingImportRefs": False,
            "sTerminalApp": "",
            "sDefaultEngine": "mental ray"
        }

        # If Sandwich's environment variables exists, they will override the
        # defaults values

        # Check for environment variable SANDWICH_OUTPUT_RENDERS
        if os.environ.has_key("SANDWICH_OUTPUT_RENDERS"):
            print "Sandwich: Found environment variable " \
                  "SANDWICH_OUTPUT_RENDERS. Sets \"Output Renders\" -> %s" % \
                  (os.environ["SANDWICH_OUTPUT_RENDERS"])
            self.dGlobals["sOutputRenders"] = os.environ["SANDWICH_OUTPUT_RENDERS"]

        # Check for environment variable SANDWICH_OUTPUT_SCENES
        if os.environ.has_key("SANDWICH_OUTPUT_SCENES"):
            print "Sandwich: Found environment variable " \
                  "SANDWICH_OUTPUT_SCENES. Sets \"Output Scenes\" -> %s" % \
                  (os.environ["SANDWICH_OUTPUT_SCENES"])
            self.dGlobals["sOutputScenes"] = os.environ["SANDWICH_OUTPUT_SCENES"]

        # Check for environment variable SANDWICH_RESOLUTION
        if os.environ.has_key("SANDWICH_RESOLUTION"):
            sResolution = os.environ["SANDWICH_RESOLUTION"].lower().strip()

            if re.search("^[0-9]+x[0-9]+$", sResolution):
                print "Sandwich: Found environment variable " \
                      "SANDWICH_RESOLUTION. Sets \"Default Resolution\" -> %s" % \
                      (sResolution)

                lstTemp = sResolution.split("x")

                self.dGlobals["iWidth"] = lstTemp[0]
                self.dGlobals["iHeight"] = lstTemp[1]

            else:
                print "Sandwich: Warning! Environment variable " \
                      "SANDWICH_RESOLUTION contained the invalid value: %s. " \
                      "Must have a syntax like: 1024x576" % \
                      (sResolution)

        # Check for environment variable SANDWICH_RANGE
        if os.environ.has_key("SANDWICH_RANGE"):
            sRange = os.environ["SANDWICH_RANGE"].strip()

            if re.search("^[-,0-9]+ [-,0-9]+ [-,0-9]+$", sRange):
                lstTemp = sRange.split()
                print "Sandwich: Found environment variable SANDWICH_RANGE. " \
                      "Sets \"Default Range\" -> %s-%s@%s" % \
                      (lstTemp[0], lstTemp[1], lstTemp[2])

                self.dGlobals["iStart"] = lstTemp[0]
                self.dGlobals["iEnd"] = lstTemp[1]
                self.dGlobals["iStep"] = lstTemp[2]

            else:
                print "Sandwich: Warning! Environment variable " \
                      "SANDWICH_RANGE contained the invalid value: %s. " \
                      "Must have a syntax like: 1 60 1" % \
                      (sRange)

        # Check for environment variable SANDWICH_IMPORT_REFERENCES
        if os.environ.has_key("SANDWICH_IMPORT_REFERENCES"):
            sSetting = os.environ["SANDWICH_IMPORT_REFERENCES"].strip()

            if re.search("^[0, 1]$", sSetting):
                print "Sandwich: Found environment variable " \
                      "SANDWICH_IMPORT_REFERENCES. Sets setting " \
                      "\"Import references into the scene on export\" -> %s" % \
                      (bool(sSetting))

                self.dGlobals["bSettingImportRefs"] = bool(sSetting)

            else:
                print "Sandwich: Warning! Environment variable " \
                      "SANDWICH_IMPORT_REFERENCES contained the invalid value: %s. " \
                      "Value must be 0 or 1." % \
                      (sSetting)

        # Check for environment variable SANDWICH_TERMINAL. Otherwise try
        # guessing the terminal app
        if os.environ.has_key("SANDWICH_TERMINAL"):
            print "Sandwich: Found environment variable SANDWICH_TERMINAL. " \
                  "Sets \"Terminal App\" -> %s" % \
                  (os.environ["SANDWICH_TERMINAL"])
            self.dGlobals["sTerminalApp"] = os.environ["SANDWICH_TERMINAL"]

        else:
            if sys.platform == "win32":
                self.dGlobals["sTerminalApp"] = "cmd.exe $BATCHFILE"

            elif sys.platform == "darwin":
                self.dGlobals["sTerminalApp"] = "open -a terminal $BATCHFILE"

            else:
                print "Sandwich: Warning! Could not figure out the command " \
                      "for launching a terminal in your operating system. " \
                      "Please input it manually in Globals or set the " \
                      "environment variable SANDWICH_TERMINAL"
                self.dGlobals["sTerminalApp"] = "/usr/bin/terminal $BATCHFILE"

    def addLayerRenderGlobals(self):
        # Add default render globals if they do not exists yet
        if not self.dRenderGlobals:
            self.addRenderGlobals()

        dLayerRenderGlobals = self.utils.renderGlobals(self.engines())
        dDefaultRenderGlobals = self.dRenderGlobals.copy()
        dOutputRenderGlobals = {}

        # Iterate through all render engines available
        for sRenderEngine in dLayerRenderGlobals.keys():
            dOutputRenderGlobals[sRenderEngine] = []

            for lstSetting in dLayerRenderGlobals[sRenderEngine]:
                # Search for this setting in dDefaultRenderGlobals until we find it
                iIndex = 0
                bFoundAttr = False

                for lstDefault in dDefaultRenderGlobals[sRenderEngine]:
                    # If we find it check if it still has the same value. If not, then add it to our
                    # dOutputRenderGlobals. Also remove the entry from dDefaultRenderGlobals to iterate faster!
                    if lstSetting[0] == lstDefault[0]:
                        bFoundAttr = True

                        if lstSetting[1] != lstDefault[1]:
                            dOutputRenderGlobals[sRenderEngine].append(lstSetting)

                        break

                    iIndex += 1

                # If the attribute was found delete it to decrease the list to iterate through!
                if bFoundAttr:
                    dDefaultRenderGlobals[sRenderEngine].pop(iIndex)

            # Remove the engine once iterated to save some memory
            del dDefaultRenderGlobals[sRenderEngine]

        self.dLayers[self.sCurrentLayer]["dRenderGlobals"] = dOutputRenderGlobals

    def addRenderGlobals(self):
        """
        Sets the default render globals for all render engines available in Sandwich. When a render layer later saves
        it's settings it will only store what has been edited. Like git.
        """

        self.dRenderGlobals = self.utils.renderGlobals(self.engines())

    def engines(self):
        """
        Returns a list of all supported engines for Sandwich. Please note that
        this list does not reflect which engines that are actually installed
        on the user's machine.
        """

        return self.lstEngines

    def existsShaderInLayer(self, sShaderName, sRenderLayer):
        """
        Checks if shader sShaderName exists for render layer sRenderLayer
        """

        if not sRenderLayer in self.dLayers.keys():
            print "Sandwich: ERROR! Specified render layer \"%s\" does not exists!" % (sRenderLayer)

            exit()

        return sShaderName in self.dLayers[sRenderLayer]["dShaders"].keys()

    def export(self, lstRenderLayers, bAsBinary = True, bAsAscii = False):
        self.out.export(lstRenderLayers, bAsBinary = True, bAsAscii = False)

    def getAttributeEnum(self, sNode, sAttrName):
        lstResult = mc.attributeQuery(sAttrName, node = sNode, listEnum = True)
        lstOutput = []

        if lstResult:
            for sItem in lstResult[0].split(":"):
                lstOutput.append(sItem.split("=")[0])

        return lstOutput

    def getAttributeName(self, sNodeWithAttribute):
        return mc.attributeName(sNodeWithAttribute)

    def getAttributeType(self, sNodeWithAttribute):
        dAttrTypes = {"bool": 1, "float": 2, "short": 3, "enum": 4, "string": 5,
            "long": 6, "TdataCompound": 7, "float3": 8, "time": 9, "byte": 10}
        sAttrType = mc.getAttr(sNodeWithAttribute, type = True)

        if sAttrType in dAttrTypes.keys():
            return dAttrTypes[sAttrType]

        else:
            return 0

    def getAttributeValue(self, sNodeWithAttribute):
        return mc.getAttr(sNodeWithAttribute)

    def getDefaultRenderGlobalsItem(self, sRenderEngine, sAttr):
        for lstItem in self.dDefaultRenderGlobals[sRenderEngine]:
            if lstItem[0] == sAttr:
                return lstItem[1]

    def getGlobals(self):
        return self.dGlobals

    def getGlobalsValue(self, sValueName):
        return self.dGlobals[sValueName]

    def getOnlyNew(self, lstExistingObjects, lstNewObjects, bAsList = False):
        """
        Returns only those objects in lstNewObjects that does not yet exists
        in lstExistingObjects. This method also supports regular expression
        entries in lstExistingObjects (that are usually taken from the interface).
        This way an entry of ex. "myHouse*GEO" will prevent this method
        of adding "myHouse01_GEO", "myHouse999_GEO" from the lstNewObjects if
        they were supplied.
        """

        lstOutput = []

        # Iterate through the new objects
        for sSelectedObject in lstNewObjects:
            bAlreadyExists = False

            # Iterate through the existing objects, making each a regular
            # expression that you check sSelectedObject against
            for sExistingObject in lstExistingObjects:
                sRegExp = sExistingObject.replace("*", ".{0,}")
                if re.search(sRegExp, sSelectedObject):
                    bAlreadyExists = True

                    break

            if not bAlreadyExists:
                lstOutput.append(sSelectedObject)

        # Return either as a list or string
        if bAsList:
            return lstOutput

        else:
            return string.join(lstOutput, " ")

    def getOnlyObjects(self, sText):
        """
        Returns a list of all objects specifies in the text.
        Any Python comment inside the text will be removed.
        """

        sOutput = ""

        for sLine in re.split("\n", sText.strip()):
            reFindComment = re.search("#", sLine)
            if reFindComment:
                # If we find a comment, we will remove that part
                # of the line. If comment however start at position
                # zero, then we will skip it
                if reFindComment.start():
                    sOutput += sLine[0:reFindComment.start()].strip() + "\n"

            else:
                sOutput += sLine.strip() + "\n"

        return re.split("\\s+", sOutput)

    def getReorganizedContent(self, sText):
        """
        Reorganizes the sText in alphabetical order. Takes Python
        comments into consideration, meaning that everything up to
        comment gets sorted for itself.
        """

        sOutput = ""
        sSection = ""

        for sLine in re.split("\n", sText.strip()):
            reIsComment = re.search("#", sLine)

            if reIsComment:
                # When a comment has been found, we will sort the
                # current content of sSection and add it to sOutput
                if sSection:
                    lstContent = sorted(re.split("\\s+", sSection))
                    sOutput += string.join(lstContent, " ").strip() + "\n\n"
                    sSection = ""

                # There are two ways of making comments. One type is
                # by having a complete row being a comment and the other
                # one could be just after some objects. In the later
                # mentioned way, we need to sort that line separately

                sTemp = sLine[0:reIsComment.start()]
                if sTemp.strip():
                    # We have a line with objects and comments at the end
                    sNewLine = string.join(sorted(re.split("\\s+", sTemp)), " ")
                    sNewLine += "  " + sLine[reIsComment.start():]

                    sOutput += sNewLine.strip() + "\n\n"

                else:
                    # This line is only a comment
                    sOutput += sLine.strip() + "\n"

            else:
                sSection += sLine

        # If there was content after the last found comment, we will add it
        if sSection:
            lstContent = sorted(re.split("\\s+", sSection))
            sOutput += string.join(lstContent, " ").strip()

        return sOutput

    def getSceneCameras(self):
        lstCameraShapes = mc.ls(type = "camera")
        lstDefaults = ["frontShape", "perspShape", "sideShape", "topShape"]
        lstOutput = []

        if not lstCameraShapes:
            lstCameraShapes = []

        for sCameraShape in lstCameraShapes:
            if not sCameraShape in lstDefaults:
                lstTemp = mc.listRelatives(sCameraShape, parent = True)
                lstOutput.append(lstTemp[0])

        return lstOutput

    def getSceneSelectedObjects(self):
        lstOutput = mc.ls(sl = True)
        if not lstOutput:
            lstOutput = []

        return lstOutput

    def getSceneShaders(self):
        """
        Returns all unassigned shaders within the scene by comparing with what the
        current layer has
        """

        lstAll = mc.ls(materials = True)
        lstLayerShaders = self.layer().shaders() + ["lambert1", "particleCloud1"]
        lstOutput = []

        for sSceneSG in lstAll:
            if not sSceneSG in lstLayerShaders:
                lstOutput.append(sSceneSG)

        return sorted(lstOutput)

    def getSupportedEngines(self):
        # TODO: REMOVE? I THINK THIS DOES THE SAME AS engines() ?
        return ["mental ray", "maya software", "vray"]

    def help(self):
        """
        Launches the Help page for Sandwich in an Internet browser
        """

    def layer(self, sLayerName = None):
        """
        Returns the Layer object for the specified layer. If no layer has been
        specified, the currently selected layer will be used.
        """

        for oLayer in self.lstLayers:
            if oLayer.layerName() == sLayerName or self.sCurrentLayer:
                return oLayer

    def layers(self):
        """
        Returns a list of all layers currently available in the scene
        """

        return self.lstLayers

    def newLayer(self, sLayerName):
        """
        Create a new layer and change it into the default layer
        """

        # Check if the name is our reserved word "masterLayer"
        if re.search("^" + self.sMasterLayer + "$", sLayerName, re.IGNORECASE):
            return "The name \"%s\" is a reserved name. Please " \
                   "change it and try again." % (self.sMasterLayer)

        # Check if the name already exists
        for oLayer in self.layers():
            if re.search(sLayerName, oLayer.layerName(), re.IGNORECASE):
                return "There is already a render layer with the name \"%s\"! " \
                       "Please change it and try again." % (sLayerName)

        # Add the render layer
        dNewLayer = {
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

        # Add all supported render engines
        for sRenderEngine in self.lstSupportedEngines:
            dNewLayer["dRenderGlobals"][sRenderEngine] = []

        oLayer = libLayer.Layer(self, sLayerName, dNewLayer)
        self.lstLayers.append(oLayer) 

        # Set the new layer to the current working layer
        self.sCurrentLayer = sLayerName

    def reload(self):
        # Load all layers available from the node
        dLayers = self.node.layers()

        for sLayerName in dLayers.keys():
            oLayer = libLayer.Layer(self, sLayerName, dLayers[sLayerName])

            self.lstLayers.append(oLayer)
        
        # Load the render globals. If no render globals exists yet, then create
        # new that will directly be stored in the Sandwich node
        dData = self.node.renderGlobals()

        if not dData:
            # Because no default render globals exists yet, create them and 
            # store them on the node
            dData = self.utils.renderGlobals(self.engines())
            self.node.saveDefaultRenderGlobals(dData)

        self.setRenderGlobals(dData)
        self.setDefaultRenderGlobals(dData)

        # Load the Sandwich globals
        dData = self.node.globals()

        if sData:
            self.setGlobals(dData)

        else:
            self.addGlobals()
            self.node.saveGlobals(self.dGlobals)

    def reloadEngines(self):
        self.lstEngines = []
        sDirPath = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        print "sDirPath", sDirPath
        for sFileName in os.listdir(sDirPath):
            if re.search("^_", sFileName):
                continue

            if not re.search("\.py$", sFileName):
                continue

            sFileName = sFileName.rsplit(".", 1)[0]

            module = __import__("engines." + sFileName)
            print module, dir(module)
            self.lstEngines.append(__import__("engines." + sFileName).Engine(self.iMayaVersion))

        print self.lstEngines

    def render(self, lstRenderLayers, bCurrentFrame = False, bEverything = False):
        self.out.render(lstRenderLayers, bCurrentFrame, bEverything)

    def revertRenderLayerAttributes(self):
        """
        Before saving the new attribute edits, we must make sure to use the old settings stored in the sandwichNode
        to revert all attributes. This is to prevent cases where the old override value for an attribute still would
        exists instead of the revert value when changing into a new attribute name.
        """

        dAttributeData = self.node.getLayerAttributesData(self.sCurrentLayer)

        for sAttributeName in dAttributeData.keys():
            self.utils.applyAttribute(sAttributeName, dAttributeData[sAttributeName]["sRevertValue"],
                dAttributeData[sAttributeName]["sObjects"].split())

    def revertSelection(self):
        if self.lstSelection:
            mc.select(self.lstSelection)

    def saveGlobals(self):
        self.node.saveGlobals()

    def saveSelection(self):
        self.lstSelection = mc.ls(sl = True)

    def setDefaultRenderGlobals(self, dData):
        self.dDefaultRenderGlobals = dData

    def setGlobals(self, dData):
        self.dGlobals = dData

    def setGlobalsValue(self, sValueName, xValue):
        self.dGlobals[sValueName] = xValue

    def setLayerRenderSetting(self, sRenderSetting, lstData):
        """
        Set what layer render settings should be used for the currently selected layer
        """

        self.dLayers[self.sCurrentLayer]["dRenderSettings"][sRenderSetting] = lstData

    def setRenderViewEngine(self, sRenderEngine):
        """
        Sets the current render engine in Maya's Render View
        """

        # TODO: TEMP SOLUTION!!
        for oEngine in self.lstEngines:
            if oEngine.engineName() == sRenderEngine:
                break

        self.utils.setRenderViewEngine(oEngine)

    def transferShader(self, sShaderName, sRenderLayer):
        """
        Transfer shader sShaderName from current render layer to layer sRenderLayer.
        """

        self.dLayers[sRenderLayer]["dShaders"][sShaderName] = \
            self.dLayers[self.sCurrentLayer]["dShaders"][sShaderName]

        # Re-save the specified render layer into Sandwich's scene node
        self.node.save(self.layer(sRenderLayer))

    def translateMentalRayAttr(self, sNodeWithAttr):
        sNodeWithAttr = re.sub("\$MG", "mentalrayGlobals", sNodeWithAttr)
        sNodeWithAttr = re.sub("\$DO", "miDefaultOptions", sNodeWithAttr)

        return re.sub("\$DF", "miDefaultFramebuffer", sNodeWithAttr)

    def translateSoftwareAttr(self, sNodeWithAttr):
        sNodeWithAttr = re.sub("\$RG", "defaultRenderGlobals", sNodeWithAttr)

        return re.sub("\$RQ", "defaultRenderQuality", sNodeWithAttr)

    def translateVrayAttr(self, sNodeWithAttr):
        return re.sub("\$VS", "vraySettings", sNodeWithAttr)