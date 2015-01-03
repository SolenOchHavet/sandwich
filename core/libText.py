#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""

Library "Text"

Stores all text defined in Sandwich. We will use several suffixes to define what type of text it is:
* Tip: Shows the tip for an element (ex: text.visibility.addobjectsTip)
* Label: Show the text for a widget (ex: text.visibility.addobjectsLabel)

"""

import maya.cmds as mc
import maya.mel as mel

import string
import re
import os
import sys
import subprocess as sub


class Text(object):
    def __init__(self):
        self.code = Code()
        self.overview = Overview()
        self.override = OverrideGlobals()
        self.shaders = Shaders()
        self.visibility = Visibility()


class Code(object):
    def __init__(self):
        self.overrideLabel = "Override Code"
        self.revertLabel = "Revert Code"
        self.overrideTip = "Set the override code that should be run when this render layer is active."
        self.revertTip = "Set the revert code that should be run when this render layer is inactive."

class OverrideGlobals(object):
    """
    Contains all labels and tips for tab "Output Settings"
    """

    def __init__(self):
        self.cameraLabel = "Override Camera Name"
        self.cameraBrowseLabel = "Browse..."
        self.engineLabel = "Override Engine"
        self.rangeLabel = "Override Range"
        self.resolutionLabel = "Override Resolution"

        self.cameraactivateTip = "Activate this check box if you wish to override " \
            "the render camera for this render layer."
        self.cameraTip = "Select the render camera that should be used to render " \
            "this layer."
        self.camerafieldTip = "Write the name of the render camera that should be " \
            "used to render this layer."
        self.camerabrowseTip = "Select the render camera that should be used to " \
            "render this layer from a list."
        self.resolutionactivateTip = "Activate this check box if you wish to " \
            "override the resolution for this render layer."
        self.resolutionTip = "Set the resolution that should be used to render " \
            "this layer."
        self.widthTip = "Set the width of the resolution that should be used to " \
            "render this layer."
        self.heightTip = "Set the height of the resolution that should be used to " \
            "render this layer."
        self.rangeactivateTip = "Activate this check box if you wish to override " \
            "the frame range for this render layer."
        self.rangeTip = "Set the frame range that should be used to render this layer."
        self.startTip = "Set the start frame that should be used to render this layer."
        self.endTip = "Set the end frame that should be used to render this layer."
        self.stepTip = "Set the frame step that should be used to render this layer."
        self.engineactivateTip = "Activate this check box if you wish to override " \
            "the render engine for this render layer."
        self.engineTip = "Select the render engine that should be used to render " \
            "this layer."

class Overview(object):
    """
    Contains all labels and tips for tab "Overview"
    """

    def __init__(self):
        self.descriptionLabel = "Your Notes"

        self.descriptionTip = "Write down all ideas, reminders and general comments " \
            "about the render layer here."

class Shaders(object):
    """
    Contains all labels and tips for tab "Shaders"
    """

    def __init__(self):
        self.addshaderLabel = "Add Shader..."
        self.renameshaderLabel = "Rename Shader..."
        self.addobjectsLabel = "Add Objects"
        self.organizebjectsLabel = "Reorganize Objects"
        self.shaderlistLabel = "Shader List"
        self.assignLabel = "Assign to these Objects"


        self.addshaderTip = "Add new shader from the scene."
        self.renameshaderTip = "Rename selected shader. Will not rename the shader " \
            "in the scene. Name must be unique."
        self.addobjectsTip = "Add selected objects from the scene."
        self.organizebjectsTip = "Reorganizes the assigned object's names in " \
            "alphabetic order per comment section."
        self.shaderlistTip = "All current shaders for the render layer. " \
            "Select one to set which objects it should assign to."
        self.assignTip = "Set which objects should be affected by the currently " \
            "selected shader."

class Visibility(object):
    """
    Contains all labels and tips for tab "Visibility"
    """

    def __init__(self):
        self.addobjectsLabel = "Add Objects"
        self.organizebjectsLabel = "Reorganize Objects"

        self.addobjectsTip = "Add selected objects from the scene."
        self.organizebjectsTip = "Reorganizes the assigned object's names in " \
            "alphabetic order per comment section."
        self.visibilityTip = "Set which objects should be visible in this render " \
            "layer. Python styled comments allowed."