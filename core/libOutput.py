#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""

Library "Output"

Handles the export and rendering functions.

"""

import os
import re
import sys
import subprocess as sub

import maya.cmds as mc


class Output(object):
    def __init__(self, parent = None):
        self.parent = parent

        self.sMayaPath = os.getenv("MAYA_LOCATION")

        if sys.platform == "win32":
            self.sMayaPath += "/bin/Render.exe"
            self.sFileHeader = ""
            self.sFileExt = ".bat"

        else:
            self.sMayaPath += "/bin/Render"
            self.sFileHeader = "#!/bin/sh\n"
            self.sFileExt = ""

    def export(self, lstRenderLayers, bAsBinary = False, bAsAscii = False):
        """
        Exports a list of render layers either as Maya Binary or Maya Ascii.

        lstRenderLayers is a list of all render layers that's going to be exported.
        bAsBinary specifies if Maya Binary files should be used.
        bAsAscii specifies if Maya Ascii files should be used.
        """

        lstOutput = []

        # Export Settings
        bSettingImportRefs = self.parent.getGlobalsValue("bSettingImportRefs")
        sOriginalScene = mc.file(query = True, sn = True)

        # Put together the full export path with file name but no file extension
        # yet
        sExportPath = self.parent.getGlobalsValue("sOutputScenes")
        sFileName = self.sceneName()

        if not os.path.exists(sExportPath):
            os.makedirs(sExportPath)

        # If we are going to import references into the main scene we need an
        # original backup of the scene
        if bSettingImportRefs:
            sTemp = self.parent.getGlobalsValue("sOutputScenes") + "/sandwich_restore"
            sSavedTemp = self.saveFile(sTemp, bAsBinary = True)

        for oLayer in lstRenderLayers:
            sRenderLayerPath = sExportPath + "/" + oLayer.fileName()

            # Execute the layer
            oLayer.execute()

            # If user wish to import the references into the scene, open the
            # saved file, merge the references, resave the file and then open
            # the temp file that we began from
            if bSettingImportRefs:
                self.mergeReferences()
                sSavedFile = self.saveFile(sRenderLayerPath, bAsBinary, bAsAscii)
                
                mc.file(sSavedTemp, open = True)

            else:
                sSavedFile = self.saveFile(sRenderLayerPath, bAsBinary, bAsAscii)
            
            lstOutput.append(sSavedFile)

            print "Sandwich: Exported render layer \"%s\" to file %s" % \
                (oLayer.layerName(), sSavedFile)

        mc.file(rename = sOriginalScene)

        if bSettingImportRefs:
            if os.path.exists(sSavedTemp):
                try:
                    os.remove(sSavedTemp)

                except:
                    print "Sandwich: Warning! Failed to remove temp file %s. Skipping" % (sSavedTemp)

        print "Sandwich: All exports done! Check log for further details"

        return lstOutput

    def mergeReferences(self):
        """
        Imports all references into the scene. This is a setting that can be
        activated from Sandwich Globals. Use only if you encounter references
        disappearing when rendering. Stupid bug or something.
        """

        lstInvalidRefs = (re.compile("^sharedNode$"), re.compile("_UNKNOWN_REF_NODE_$"))

        for x in range(5):
            # If only one reference node exists and it's sharedNode, then
            # we are done
            lstReferences = mc.ls(type = "reference")

            for sReferenceNode in lstReferences:
                for reInvalidRef in lstInvalidRefs:
                    if reInvalidRef.search(sReferenceNode):
                        lstReferences.remove(sReferenceNode)

            if not lstReferences:
                break

            for sReferenceNode in lstReferences:
                try:
                    sUnresolvedName = mc.referenceQuery(sReferenceNode,
                        filename = True, un = True)
                    mc.file(sUnresolvedName, importReference = True)

                except:
                    print "Sandwich: Warning! Could not import reference node %s. " \
                        "Skipping." % (sReferenceNode)

    def render(self, lstRenderLayers, bCurrentFrame = False, bEverything = False):
        """
        Renders a list of render layers either using current frame or their
        full range.

        lstRenderLayers is a list of all render layers that's going to be rendered.
        bCurrentFrame specifies if only the current frame should be rendered.
        bEverything specifies if the full range for each render layer should be rendered.
        """

        # Variables
        sCmds = self.sFileHeader

        # The batch file will be put inside the same folder as the scenes are
        # exported to
        sExportPath = self.parent.getGlobalsValue("sOutputScenes")
        sSandwichFile = sExportPath + "/sandwich_batchRender" + self.sFileExt

        # Export selected render layers into binary files
        lstFilePaths = self.export(lstRenderLayers, bAsBinary = True)

        # Loop through all layers in order to put together the render commands
        for oLayer in lstRenderLayers:
            # Get the start and end frame depending on the values of
            # bCurrentFrame and bEverything are set to
            if bCurrentFrame:
                iStartFrame = mc.currentTime(query = True)
                iEndFrame = iStartFrame

            else:
                iStartFrame = oLayer.startFrame()
                iEndFrame = oLayer.endFrame()

            # The name of the rendered image
            sImageName = oLayer.layerName() + "_" + oLayer.cameraName()

            # Setup the folder path to where the rendered image will be saved
            # and make sure it already exists
            sRenderPath = "%s/%s_%s/%sx%s/" %\
                (dSettings["sRenderPath"], oLayer.fileName(),   # TODO!! RenderPath is actually same for all layers, take it from main?
                oLayer.cameraName(), oLayer.resolutionWidth(),
                oLayer.resolutionHeight())

            if not os.path.exists(sRenderPath):
                os.makedirs(sRenderPath)

            # Add the render command for the engine
            sCmds += oLayer.renderEngine.renderCommand() % \
                (self.sMayaPath, iStartFrame, iEndFrame, 
                oLayer.resolutionWidth(), oLayer.resolutionHeight(), 
                oLayer.cameraName(), sRenderPath, sImageName, lstFilePaths[x])
            sCmds += "\n"

        # Last command will be removing the batch render file
        if sys.platform != "win32":
            sCmds += "rm -f " + sSandwichFile + "\n"

        oFileOut = file(sSandwichFile, "w")
        oFileOut.write(sCmds)
        oFileOut.close()

        # If Unix, make file executable
        if sys.platform != "win32":
            os.system("chmod +x " + sSandwichFile)

        # Put together the final command for executing the script. Script will
        # be executed in a separate
        sRunCmd = self.parent.getGlobalsValue("sTerminalApp")
        sRunCmd = sRunCmd.replace("$BATCHFILE", sSandwichFile)

        sub.Popen(sRunCmd, shell = True, universal_newlines = True,
            env = os.environ)

        print "Sandwich: Executed the render command: " + sRunCmd

    def saveFile(self, sFullPath, bAsBinary = False, bAsAscii = False):
        """
        Saves file into a Maya Ascii or Binary file.

        sFullPath specifies the full path except the file extension.
        Use bAsBinary and bAsAscii to specify format.
        """

        if bAsBinary:
            sType = "mayaBinary"
            sFullPath += ".mb"

        elif bAsAscii:
            sType = "mayaAscii"
            sFullPath += ".ma"

        mc.file(rename = sFullPath)

        try:
            mc.file(save = True, force = True, type = sType)
            return sFullPath

        except:
            return ""