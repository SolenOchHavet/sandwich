#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""

Library "Utils"

Handles the applying of attributes, shaders and MEL on objects within Maya.

"""

import re
import string

import maya.cmds as mc
import maya.mel as mel


class Utils(object):
    def __init__(self):
        self.reDirName = re.compile("[\|,_,a-z,0-9,:]+\|", re.IGNORECASE)

    def applyAttribute(self, sAttributeName, sValue, lstObjects):
        """
        Applies the attribute sAttributeName to all objects defined in the
        list lstObjects with the value of sValue. This approach evaluates
        the content of the variable sValue in order to figure out if it's
        a string or not
        """

        lstGeometries = self.getGeometries(lstObjects)
        xValue = self.getValue(sValue)

        if not isinstance(xValue, basestring):
            for sGeometry in lstGeometries:
                try:
                    mc.setAttr(sGeometry + "." + sAttributeName, xValue)

                except:
                    print "Sandwich: Warning! Couldn't set %s.%s -> %s (type: %s)" %\
                          (sGeometry, sAttributeName, xValue, type(xValue))

        else:
            for sGeometry in lstGeometries:
                try:
                    mc.setAttr(sGeometry + "." + sAttributeName, xValue, dataType = "string")

                except:
                    print "Sandwich: Warning! Couldn't set %s.%s -> %s (type: %s)" %\
                          (sGeometry, sAttributeName, xValue, type(xValue))

    def applyCode(self, sMode, sCode):
        """
        Executes the MEL code inside the sMelCode string.
        """

        if not sCode.strip():
            return

        if sMode == "mel":
            try:
                mel.eval(sMelCode)

            except:
                print "Sandwich: Error! Couldn't run MEL code!"

        elif sMode == "python":
            try:
                eval(sCode)

            except:
                print "Sandwich: Error! Couldn't run PYTHON code!"

    def applyRenderGlobals(self, lstEngines, dDataPerEngine):
        """
        Apply the render globals using a huge dictionary containing all data
        for each render engine.
        """
        print "applyRenderGlobals()!!!! - DISABLED TEMPORARILY!"
        return
        print "---", lstEngines, dDataPerEngine
        for oRenderEngine in lstEngines:
            # If engine is not installed on the machine, then skip it
            if not oRenderEngine.isInstalled():
                continue

            # If no settings exists yet for engine, skip it
            if not dDataPerEngine.has_key(oRenderEngine.engineName()):
                continue

            for lstSetting in dDataPerEngine[oRenderEngine.engineName()]:
                sAttrPath = lstSetting[0]
                print "lstSetting", lstSetting
                for lstNode in oRenderEngine.nodes():
                    print "lstNode", lstNode
                    sAttrPath = re.sub("^\\" + lstNode[1], lstNode[0], sAttrPath)
                    print "sAttrPath", sAttrPath
                try:
                    # Try to brute force set the attribute. If we fail we handle them separately
                    mc.setAttr(sAttrPath, lstSetting[1])

                except:
                    xValue = lstSetting[1]

                    sAttrType = mc.getAttr(sAttrPath, type = True)

                    if sAttrType == "string":
                        # Once again Maya astonishes us with cool features: an empty string is a None
                        if not xValue:
                            xValue = ""

                        mc.setAttr(sAttrPath, xValue, type = sAttrType)

                    elif sAttrType == "float3":
                        xValue = xValue[0]

                        mc.setAttr(sAttrPath, xValue[0], xValue[1], xValue[2], type = sAttrType)

                    elif sAttrType == "TdataCompound":
                        #xValue = xValue[0]
                        print "Sandwich: TdataCompound attribute", sAttrPath, "not yet supported. Data:", xValue

                        #if xValue:
                        #    mc.setAttr(sAttrPath, xValue, type = sAttrType)

                        #else:
                        #    mc.setAttr(sAttrPath, xValue[0], type = sAttrType)
                    else:

                        # This is a message attribute. Begin by disconnect all attributes connected to this attribute
                        lstExistingConnections = mc.listConnections(sAttrPath, plugs = True)
                        if not lstExistingConnections:
                            lstExistingConnections = []

                        print "Sandwich: SKIPPING", lstExistingConnections
#                        for sExistingConnection in lstExistingConnections:
#                            try:
#                                mc.disconnectAttr(sAttrPath, sExistingConnection)
#
#                            except:
#                                print "Sandwich: Could not disconnect", sAttrPath, sExistingConnection
#
#                        # For some reason, this can become None?
#                        if not xValue:
#                            continue
#
#                        # Now use the list in xValue to connect to the new items
#                        for sConnection in xValue:
#                            print "connect", sAttrPath, sConnection
#                            try:
#                                mc.connectAttr(sAttrPath, sConnection)
#
#                            except:
#                                print "Sandwich: FAILED to connect", sAttrPath, "->", sConnection

                            #                        elif sAttrType == "TdataCompound":
                            #                            xValue = xValue[0]
                            #
                            #                        if sAttrType == "message":
                            #                            pass
                            #
                            #                        else:
                            #                            print "!!", sAttrType, sAttrPath, xValue
                            #                            mc.setAttr(sAttrPath, xValue, type = sAttrType)
                            #
                            #
                            #                        print "setAttr", sAttrPath, lstSetting[1], "!!! :D"
                            #                        print sAttrType

    def applyShader(self, sShader, lstObjects):
        """
        Apply shader sShader on the list of objects specified by lstObjects.
        """

        sShadingGroup = self.getShadingGroup(sShader)

        if not sShadingGroup:
            print "Sandwich: Could not find shading group for %s! Sandwich " \
                "can only find it if shader is connected using .outValue " \
                "or .outColor to shading group. Will skip this shader " \
                "until you have fixed it." % (sShader)

            return

        if not mc.objExists(sShadingGroup):
            print "Sandwich: Can't apply shading group", sShadingGroup, \
                "on objects since it does not exist in this scene!"

            return

        for sItem in lstObjects:
            lstContent = mc.ls(sItem, transforms = True)
            if not lstContent:
                lstContent = []

            for sTransform in lstContent:
                if not mc.objectType(sTransform) == "objectSet":
                    mc.sets(sTransform, forceElement = sShadingGroup,
                        edit = True, noWarnings = True)
                else:
                    lstObjectsInSet = mc.sets(sTransform, nodesOnly = True, query = True)

                    if lstObjectsInSet:
                        mc.sets(lstObjectsInSet, forceElement = sShadingGroup,
                            edit = True, noWarnings = True)

    def applyVisibility(self, lstObjects):
        """
        Applies visibility only to the defined objects. This is a special
        method that take cares of hierarchy problems.
        """

        # Create two lists, one that will contain the full path to all objects
        # that should be visible and another list containing all the objects
        # that exists at the same level in the hierarchy (siblings)
        lstVisible = []
        lstNeighbours = []
        lstSiblings = []

        for sItem in lstObjects:
            lstContent = mc.ls(sItem, transforms = True, long = True) or []
            
            for sObjectFullPath in lstContent:
                obj = self.reDirName.search(sObjectFullPath)

                if obj:
                    sParentPath = obj.group()
                    lstSiblings = mc.listRelatives(sParentPath, fullPath = True) or []

                else:
                    sParentPath = ""
                    lstSiblings = mc.ls(assemblies = True, long = True)

                lstNeighbours += lstSiblings
                lstSiblings = []

            lstVisible += lstContent

        # Create a huge string containing all the objects that should be
        # visibile
        sAllHits = string.join(lstVisible, "\n")

        # Iterate through all siblings and compare it with the huge string
        # sAllHits. If a valid hit can be found within the string then make it
        # visible, otherwise invisible
        for sItem in lstNeighbours:
            sRegExp = "^" + sItem.replace("|", "\\|")

            if re.search(sRegExp, sAllHits, re.MULTILINE):
                mc.showHidden([sItem], above = True)

            else:
                self.applyAttribute("visibility", False, [sItem])

    def getGeometries(self, lstObjects):
        """
        Returns a list of valid objects out of a list of objects that might
        contain expressions and sets.
        """

        lstOutput = []

        for sItem in lstObjects:
            lstContent = mc.ls(sItem)
            if not lstContent:
                lstContent = []

            for sTransform in lstContent:
                if not mc.objectType(sTransform) == "objectSet":
                    lstOutput.append(sTransform)

                else:
                    lstObjectsInSet = mc.sets(sTransform, nodesOnly = True, query = True)

                    if lstObjectsInSet:
                        lstOutput += lstObjectsInSet

        return lstOutput

    def getShadingGroup(self, sShader):
        """
        Returns the shading group name for a shader.
        """

        # Retrieve all connections to the slot on the material
        # that should go to the shading group
        if mc.objExists(sShader + ".outColor"):
            # This is for Maya Software and VRay shaders
            lstResult = mc.listConnections(sShader + ".outColor", d = True, s = False)

        elif mc.objExists(sShader + ".outValue"):
            # This is for mental ray shaders
            lstResult = mc.listConnections(sShader + ".outValue", d = True, s = False)

        else:
            return

        # If we found connections, then iterate through them to
        # find the first shading group
        if lstResult:
            for sNode in lstResult:
                if mc.nodeType(sNode) == "shadingEngine":
                    return sNode

        return

    def getSiblings(self, sFullObjectPath):
        """
        Returns a list of all objects on the same level in the object hierarchy.
        """

        obj = self.reDirName.search(sFullObjectPath)

        if obj:
            return mc.listRelatives(obj.group())

        else:
            return mc.ls(assemblies = True)

    def getValue(self, sValue):
        """
        Converts the sValue content into what variable type it used
        to be.
        """

        # By evaluating the sValue variable Python will figure out the type of
        # variable itself. However it will fail if it's a string, so use a try-
        # except statement to catch such occasions
        if isinstance(sValue, basestring):
            try:
                xValue = eval(sValue)

            except:
                xValue = sValue

            return xValue

        else:
            return sValue

    def renderGlobals(self, lstEngines):
        """
        Returns a dictionary with an entry for each render engine which 
        contains the current render globals for each engine.
        """

        dOutput = {}

        for oRenderEngine in lstEngines:
            # Skip engines that are not installed
            if not oRenderEngine.isInstalled():
                continue

            sRenderEngine = oRenderEngine.engineName()

            # Reset the render globals for the specified engine
            dOutput[sRenderEngine] = []

            # Iterate through all render globals nodes for the render engine
            for lstNode in oRenderEngine.nodes():
                # If node does not exists for some reason, then skip it
                if not mc.objExists(lstNode[0]):
                    continue

                # For each render globals node retrieve all attributes as short names and save them along with their
                # current state
                for sAttr in mc.listAttr(lstNode[0], shortNames = True):
                    # Skip all attribute names that contains dots. I don't know why they are included but they gives
                    # you a lot of trouble
                    if sAttr.count("."):
                        continue

                    # Begin by dividing the attributes into single and compound (multi) attributes
                    if not mc.attributeQuery(sAttr, node = lstNode[0], numberOfChildren = True):
                        # Attribute is single attribute

                        # Check if it is a normal or message attribute
                        if not mc.attributeQuery(sAttr, node = lstNode[0], message = True):
                            # This is a normal attribute, the easy ones
                            dOutput[sRenderEngine].append((lstNode[1] + "." + sAttr, mc.getAttr(lstNode[0] + "." + sAttr)))

                        else:
                            pass
                            # Because this is a message attribute, we will store a list of all outgoing connections from
                            # this attribute so we can later restore it
                            #lstConnection = mc.connectionInfo(lstNode[0] + "." + sAttr, destinationFromSource = True)
                            #if not lstConnection:
                            #    lstConnection = []

                            #dOutput[sRenderEngine].append((lstNode[1] + "." + sAttr, lstConnection))

                    else:
                        # Attribute is a compound

                        # Since we can encounter compound attributes we have to make sure we exclude their variants
                        # with one dot in their attribute names. I don't know why Maya even displays them..
                        #if sAttr.count(".") >= 1:
                        #    continue

                        sAttrPath = lstNode[0] + "." + sAttr
                        sAttrType = mc.getAttr(lstNode[0] + "." + sAttr, type = True)

                        lstMultiIndices = mc.getAttr(lstNode[0] + "." + sAttr, multiIndices = True)
                        if lstMultiIndices:
                            for iIndex in lstMultiIndices:
                                sCompoundPath = "%s.%s[%s]" % (lstNode[0], sAttr, iIndex)
                                lstMulti = mc.listAttr(sCompoundPath, multi = True, sn = True)

                                for sAttrInMulti in lstMulti[1:]:
                                    sCompoundPath = "%s.%s" % (lstNode[0], sAttrInMulti)

                                    dOutput[sRenderEngine].append(
                                        (sCompoundPath, mc.getAttr(sCompoundPath)))

                        else:
                            for sConnection in mc.listAttr(sAttrPath, multi = True, sn = True)[1:]:
                                sCompoundPath = lstNode[0] + "." + sConnection

                                dOutput[sRenderEngine].append(
                                    (sCompoundPath, mc.getAttr(sCompoundPath)))
        print "COMING OUT OF utils.renderGlobals()::", dOutput
        return dOutput

    def resetShading(self):
        """
        Apply the default shader to all objects within the scene. This is the
        default state for Sandwich before applying any shaders
        """

        lstTopLevelObjects = mc.ls(assemblies = True)
        if not lstTopLevelObjects:
            lstTopLevelObjects = []

        self.applyShader("lambert1", lstTopLevelObjects)

    def resetVisiblity(self):
        """
        Hide all top level nodes within the scene. This is the default state for
        Sandwich to always hide everything before executing a render layer

        NOTE: This is only a quick solution to hide all geometries in the scene.
        We still need to iterate through each layer and hide their assigned object
        in order to be certain that the visibility remains correctly.
        """

        mc.hide(allObjects = True)

    def sceneName(self):
        """
        Returns the scene name except the file extension

        TODO: This method should probably be moved to libMain!!
        """

        sFileName = mc.file(query = True, sn = True, shortName = True)

        if sFileName:
            sFileName = sFileName.rsplit(".", 1)[0]

        else:
            sFileName = "untitled"

        return sFileName

    def setRenderViewEngine(self, oRenderEngine = None):
        """
        Sets the current render engine in Maya's Render View
        """

        if not oRenderEngine:
            print "Sandwich: WARNING! No render engine was specified. Can't " \
                "set Render View engine!"

            return

        mel.eval("setCurrentRenderer %s;" % (oRenderEngine.engineName()))

        print "Sandwich: Sets render engine \"%s\" in Render View" % \
            (oRenderEngine.displayName())


            #def setAttr(self, sAttributeName, sValue, lstObjects):
            #	#objects_notFound	= []
            #	#objects_missesAttr	= []
            #	#objects_lockedAttr 	= []
            #	#objects_keyedAttr	= []
            #
            #	for item in objectList:
            #		objects	= mc.ls(item, transforms = True)
            #
            #		for object in objects:
            #			# If object and attribute exists
            #			if mc.objExists(object + "." + attrName):
            #				# Check if attribute is locked or keyed/connected. If any is
            #				#true, save it and report it to the user
            #				attrLocked	= mc.getAttr(object + "." + attrName,
            #									   lock = True)
            #				attrKeyed		= (mc.listConnections(object + "."
            #											  + attrName) != None)
            #
            #				if attrLocked: objects_lockedAttr.append(object)
            #				if attrKeyed:	objects_keyedAttr.append(object)
            #
            #				# Only set value if attribute is clean
            #				if not attrLocked and not attrKeyed:
            #					mc.setAttr((object + "." + attrName), value)
            #
            #			# If either object or attribute not exists, save it in list and warn
            #			# the user
            #			else:
            #				# Check if object does not exists
            #				if mc.objExists(object) == False:
            #					objects_notFound.append(object)
            #				# Check if the attribute exists
            #				elif mc.objExists(object + "." + attrName):
            #					objects_missesAttr.append(object)
            #
            #	if len(objects_notFound) > 0:
            #		text = "Section: %s\\nIssue: The following objects could " \
            #			  "not be found\\nObjects: %s" % \
            #			  (sectionName, join(objects_notFound, ", "))
            #		mel.eval("warning(\"" + text + "\")")
            #
            #	if len(objects_missesAttr) > 0:
            #		text = "Section: %s\\nIssue: The following objects misses the " \
            #			  "attribute \"%s\"\\nObjects: %s" % \
            #			  (sectionName, attrName, join(objects_missesAttr, ", "))
            #		mel.eval("warning(\"" + text + "\")")
            #
            #	if len(objects_lockedAttr) > 0:
            #		text = "Section: %s\\nIssue: The following objects have the " \
            #			  "attribute \"%s\" locked\\nObjects: %s" % \
            #			  (sectionName, attrName, join(objects_lockedAttr, ", "))
            #		mel.eval("warning(\"" + text + "\")")
            #
            #	if len(objects_keyedAttr) > 0:
            #		text = "Section: %s\\nIssue: The following objects have the " \
            #			  "attribute \"%s\" either keyed or connected to something " \
            #			  "else\\nObjects: %s" % \
            #			  (sectionName, attrName, join(objects_keyedAttr, ", "))
            #		mel.eval("warning(\"" + text + "\")")